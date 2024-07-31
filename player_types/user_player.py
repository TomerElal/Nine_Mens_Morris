from player import Player
from move import MoveType

INSERT_PIECE_INDEX_TO_MOVE = ("Choose a piece of yours to move.\nInsert it's index by the format [num_row][num_column]."
                              "\nFor example, if you want to move a piece that placed in row number 5 and"
                              " column number 2, insert:\n52")
INSERT_PIECE_NEW_INDEX = ("Choose a new place for your piece.\nInsert it's index by the format [num_row][num_column]."
                          "\nFor example, if you want to move a piece to a placed in row number 3 and"
                          " column number 1, insert:\n31")
CHOOSE_NEW_PIECE_PLACEMENT = (
    "Choose a placement for your piece.\nInsert it's index by the format [num_row][num_column]."
    "\nFor example, if you want to place the piece in row number 7 and column number 2, insert:\n72")
CHOOSE_OPPONENT_PIECE_TO_REMOVE = (
    "Choose an index of opponent's piece to remove.\nInsert the index by the format [num_row][num_column]."
    "\nFor example, if you want to remove a piece from row number 2 and column number 1, insert:\n21")


def get_valid_input(prompt, validation_func, validation_list, prev_input=None):
    while True:
        user_input = input(prompt)
        is_valid, result = validation_func(user_input, validation_list, prev_input)
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


def validate_input_of_piece_to_move(user_input, possible_move_actions, prev_input):
    if not index_format_is_valid(user_input):
        return False, "You have entered an invalid index format. Try again!"

    piece_index_to_move = tuple(user_input)
    all_existed_pieces_indexes = [action[0] for action in possible_move_actions]
    if piece_index_to_move in all_existed_pieces_indexes:
        return True, piece_index_to_move

    return False, "The index you've entered isn't valid. Try again!"


def validate_input_of_piece_new_place(user_input, possible_move_actions, index_to_move_from):
    if not index_format_is_valid(user_input):
        return False, "You have entered an invalid index format. Try again!"

    new_place_index = tuple(user_input)
    desired_action = (index_to_move_from, new_place_index)
    if desired_action in possible_move_actions:
        return True, new_place_index

    return False, "The index you've entered isn't valid. Try again!"


def validate_input_of_new_piece_placement(user_input, empty_cells_list, prev_input):
    if not index_format_is_valid(user_input):
        return False, "You have entered an invalid index format. Try again!"

    piece_placement_index = tuple(user_input)
    if piece_placement_index in empty_cells_list:
        return True, piece_placement_index

    return False, "The index you've entered isn't valid. Try again!"


def validate_input_of_opponent_piece_removal(user_input, opponent_cells_list, prev_input):
    if not index_format_is_valid(user_input):
        return False, "You have entered an invalid index format. Try again!"

    opponent_piece_removal_index = tuple(user_input)
    if opponent_piece_removal_index in opponent_cells_list:
        return True, opponent_piece_removal_index

    return False, "The index you've entered isn't valid. Try again!"


class UserPlayer(Player):

    def get_action(self, state, type_of_required_action=MoveType.MOVE_PIECE):

        if type_of_required_action == MoveType.MOVE_PIECE:
            possible_actions = self.get_possible_move_pieces_actions(game_state=state)
            chosen_piece_index_to_move = get_valid_input(INSERT_PIECE_INDEX_TO_MOVE,
                                                         validate_input_of_piece_to_move,
                                                         possible_actions)
            chosen_new_piece_place = get_valid_input(INSERT_PIECE_NEW_INDEX, validate_input_of_piece_new_place,
                                                     possible_actions, chosen_piece_index_to_move)
            return chosen_piece_index_to_move, chosen_new_piece_place

        elif type_of_required_action == MoveType.PLACE_PIECE:
            possible_piece_placements = self.get_possible_piece_placements(game_state=state)
            chosen_piece_placement_index = get_valid_input(INSERT_PIECE_INDEX_TO_MOVE,
                                                           validate_input_of_new_piece_placement,
                                                           possible_piece_placements)
            return chosen_piece_placement_index

        else:  # Case of remove piece of the opponent
            possible_remove_actions = self.get_possible_opponent_remove_pieces(game_state=state)
            chosen_opponent_piece_index_to_remove = get_valid_input(CHOOSE_OPPONENT_PIECE_TO_REMOVE,
                                                                    validate_input_of_opponent_piece_removal,
                                                                    possible_remove_actions)
            return chosen_opponent_piece_index_to_remove
