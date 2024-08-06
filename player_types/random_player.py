import random

from src.player import Player
from src.move import MoveType
from utils.strings import *
from utils.utils import perform_placement_or_remove_action_to_console, perform_move_action_to_console


class RandomPlayer(Player):

    def get_action(self, state, type_of_required_action=MoveType.MOVE_PIECE,
                   events=None, pieces=None, selected_position=None):

        print_result = ''
        if (type_of_required_action == MoveType.MOVE_PIECE
                or type_of_required_action == MoveType.SELECT_PIECE_TO_MOVE
                or type_of_required_action == MoveType.MOVE_SELECTED_PIECE):
            result = random.choice(self.get_possible_move_pieces_actions(game_state=state))
            if not self.is_gui_game:
                print_result = perform_move_action_to_console(PLAYER_CHOOSE_MOVEMENT, self.name,
                                                              PLAYER_MOVED_PIECE, result)

        elif type_of_required_action == MoveType.PLACE_PIECE:
            result = random.choice(self.get_possible_piece_placements(game_state=state))
            if not self.is_gui_game:
                print_result = perform_placement_or_remove_action_to_console(PLAYER_CHOOSE_PLACEMENT, self.name,
                                                                             PLAYER_PLACED_PIECE, result)

        else:
            result = random.choice(self.get_possible_opponent_remove_pieces(game_state=state))
            if not self.is_gui_game:
                print_result = perform_placement_or_remove_action_to_console(PLAYER_CHOOSE_REMOVAL, self.name,
                                                                             PLAYER_REMOVED_PIECE, result)

        if not self.is_gui_game:
            print(print_result)
            return result
        return result, True
