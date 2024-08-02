from player import Player
from move import MoveType
from colorama import Style, Fore

SEPERATOR = "\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n"

INSERT_PIECE_INDEX_TO_MOVE = ("Choose a piece of yours to move.\nInsert it's index by the format [num_row][num_column]."
                              "\nFor example, if you want to move a piece that placed in row number 5 and"
                              " column number 2, insert: 52\n📝️ Your Choice 👉🏻:  ")
INSERT_PIECE_NEW_INDEX = (SEPERATOR + Fore.LIGHTMAGENTA_EX +
                          "Now choose a new place for your piece."
                          + Style.RESET_ALL + SEPERATOR +
                          "Insert it's index by the format [num_row][num_column]."
                          "\nFor example, if you want to move a piece to a placed in row number 3 and"
                          " column number 1, insert: 31\n📝️ Your Choice 👉🏻:  ")
CHOOSE_NEW_PIECE_PLACEMENT = (
    "Choose a placement for your piece.\nInsert it's index by the format [num_row][num_column]."
    "\nFor example, if you want to place the piece in row number 7 and column number 2, insert: 72\n"
    "📝️ Your Choice 👉🏻:  ")
CHOOSE_OPPONENT_PIECE_TO_REMOVE = (SEPERATOR + Fore.LIGHTYELLOW_EX +
                                   "🚀🚀 Choose an index of opponent's piece to remove! 🚀🚀"
                                   + Style.RESET_ALL + SEPERATOR +
                                   "Insert the index by the format [num_row][num_column]."
                                   "\nFor example, if you want to remove a piece from row number 2 and"
                                   " column number 1, insert: 21\n📝️ Your Choice 👉🏻:  ")
INVALID_INPUT_FORMAT = (SEPERATOR + Fore.LIGHTCYAN_EX + "You have entered an invalid index format. Try again!" +
                        Style.RESET_ALL + SEPERATOR)
INVALID_INDEX = (SEPERATOR + Fore.LIGHTCYAN_EX + "The index you've entered is invalid. Try again!" +
                 Style.RESET_ALL + SEPERATOR)


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
    all_existed_pieces_indexes = set([action[0] for action in possible_move_actions])
    if piece_index_to_move in all_existed_pieces_indexes:
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


class UserPlayer(Player):

    def get_action(self, state, type_of_required_action=MoveType.MOVE_PIECE):

        possible_actions = self.get_possible_actions(state, type_of_required_action)
        greeting = self.player_color.color + f"\n{self.name} " + Style.RESET_ALL + "it's your turn ! 😎\n"
        empty_cells = state.get_empty_cells()
        if type_of_required_action == MoveType.MOVE_PIECE:
            chosen_piece_index_to_move = get_valid_input(greeting + INSERT_PIECE_INDEX_TO_MOVE,
                                                         validate_input_of_piece_to_move,
                                                         possible_actions)
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
