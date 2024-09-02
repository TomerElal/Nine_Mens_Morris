import copy
import math
import random

from search_agents.base_agent import Agent
from src.move import MoveType


class MCTSNode:
    def __init__(self, state, parent=None):
        self.state = state
        self.parent = parent
        self.children = []
        self.visits = 0
        self.wins = 0

    def is_fully_expanded(self):
        if self.state.move_type != self.state.get_player_move_type(self.state.curr_player_turn):
            k=9
        return len(self.children) == len(self.state.get_legal_actions(self.state.curr_player_turn))

    def best_child(self, exploration_weight=1.4):
        choices_weights = [
            (child.wins / child.visits) + exploration_weight * math.sqrt(math.log(self.visits) / child.visits)
            for child in self.children
        ]
        return self.children[choices_weights.index(max(choices_weights))]

    def add_child(self, child_state):
        child = MCTSNode(child_state, self)
        self.children.append(child)
        return child


class MCTSAgent:
    def __init__(self, num_simulations=2):
        self.num_simulations = num_simulations

    def get_action(self, game_state):
        copy_state = copy.deepcopy(game_state)
        if (copy_state.move_type == MoveType.SELECT_PIECE_TO_MOVE
                or copy_state.move_type == MoveType.MOVE_SELECTED_PIECE):
            copy_state.move_type = MoveType.MOVE_PIECE
        root = MCTSNode(copy.deepcopy(copy_state))

        for _ in range(self.num_simulations):
            node = self.tree_policy(root)
            reward = self.simulate(node.state)
            self.backpropagate(node, reward)

        return self.best_action(root)

    def tree_policy(self, node):
        while not node.state.is_game_over():
            if not node.is_fully_expanded():
                return self.expand(node)
            else:
                node = node.best_child()
        return node

    def expand(self, node):
        tried_actions = [child.state.get_last_move() for child in node.children]
        legal_actions = node.state.get_legal_actions(node.state.curr_player_turn)
        for action in legal_actions:
            if action not in tried_actions:
                new_state = node.state.generate_new_state_successor(node.state.curr_player_turn, action)
                return node.add_child(new_state)
        return None

    def simulate(self, state):
        curr_simulation_state = copy.deepcopy(state)
        player_turn = state.curr_player_turn
        while not curr_simulation_state.is_game_over():
            legal_actions = curr_simulation_state.get_legal_actions(player_turn)
            action = random.choice(legal_actions)
            curr_simulation_state = curr_simulation_state.generate_new_state_successor(player_turn, action)
            player_turn = curr_simulation_state.curr_player_turn  # Switch player

        # Determine the winner
        if curr_simulation_state.player1.is_lost_game(curr_simulation_state, curr_simulation_state.move_type):
            return 0
        elif curr_simulation_state.player2.is_lost_game(curr_simulation_state, curr_simulation_state.move_type):
            return 1
        else:
            return 0.5  # Draw

    def backpropagate(self, node, reward):
        while node is not None:
            node.visits += 1
            node.wins += reward
            node = node.parent

    def best_action(self, root):
        return max(root.children, key=lambda child: child.wins / child.visits).state.get_last_move()
