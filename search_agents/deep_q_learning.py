import torch
import torch.nn as nn
import torch.optim as optim
import random
import numpy as np
from collections import namedtuple, deque
import math
from search_agents.base_agent import Agent, AgentType
from src.move import Move, MoveType
from src.game_state import GameState, CellState, NUM_OF_ROWS, NUM_OF_COLS
import copy


Transition = namedtuple('Transition', ('state', 'action', 'next_state', 'reward'))


class ReplayMemory:
    def __init__(self, capacity):
        self.memory = deque([], maxlen=capacity)

    def push(self, *args):
        self.memory.append(Transition(*args))

    def sample(self, batch_size):
        return random.sample(self.memory, batch_size)

    def __len__(self):
        return len(self.memory)


class DQN(nn.Module):
    def __init__(self, input_size, output_size):
        super(DQN, self).__init__()
        self.fc1 = nn.Linear(input_size, 128)
        self.fc2 = nn.Linear(128, 128)
        self.fc3 = nn.Linear(128, output_size)

    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = torch.relu(self.fc2(x))
        x = self.fc3(x)
        return x


def get_valid_actions(game_state):
    valid_actions = []

    if (game_state.move_type == MoveType.SELECT_PIECE_TO_MOVE
            or game_state.move_type == MoveType.MOVE_SELECTED_PIECE):
        game_state.move_type = MoveType.MOVE_PIECE

    # Logic for the moving phase
    if game_state.move_type == MoveType.MOVE_PIECE:
        for piece in game_state.get_legal_actions(game_state.curr_player_turn):
            prev_position = piece[0][0] * NUM_OF_COLS + piece[0][1]
            new_position = piece[1][0] * NUM_OF_COLS + piece[1][1]
            valid_actions.append((prev_position, new_position))

    # Logic for removing opponent's piece
    if game_state.move_type == MoveType.REMOVE_OPPONENT_PIECE or (game_state.move_type == MoveType.PLACE_PIECE):
        for piece in game_state.get_legal_actions(game_state.curr_player_turn):
            position_index = piece[0] * NUM_OF_COLS + piece[1]
            valid_actions.append(position_index)

    return valid_actions


def get_state_vector(game_state):
    board_state = []
    for row in game_state.board:
        for cell in row:
            board_state.append(cell.value)
    state_vector = board_state + [game_state.curr_player_turn, game_state.move_type.value]
    return torch.tensor([state_vector], dtype=torch.float32)


def map_action_to_game(game_state, action_index):
    if game_state.move_type == MoveType.PLACE_PIECE:
        # For placing pieces, action_index corresponds to the board position
        row = action_index // NUM_OF_COLS
        col = action_index % NUM_OF_COLS
        return row, col

    if game_state.move_type == MoveType.MOVE_PIECE:
        # For moving pieces, action_index is a tuple (prev_position_index, new_position_index)
        prev_position_index, new_position_index = action_index[0], action_index[1]
        prev_row = prev_position_index // NUM_OF_COLS
        prev_col = prev_position_index % NUM_OF_COLS
        new_row = new_position_index // NUM_OF_COLS
        new_col = new_position_index % NUM_OF_COLS
        return (prev_row, prev_col), (new_row, new_col)

    if game_state.move_type == MoveType.REMOVE_OPPONENT_PIECE:
        # For removing opponent's piece, action_index corresponds to the board position
        row = action_index // NUM_OF_COLS
        col = action_index % NUM_OF_COLS
        return row, col


def calculate_reward(game_state):
    if game_state.is_game_over():
        if game_state.player1.is_lost_game(game_state, game_state.move_type):
            return 1.0, True
        elif game_state.player2.is_lost_game(game_state, game_state.move_type):
            return -1.0, True
    else:
        return 0.0, False


def opponent_select_action(game_state):
    valid_actions = get_valid_actions(game_state)
    if not valid_actions:
        return None
    return torch.tensor([[random.choice(valid_actions)]], dtype=torch.long)


