import numpy as np

from search_agents.base_agent import Agent, AgentType
from src.move import Move, MoveType


class MiniMaxAgent(Agent):

    def evaluation_function(self, game_state):
        # TODO: Player1 should represent MAX agent.
        return len(game_state.player1.pieces_on_board) - len(game_state.player2.pieces_on_board)

    def __init__(self, depth=1):
        self.search_depth = depth * 2

    def get_action(self, game_state):

        def minimax(curr_agent, curr_game_state, depth):

            if depth == self.search_depth or game_state.is_game_over():
                return self.evaluation_function(curr_game_state), Move.STOP

            if curr_game_state.move_type != MoveType.REMOVE_OPPONENT_PIECE:
                depth += 1

            if curr_agent == AgentType.MAX:
                max_val = -np.inf
                action_result = None
                for player_action in curr_game_state.get_legal_actions(player_number=1):
                    new_state_successor = (curr_game_state.
                                           generate_new_state_successor(player_number=1, action=player_action))
                    next_agent = AgentType.MAX if (new_state_successor.move_type ==
                                                   MoveType.REMOVE_OPPONENT_PIECE) else AgentType.MIN
                    score = minimax(next_agent, new_state_successor, depth)[0]
                    if score > max_val:
                        max_val = score
                        action_result = player_action
                return max_val, action_result

            if curr_agent == AgentType.MIN:
                min_val = np.inf
                action_result = None
                for opponent_action in curr_game_state.get_legal_actions(player_number=2):
                    new_state_successor = (curr_game_state.
                                           generate_new_state_successor(player_number=2, action=opponent_action))
                    next_agent = AgentType.MIN if (new_state_successor.move_type ==
                                                   MoveType.REMOVE_OPPONENT_PIECE) else AgentType.MAX
                    score = minimax(next_agent, new_state_successor, depth)[0]
                    if score < min_val:
                        min_val = score
                        action_result = opponent_action
                return min_val, action_result

        start_depth = 0
        if game_state.move_type == MoveType.REMOVE_OPPONENT_PIECE:
            start_depth = 1
        return minimax(AgentType.MAX, game_state, start_depth)[1]
