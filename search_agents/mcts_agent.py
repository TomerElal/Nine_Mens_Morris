import copy
import math
import random

from player_types.smart_player import check_if_smart_player_can_perform_a_mill, \
    check_if_opponent_can_perform_a_mill
from src.move import MoveType


class MCTSNode:
    def __init__(self, state, parent=None):
        self.state = state
        self.parent = parent
        self.children = []
        self.visits = 0
        self.score = 0

    def is_fully_expanded(self):
        return len(self.children) == len(self.state.get_legal_actions(self.state.curr_player_turn))

    def best_child(self, exploration_weight=1.4):
        choices_weights = [
            (child.score / child.visits) + exploration_weight * math.sqrt(math.log(self.visits) / child.visits)
            for child in self.children
        ]
        return self.children[choices_weights.index(max(choices_weights))]

    def add_child(self, child_state):
        child = MCTSNode(child_state, self)
        self.children.append(child)
        return child


class MCTSAgent:
    def __init__(self, player_number_of_the_opponent, num_simulations=100):
        self.player_number_of_the_opponent = player_number_of_the_opponent
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
        score = 0
        penalty, reward = 10, 100
        while not curr_simulation_state.is_game_over():
            legal_actions = curr_simulation_state.get_legal_actions(player_turn)
            action = random.choice(legal_actions)
            if curr_simulation_state.curr_player_turn == self.player_number_of_the_opponent:
                action = self.get_smart_opponent_action(curr_simulation_state, legal_actions)
                if curr_simulation_state.move_type == MoveType.REMOVE_OPPONENT_PIECE:
                    denominator = score if score != 0 else 0.1
                    score -= penalty / denominator
            else:
                if curr_simulation_state.move_type == MoveType.REMOVE_OPPONENT_PIECE:
                    denominator = score if score != 0 else 0.1
                    score += reward / denominator
                else:
                    score += 1
            curr_simulation_state = curr_simulation_state.generate_new_state_successor(player_turn, action)
            player_turn = curr_simulation_state.curr_player_turn  # Switch player

        return score

    def backpropagate(self, node, reward):
        while node is not None:
            node.visits += 1
            node.score += reward
            node = node.parent

    def best_action(self, root):
        return max(root.children, key=lambda child: child.visits).state.get_last_move()

    def get_smart_opponent_action(self, curr_simulation_state, legal_actions):
        opponent_move_performed_a_mill = check_if_opponent_can_perform_a_mill(
            curr_simulation_state.get_curr_player_color(), curr_simulation_state, curr_simulation_state.move_type)

        if (curr_simulation_state.move_type == MoveType.MOVE_PIECE
                or curr_simulation_state.move_type == MoveType.SELECT_PIECE_TO_MOVE
                or curr_simulation_state.move_type == MoveType.MOVE_SELECTED_PIECE):
            result = random.choice(legal_actions)
            smart_can_perform_a_mill = check_if_smart_player_can_perform_a_mill(
                curr_simulation_state.get_curr_player_color(), curr_simulation_state,
                legal_actions)
            if smart_can_perform_a_mill:
                result = smart_can_perform_a_mill
            else:
                if opponent_move_performed_a_mill:
                    for action in legal_actions:
                        if opponent_move_performed_a_mill == action[1]:
                            result = action
        elif curr_simulation_state.move_type == MoveType.PLACE_PIECE:
            result = random.choice(legal_actions)
            smart_can_perform_a_mill = check_if_smart_player_can_perform_a_mill(
                curr_simulation_state.get_curr_player_color(), curr_simulation_state, legal_actions)
            if smart_can_perform_a_mill:
                result = smart_can_perform_a_mill
            else:
                if opponent_move_performed_a_mill:
                    result = opponent_move_performed_a_mill
        else:
            result = random.choice(legal_actions)
            if opponent_move_performed_a_mill:
                result = opponent_move_performed_a_mill
        return result