class DQNAgent(Agent):
    def __init__(self, state_size, action_size,
                 batch_size=128, gamma=0.99, epsilon_start=0.9,
                 epsilon_end=0.05, epsilon_decay=1000, target_update=10,
                 memory_size=10000, lr=1e-3):
        self.state_size = state_size
        self.action_size = action_size
        self.gamma = gamma
        self.epsilon_start = epsilon_start
        self.epsilon_end = epsilon_end
        self.epsilon_decay = epsilon_decay
        self.batch_size = batch_size
        self.target_update = target_update

        # Initialize the network
        self.policy_net = DQN(state_size, action_size)
        self.target_net = DQN(state_size, action_size)
        self.target_net.load_state_dict(self.policy_net.state_dict())
        # TODO: check if needed
        self.target_net.eval()

        self.optimizer = optim.Adam(self.policy_net.parameters(), lr=lr)
        self.criterion = nn.MSELoss()
        self.steps_done = 0
        # Initialize replay buffer
        self.memory = ReplayMemory(memory_size)

    def select_action(self, state, valid_actions, move_type):
        sample = random.random()
        eps_threshold = (self.epsilon_end + (self.epsilon_start - self.epsilon_end) *
                         math.exp(-1. * self.steps_done / self.epsilon_decay))
        self.steps_done += 1
        if sample > eps_threshold:
            with torch.no_grad():
                q_values = self.policy_net(state)

                if move_type == MoveType.MOVE_PIECE:
                    valid_q_values = []

                    for action in valid_actions:
                        prev_position, next_position = action
                        q_value = q_values[0, prev_position] + q_values[0, next_position]
                        valid_q_values.append(q_value)

                    valid_q_values_tensor = torch.tensor(valid_q_values)
                    best_action_index = valid_q_values_tensor.argmax().item()
                    return torch.tensor([[valid_actions[best_action_index]]], dtype=torch.long)

                # Mask invalid actions by setting their Q-values to a very low number
                masked_q_values = torch.full(q_values.shape, -float('inf'))
                masked_q_values[0, valid_actions] = q_values[0, valid_actions]
                return masked_q_values.max(1)[1].view(1, 1)

        else:
            return torch.tensor([[random.choice(valid_actions)]], dtype=torch.long)

    def optimize_model(self):
        if len(self.memory) < self.batch_size:
            return

        transitions = self.memory.sample(self.batch_size)
        batch = Transition(*zip(*transitions))

        state_batch = torch.cat(batch.state)
        action_batch = torch.tensor(batch.action)
        reward_batch = torch.tensor(batch.reward)
        non_final_mask = torch.tensor(tuple(map(lambda s: s is not None, batch.next_state)), dtype=torch.bool)
        non_final_next_states = torch.cat([s for s in batch.next_state if s is not None])

        state_action_values = self.policy_net(state_batch).gather(1, action_batch)

        next_state_values = torch.zeros(self.batch_size)
        with torch.no_grad():
            next_state_values[non_final_mask] = self.target_net(non_final_next_states).max(1)[0]

        expected_state_action_values = (next_state_values * self.gamma) + reward_batch

        loss = self.criterion(state_action_values, expected_state_action_values.unsqueeze(1))

        self.optimizer.zero_grad()
        loss.backward()
        for param in self.policy_net.parameters():
            param.grad.data.clamp_(-1, 1)
        self.optimizer.step()

    def get_action(self, game_state):
        state = get_state_vector(game_state)
        valid_actions = get_valid_actions(game_state)
        if not valid_actions:
            return None
        action = self.select_action(state, valid_actions, game_state.move_type)
        return map_action_to_game(game_state, action.numpy()[0][0])

    def train(self, env, num_episodes=1000):
        for episode in range(num_episodes):
            new_env = GameState(copy.deepcopy(env.player1), copy.deepcopy(env.player2), MoveType.PLACE_PIECE, player_turn=1)
            state = get_state_vector(env)
            done = False
            while not done:
                if new_env.curr_player_turn == 2:  # DQN agent's turn
                    valid_actions = get_valid_actions(new_env)
                    if not valid_actions:
                        break
                    action = self.select_action(state, valid_actions, new_env.move_type)

                    # Map action to the game's move
                    action_tuple = map_action_to_game(new_env, action.numpy()[0][0])

                    # Generate the new state
                    next_state = new_env.generate_new_state_successor(new_env.curr_player_turn, action_tuple)

                    # Get the reward and check if the game is done
                    reward, done = calculate_reward(next_state)
                    reward = torch.tensor([reward], dtype=torch.float32)

                    next_state_tensor = get_state_vector(next_state) if not done else None

                    # Store the transition in memory
                    self.memory.push(state, action, next_state_tensor, reward)

                    # Move to the next state
                    new_env = next_state
                    state = next_state_tensor

                    # Perform optimization
                    self.optimize_model()
                else:  # Opponent's turn
                    # Opponent takes an action
                    opponent_action = opponent_select_action(env)
                    if opponent_action is None:
                        break
                    opponent_action_tuple = map_action_to_game(env, opponent_action.numpy()[0][0])
                    next_state = env.generate_new_state_successor(env.curr_player_turn, opponent_action_tuple)

                    # Move to the next state
                    env = next_state
                    state = get_state_vector(next_state)

                    # Check if the game is over
                    _, done = calculate_reward(next_state)
            # Update the target network at the specified interval
            if episode % self.target_update == 0:
                self.target_net.load_state_dict(self.policy_net.state_dict())

    def evaluation_function(self, game_state):
        pass
