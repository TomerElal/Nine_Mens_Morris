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
from common.utils import move_performed_a_mill

device = torch.device(
    "cuda" if torch.cuda.is_available() else
    "mps" if torch.backends.mps.is_available() else
    "cpu"
)
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
    player1_pieces = np.zeros((NUM_OF_ROWS, NUM_OF_COLS), dtype=np.float32)
    player2_pieces = np.zeros((NUM_OF_ROWS, NUM_OF_COLS), dtype=np.float32)
    empty_spaces = np.zeros((NUM_OF_ROWS, NUM_OF_COLS), dtype=np.float32)

    # Fill the channels based on the board state
    for row in range(NUM_OF_ROWS):
        for col in range(NUM_OF_COLS):
            cell = game_state.board[row][col]
            if cell == CellState.WHITE:
                player1_pieces[row, col] = 1.0
            elif cell == CellState.BLACK:
                player2_pieces[row, col] = 1.0
            else:
                empty_spaces[row, col] = 1.0

    # Stack the channels to create a 3D tensor (3 channels, NUM_OF_ROWS, NUM_OF_COLS)
    board_tensor = np.stack([player1_pieces, player2_pieces, empty_spaces])

    # Convert the board tensor to a PyTorch tensor
    board_tensor = torch.tensor(board_tensor, device=device, dtype=torch.float32)

    # Create an additional feature vector for player turn and move type
    additional_features = torch.tensor(
        [[game_state.curr_player_turn, game_state.move_type.value]],
        device=device,
        dtype=torch.float32
    )

    return torch.cat((board_tensor.view(-1), additional_features.view(-1)), dim=0).unsqueeze(0)


def map_action_to_game(game_state, action_index):
    if action_index.numel() == 1:
        action_index = action_index.item()
    else:
        action_index = action_index.tolist()

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


def calculate_reward(game_state, num_steps, action, move_type, opponent_move_type, player_color, opponent_color):
    if game_state.is_game_over():
        if game_state.player1.is_lost_game(game_state, game_state.move_type):
            return 100, True
        elif game_state.player2.is_lost_game(game_state, game_state.move_type):
            reward = -100
            reward -= (1 / num_steps) * 10
            return reward, True
    else:
        reward = 0.0
        new_pos = action
        if move_type == MoveType.MOVE_PIECE:
            prev_pos, new_pos = action
        is_mill = move_performed_a_mill(new_pos, game_state, player_color)
        block_opponent_mill = move_performed_a_mill(new_pos, game_state, opponent_color)
        if is_mill:
            reward += 50
        if block_opponent_mill:
            reward += 10
        if move_type == MoveType.REMOVE_OPPONENT_PIECE:
            reward += 15
        if opponent_move_type == MoveType.REMOVE_OPPONENT_PIECE:
            reward -= 30
        if not is_mill and not block_opponent_mill:
            reward -= 5
        return reward, False


