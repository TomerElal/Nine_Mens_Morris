from src.player import Player
from src.move import MoveType
from common.strings import *


def get_valid_input(prompt, validation_func, validation_list, prev_input=None, empty_cells=None):
    while True:
        user_input = input(prompt)
        is_valid, result = validation_func(user_input, validation_list, prev_input, empty_cells)
        if is_valid:
            return result
        else:
            print(result)


def index_format_is_valid(user_input):
    # Check if the input is exactly two characters long
    if len(user_input) != 2:
        return False

    # Check if both characters are digits
    if not (user_input[0].isdigit() and user_input[1].isdigit()):
        return False

    return True


def validate_input_of_piece_to_move(user_input, possible_move_actions, prev_input, _):
    if not index_format_is_valid(user_input):
        return False, INVALID_INPUT_FORMAT

    piece_index_to_move = tuple(int(char) for char in user_input)
    if piece_index_to_move in possible_move_actions:
        return True, piece_index_to_move

    return False, INVALID_INDEX


def validate_input_of_piece_new_place(user_input, possible_move_actions, index_to_move_from, empty_cells):
    if not index_format_is_valid(user_input):
        return False, INVALID_INPUT_FORMAT

    new_place_index = tuple(int(char) for char in user_input)
    desired_action = (index_to_move_from, new_place_index)
    if new_place_index in empty_cells and desired_action in possible_move_actions:
        return True, new_place_index

    return False, INVALID_INDEX


def validate_input_of_new_piece_placement(user_input, empty_cells_list, prev_input, _):
    if not index_format_is_valid(user_input):
        return False, INVALID_INPUT_FORMAT

    piece_placement_index = tuple(int(char) for char in user_input)
    if piece_placement_index in empty_cells_list:
        return True, piece_placement_index

    return False, INVALID_INDEX


def validate_input_of_opponent_piece_removal(user_input, opponent_cells_list, prev_input, _):
    if not index_format_is_valid(user_input):
        return False, INVALID_INPUT_FORMAT

    opponent_piece_removal_index = tuple(int(char) for char in user_input)
    if opponent_piece_removal_index in opponent_cells_list:
        return True, opponent_piece_removal_index

    return False, INVALID_INDEX


class ConsoleUserPlayer(Player):

    def get_action(self, state, type_of_required_action=MoveType.MOVE_PIECE):

        possible_actions = self.get_possible_actions(state, type_of_required_action)
        greeting = PLAYER_TURN_GREETING_TEMPLATE.format(
            color=self.player_color.color,
            name=self.name,
            reset=Style.RESET_ALL
        )
        empty_cells = state.get_empty_cells()
        if type_of_required_action == MoveType.MOVE_PIECE:
            chosen_piece_index_to_move = get_valid_input(greeting + INSERT_PIECE_INDEX_TO_MOVE,
                                                         validate_input_of_piece_to_move,
                                                         self.get_all_pieces_positions())
            chosen_new_piece_place = get_valid_input(INSERT_PIECE_NEW_INDEX, validate_input_of_piece_new_place,
                                                     possible_actions, chosen_piece_index_to_move, empty_cells)
            return chosen_piece_index_to_move, chosen_new_piece_place

        elif type_of_required_action == MoveType.PLACE_PIECE:
            chosen_piece_placement_index = get_valid_input(greeting + CHOOSE_NEW_PIECE_PLACEMENT,
                                                           validate_input_of_new_piece_placement,
                                                           possible_actions)
            return chosen_piece_placement_index

        else:  # Case of remove piece of the opponent
            chosen_opponent_piece_index_to_remove = get_valid_input(greeting + CHOOSE_OPPONENT_PIECE_TO_REMOVE,
                                                                    validate_input_of_opponent_piece_removal,
                                                                    possible_actions)
            return chosen_opponent_piece_index_to_remove
