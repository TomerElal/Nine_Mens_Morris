import random

from src.player import Player
from src.move import MoveType
from utils.strings import *
from utils.utils import perform_action_to_console


class RandomPlayer(Player):

    def get_action(self, state, type_of_required_action=MoveType.MOVE_PIECE):

        if type_of_required_action == MoveType.MOVE_PIECE:
            result = random.choice(self.get_possible_move_pieces_actions(game_state=state))
            print_result = perform_action_to_console(PLAYER_CHOOSE_MOVEMENT, RANDOM_PLAYER,
                                                     PLAYER_MOVED_PIECE, result)

        elif type_of_required_action == MoveType.PLACE_PIECE:
            result = random.choice(self.get_possible_piece_placements(game_state=state))
            print_result = perform_action_to_console(PLAYER_CHOOSE_PLACEMENT, RANDOM_PLAYER,
                                                     PLAYER_PLACED_PIECE, result)

        else:
            result = random.choice(self.get_possible_opponent_remove_pieces(game_state=state))
            print_result = perform_action_to_console(PLAYER_CHOOSE_REMOVAL, RANDOM_PLAYER,
                                                     PLAYER_REMOVED_PIECE, result)

        print(print_result)
        return result
