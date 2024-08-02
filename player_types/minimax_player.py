from src.player import Player
from src.move import MoveType
from utils.strings import *
from utils.utils import perform_action_to_console


class MinimaxPlayer(Player):

    def __init__(self, name, initial_num_of_pieces, player_color, agent):
        super().__init__(name, initial_num_of_pieces, player_color)
        self.search_agent = agent

    def get_action(self, state, type_of_required_action=MoveType.MOVE_PIECE):

        result = self.search_agent.get_action(state)

        if type_of_required_action == MoveType.MOVE_PIECE:
            print_result = perform_action_to_console(PLAYER_CHOOSE_MOVEMENT, MINIMAX_PLAYER,
                                                     PLAYER_MOVED_PIECE, result)

        elif type_of_required_action == MoveType.PLACE_PIECE:
            print_result = perform_action_to_console(PLAYER_CHOOSE_PLACEMENT, MINIMAX_PLAYER,
                                                     PLAYER_PLACED_PIECE, result)

        else:
            print_result = perform_action_to_console(PLAYER_CHOOSE_REMOVAL, MINIMAX_PLAYER,
                                                     PLAYER_REMOVED_PIECE, result)

        print(print_result)
        return result