class DQNAgent(Agent):
    def __init__(self, state_size, action_size, batch_size=128, gamma=0.99, epsilon_start=1, epsilon_end=0.01,
                 epsilon_decay=2000, target_update=200, memory_size=100000, lr=1e-4,
                 model_save_path='dqn_model.pth'):
        super().__init__()
        self.state_size = state_size
        self.action_size = action_size
        self.gamma = gamma
        self.epsilon_start = epsilon_start
        self.epsilon_end = epsilon_end
        self.epsilon_decay = epsilon_decay
        self.batch_size = batch_size
        self.target_update = target_update
        self.model_save_path = model_save_path

        # Initialize the network
        self.policy_net = DQN(state_size, action_size).to(device)
        self.target_net = DQN(state_size, action_size).to(device)
        self.target_net.load_state_dict(self.policy_net.state_dict())
        self.target_net.eval()

        self.optimizer = optim.AdamW(self.policy_net.parameters(), lr=lr, amsgrad=True)
        self.criterion = nn.MSELoss()
        self.steps_done = 0
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
                    return torch.tensor([[valid_actions[best_action_index]]], device=device, dtype=torch.long)

                # Mask invalid actions by setting their Q-values to a very low number
                masked_q_values = torch.full(q_values.shape, -float('inf')).to(device)
                masked_q_values[0, valid_actions] = q_values[0, valid_actions]
                return masked_q_values.max(1)[1].view(1, 1)

        else:
            return torch.tensor([[random.choice(valid_actions)]], dtype=torch.long)

    def optimize_model(self):
        if len(self.memory) < self.batch_size:
            return

        transitions = self.memory.sample(self.batch_size)
        batch = Transition(*zip(*transitions))

        state_batch = torch.cat(batch.state).to(device)
        action_batch = torch.cat(batch.action).to(device)
        reward_batch = torch.cat(batch.reward).to(device)
        non_final_mask = torch.tensor(tuple(map(lambda s: s is not None, batch.next_state)), device=device,
                                      dtype=torch.bool)
        non_final_next_states = torch.cat([s for s in batch.next_state if s is not None]).to(device)

        state_action_values = self.policy_net(state_batch).gather(1, action_batch)

        next_state_values = torch.zeros(self.batch_size, device=device)
        with torch.no_grad():
            next_state_values[non_final_mask] = self.target_net(non_final_next_states).max(1).values

        expected_state_action_values = (next_state_values * self.gamma) + reward_batch

        loss = self.criterion(state_action_values, expected_state_action_values.unsqueeze(1))

        self.optimizer.zero_grad()
        loss.backward()
        torch.nn.utils.clip_grad_value_(self.policy_net.parameters(), 100)
        self.optimizer.step()

    def save_model(self, filepath=None):
        if filepath is None:
            filepath = self.model_save_path
        torch.save({
            'policy_net_state_dict': self.policy_net.state_dict(),
            'target_net_state_dict': self.target_net.state_dict(),
            'optimizer_state_dict': self.optimizer.state_dict(),
            'steps_done': self.steps_done,
        }, filepath)
        print(f"Model saved to {filepath}")

    def load_model(self, filepath=None):
        if filepath is None:
            filepath = self.model_save_path
        checkpoint = torch.load(filepath, map_location=device)
        self.policy_net.load_state_dict(checkpoint['policy_net_state_dict'])
        self.target_net.load_state_dict(checkpoint['target_net_state_dict'])
        self.optimizer.load_state_dict(checkpoint['optimizer_state_dict'])
        self.steps_done = checkpoint['steps_done']
        print(f"Model loaded from {filepath}")

    def get_action(self, game_state):
        state = get_state_vector(game_state)
        valid_actions = get_valid_actions(game_state)
        if not valid_actions:
            return None
        action = self.select_action(state, valid_actions, game_state.move_type)
        return map_action_to_game(game_state, action.view(-1))

    def train(self, player1, player2, num_episodes=1000):
        for episode in range(num_episodes):
            new_env = GameState(copy.deepcopy(player1), copy.deepcopy(player2), MoveType.PLACE_PIECE, player_turn=1)
            state = get_state_vector(new_env)
            done = False
            num_steps = 0
            opponent_move_type = MoveType.PLACE_PIECE
            while not done:
                if new_env.curr_player_turn == 2:  # DQN agent's turn
                    num_steps += 1
                    valid_actions = get_valid_actions(new_env)
                    if not valid_actions:
                        break
                    action = self.select_action(state, valid_actions, new_env.move_type)

                    action_tuple = map_action_to_game(new_env, action.view(-1))

                    next_state = new_env.generate_new_state_successor(new_env.curr_player_turn, action_tuple)

                    reward, done = calculate_reward(next_state, num_steps, action_tuple, new_env.move_type,
                                                    opponent_move_type,
                                                    CellState.BLACK, CellState.WHITE)
                    reward = torch.tensor([reward], device=device, dtype=torch.float32)

                    next_state_tensor = get_state_vector(next_state) if not done else None

                    if action.shape == torch.Size([1, 1]):
                        self.memory.push(state, torch.tensor([[action.item()]]), next_state_tensor, reward)
                    elif action.shape == torch.Size([1, 1, 2]):
                        self.memory.push(state, torch.tensor([[action.view(-1)[1].item()]]), next_state_tensor, reward)

                    new_env = next_state
                    state = next_state_tensor

                    self.optimize_model()
                else:  # Opponent's turn
                    opponent_action = new_env.player1.get_action(new_env, new_env.move_type)
                    opponent_move_type = new_env.move_type
                    next_state = new_env.generate_new_state_successor(new_env.curr_player_turn, opponent_action)

                    done = new_env.is_game_over()

                    new_env = next_state
                    state = get_state_vector(next_state)
            # Update the target network at the specified interval
            if self.steps_done % self.target_update == 0:
                self.target_net.load_state_dict(self.policy_net.state_dict())

            print(f"finished episode {episode + 1}")

    def evaluation_function(self, game_state):
        pass
