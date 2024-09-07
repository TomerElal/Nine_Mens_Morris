import random

import common.utils
from src.player import Player
from src.move import MoveType
from common.strings import *
from common.utils import perform_placement_or_remove_action_to_console, perform_move_action_to_console
from src.game_state import CellState


def check_if_opponent_can_perform_a_mill(player_color, state, type_of_required_action):
    opponent_poss_moves = state.get_opponent_legal_actions(player_color)
    for move in opponent_poss_moves:
        new_piece_location = move[1] if (state.player1.num_of_pieces_left_to_place +
                                         state.player2.num_of_pieces_left_to_place == 0) else move
        existed_piece_in_the_possible_mill = common.utils.move_performed_a_mill(new_piece_location, state,
                                                                                state.get_opponent_color())
        if existed_piece_in_the_possible_mill:
            return existed_piece_in_the_possible_mill if type_of_required_action == MoveType.REMOVE_OPPONENT_PIECE \
                else new_piece_location
    return False


def check_if_smart_player_can_perform_a_mill(player_color, state, smart_player_poss_actions):
    for action in smart_player_poss_actions:
        new_pos = action
        if state.player1.num_of_pieces_left_to_place + state.player2.num_of_pieces_left_to_place == 0:
            new_pos = action[1]
            state.set_cell_state(action[0], CellState.EMPTY)
        can_perform_a_mill = common.utils.move_performed_a_mill(new_pos, state, player_color)
        if state.player1.num_of_pieces_left_to_place + state.player2.num_of_pieces_left_to_place == 0:
            state.set_cell_state(action[0], player_color)
        if can_perform_a_mill:
            return action
    return False


class SmartPlayer(Player):
    def get_action(self, state, type_of_required_action=MoveType.MOVE_PIECE,
                   events=None, pieces=None, selected_position=None):
        opponent_move_performed_a_mill = check_if_opponent_can_perform_a_mill(self.get_player_color(), state, type_of_required_action)
        print_result = ''
        if (type_of_required_action == MoveType.MOVE_PIECE
                or type_of_required_action == MoveType.SELECT_PIECE_TO_MOVE
                or type_of_required_action == MoveType.MOVE_SELECTED_PIECE):
            smart_player_poss_actions = self.get_possible_move_pieces_actions(game_state=state)
            result = random.choice(smart_player_poss_actions)
            smart_can_perform_a_mill = check_if_smart_player_can_perform_a_mill(self.get_player_color(), state, smart_player_poss_actions)
            if smart_can_perform_a_mill:
                result = smart_can_perform_a_mill
            else:
                if opponent_move_performed_a_mill:
                    for action in smart_player_poss_actions:
                        if opponent_move_performed_a_mill == action[1]:
                            result = action
            if not self.is_gui_game:
                print_result = perform_move_action_to_console(PLAYER_CHOOSE_MOVEMENT, self.name,
                                                              PLAYER_MOVED_PIECE, result)

        elif type_of_required_action == MoveType.PLACE_PIECE:
            smart_player_poss_actions = self.get_possible_piece_placements(game_state=state)
            result = random.choice(smart_player_poss_actions)
            smart_can_perform_a_mill = check_if_smart_player_can_perform_a_mill(self.get_player_color(), state, smart_player_poss_actions)
            if smart_can_perform_a_mill:
                result = smart_can_perform_a_mill
            else:
                if opponent_move_performed_a_mill:
                    result = opponent_move_performed_a_mill
            if not self.is_gui_game:
                print_result = perform_placement_or_remove_action_to_console(PLAYER_CHOOSE_PLACEMENT, self.name,
                                                                             PLAYER_PLACED_PIECE, result)

        else:
            smart_player_poss_actions = self.get_possible_opponent_remove_pieces(game_state=state)
            result = random.choice(smart_player_poss_actions)
            if opponent_move_performed_a_mill:
                result = opponent_move_performed_a_mill

            if not self.is_gui_game:
                print_result = perform_placement_or_remove_action_to_console(PLAYER_CHOOSE_REMOVAL, self.name,
                                                                             PLAYER_REMOVED_PIECE, result)

        if not self.is_gui_game:
            print(print_result)
            return result
        return result, True
