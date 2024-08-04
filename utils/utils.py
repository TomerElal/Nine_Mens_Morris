import time

from src import game_state
from src.move import Move
from utils.strings import *

WINDOW_SIZE = (1000, 700)

# Board dimensions
BOARD_SIZE = 600
BOARD_OFFSET_X = (WINDOW_SIZE[0] - BOARD_SIZE) // 2
BOARD_OFFSET_Y = (WINDOW_SIZE[1] - BOARD_SIZE) // 2
POSITIONS = [
    [(BOARD_OFFSET_X, BOARD_OFFSET_Y), (BOARD_OFFSET_X + 300, BOARD_OFFSET_Y), (BOARD_OFFSET_X + 600, BOARD_OFFSET_Y)],
    [(BOARD_OFFSET_X + 100, BOARD_OFFSET_Y + 100), (BOARD_OFFSET_X + 300, BOARD_OFFSET_Y + 100),
     (BOARD_OFFSET_X + 500, BOARD_OFFSET_Y + 100)],
    [(BOARD_OFFSET_X + 200, BOARD_OFFSET_Y + 200), (BOARD_OFFSET_X + 300, BOARD_OFFSET_Y + 200),
     (BOARD_OFFSET_X + 400, BOARD_OFFSET_Y + 200)],
    [(BOARD_OFFSET_X, BOARD_OFFSET_Y + 300), (BOARD_OFFSET_X + 100, BOARD_OFFSET_Y + 300),
     (BOARD_OFFSET_X + 200, BOARD_OFFSET_Y + 300)],
    [(BOARD_OFFSET_X + 400, BOARD_OFFSET_Y + 300), (BOARD_OFFSET_X + 500, BOARD_OFFSET_Y + 300),
     (BOARD_OFFSET_X + 600, BOARD_OFFSET_Y + 300)],
    [(BOARD_OFFSET_X + 200, BOARD_OFFSET_Y + 400), (BOARD_OFFSET_X + 300, BOARD_OFFSET_Y + 400),
     (BOARD_OFFSET_X + 400, BOARD_OFFSET_Y + 400)],
    [(BOARD_OFFSET_X + 100, BOARD_OFFSET_Y + 500), (BOARD_OFFSET_X + 300, BOARD_OFFSET_Y + 500),
     (BOARD_OFFSET_X + 500, BOARD_OFFSET_Y + 500)],
    [(BOARD_OFFSET_X, BOARD_OFFSET_Y + 600), (BOARD_OFFSET_X + 300, BOARD_OFFSET_Y + 600),
     (BOARD_OFFSET_X + 600, BOARD_OFFSET_Y + 600)]
]


def convert_move_to_action(desired_move, piece_position):
    piece_row_position = piece_position[0]
    piece_col_position = piece_position[1]

    if desired_move == Move.UP or desired_move == Move.DOWN:
        return compute_adjacent_cell_pos(piece_position, desired_move)

    return convert_right_or_left_move_to_action(piece_col_position, piece_row_position, desired_move)


def convert_right_or_left_move_to_action(piece_col_position, piece_row_position, desired_move):
    return piece_row_position, piece_col_position + (1 if desired_move == Move.RIGHT else - 1)


def move_performed_a_mill(piece_new_location, state, player_color):
    board_connections = game_state.GameState.BOARD_CONNECTIONS
    moved_piece_connections = board_connections[piece_new_location]

    return (
            check_mill_horizontal(board_connections, moved_piece_connections, piece_new_location, player_color, state)
            or
            check_mill_vertical(board_connections, moved_piece_connections, piece_new_location, player_color, state)
    )


def check_mill_horizontal(board_connections, moved_piece_connections, piece_new_location, player_color, state):
    # Check mill horizontally.
    return (
            mill_from_right_or_middle(board_connections, moved_piece_connections, piece_new_location, player_color,
                                      state)
            or
            mill_from_left(board_connections, moved_piece_connections, piece_new_location, player_color, state)
    )


def mill_from_right_or_middle(board_connections, moved_piece_connections, piece_new_location, player_color, state):
    # Cases where the moved piece is at the right or at the middle of the mill (if existed).
    if Move.LEFT in moved_piece_connections:
        location_of_one_cell_from_left = (piece_new_location[0], piece_new_location[1] - 1)
        if state.get_cell_state(location_of_one_cell_from_left) == player_color:
            one_cell_from_left_connections = board_connections[location_of_one_cell_from_left]

            # Case where the moved piece is at the most right side of the row.
            if Move.LEFT in one_cell_from_left_connections:
                location_of_two_cells_from_left = (location_of_one_cell_from_left[0],
                                                   location_of_one_cell_from_left[1] - 1)
                if state.get_cell_state(location_of_two_cells_from_left) == player_color:
                    return True

            # Case where the moved piece is at the middle of the row.
            if Move.RIGHT in moved_piece_connections:
                location_of_one_cell_from_right = (piece_new_location[0], piece_new_location[1] + 1)
                if state.get_cell_state(location_of_one_cell_from_right) == player_color:
                    return True
    return False


def mill_from_left(board_connections, moved_piece_connections, piece_new_location, player_color, state):
    # Case where the moved piece is at the most left side of the row (if existed).
    if Move.RIGHT in moved_piece_connections:
        location_of_one_cell_from_right = (piece_new_location[0], piece_new_location[1] + 1)
        if state.get_cell_state(location_of_one_cell_from_right) == player_color:
            one_cell_from_right_connections = board_connections[location_of_one_cell_from_right]
            if Move.RIGHT in one_cell_from_right_connections:
                location_of_two_cells_from_right = (location_of_one_cell_from_right[0],
                                                    location_of_one_cell_from_right[1] + 1)
                if state.get_cell_state(location_of_two_cells_from_right) == player_color:
                    return True
    return False


def check_mill_vertical(board_connections, moved_piece_connections, piece_new_location, player_color, state):
    # Check mill vertically.
    return (
            mill_from_bottom_or_middle(board_connections, moved_piece_connections, piece_new_location, player_color,
                                       state)
            or
            mill_from_top(board_connections, moved_piece_connections, piece_new_location, player_color, state))


def mill_from_bottom_or_middle(board_connections, moved_piece_connections, piece_new_location, player_color, state):
    # Cases where the moved piece is at the bottom or at the middle of the mill (if existed).
    if Move.UP in moved_piece_connections:
        one_cell_above_location = compute_adjacent_cell_pos(piece_new_location)
        if state.get_cell_state(one_cell_above_location) == player_color:
            one_cell_above_connections = board_connections[one_cell_above_location]

            # Case where the moved piece is at the bottom.
            if Move.UP in one_cell_above_connections:
                two_cells_above_location = compute_adjacent_cell_pos(one_cell_above_location)
                if state.get_cell_state(two_cells_above_location) == player_color:
                    return True

            # Case where the moved piece is at the middle.
            if Move.DOWN in moved_piece_connections:
                one_cell_bellow_location = compute_adjacent_cell_pos(piece_new_location, Move.DOWN)
                if state.get_cell_state(one_cell_bellow_location) == player_color:
                    return True
    return False


def mill_from_top(board_connections, moved_piece_connections, piece_new_location, player_color, state):
    # Case where the moved piece is at the top of the mill (if existed).
    if Move.DOWN in moved_piece_connections:
        one_cell_bellow_location = compute_adjacent_cell_pos(piece_new_location, Move.DOWN)
        if state.get_cell_state(one_cell_bellow_location) == player_color:
            one_cell_bellow_connections = board_connections[one_cell_bellow_location]
            if Move.DOWN in one_cell_bellow_connections:
                two_cells_bellow_location = compute_adjacent_cell_pos(one_cell_bellow_location, Move.DOWN)
                if state.get_cell_state(two_cells_bellow_location) == player_color:
                    return True
    return False


def compute_adjacent_cell_pos(given_location, direction=Move.UP):
    if direction == Move.UP:
        if given_location[0] == 3:
            return given_location[1], 0
        if given_location[0] == 4:
            return (game_state.NUM_OF_COLS - 1) - given_location[1], game_state.NUM_OF_COLS - 1
        if given_location[0] in [5, 6, 7] and given_location[1] != 1:
            row = game_state.MIDDLE_ROW_LEFT_SIDE if given_location[1] == 0 else game_state.MIDDLE_ROW_RIGHT_SIDE
            col = abs(((game_state.NUM_OF_ROWS - 1) - given_location[0]) - given_location[1])
            return row, col
        return given_location[0] - 1, given_location[1]
    else:
        if given_location[0] in [0, 1, 2] and given_location[1] != 1:
            row = game_state.MIDDLE_ROW_LEFT_SIDE if given_location[1] == 0 else game_state.MIDDLE_ROW_RIGHT_SIDE
            col = abs(given_location[0] - given_location[1])
            return row, col
        if given_location[0] == 3:
            return (game_state.NUM_OF_ROWS - 1) - given_location[1], 0
        if given_location[0] == 4:
            return 5 + given_location[1], game_state.NUM_OF_COLS - 1
        return given_location[0] + 1, given_location[1]


def display_board(visual_board):
    # Create a visual representation of the Nine Men's Morris board
    print()
    print("#####################################################################################################")
    print()
    # Display the board with connections
    print(
        f"{visual_board[0][0].color}{visual_board[0][0].name[0]}{Style.RESET_ALL}---------------{visual_board[0][1].color}{visual_board[0][1].name[0]}{Style.RESET_ALL}---------------{visual_board[0][2].color}{visual_board[0][2].name[0]}{Style.RESET_ALL}")
    print(f"|               |               |")
    print(
        f"|   {visual_board[1][0].color}{visual_board[1][0].name[0]}{Style.RESET_ALL}-----------{visual_board[1][1].color}{visual_board[1][1].name[0]}{Style.RESET_ALL}-----------{visual_board[1][2].color}{visual_board[1][2].name[0]}{Style.RESET_ALL}   |")
    print(f"|   |           |           |   |")
    print(
        f"|   |   {visual_board[2][0].color}{visual_board[2][0].name[0]}{Style.RESET_ALL}-------{visual_board[2][1].color}{visual_board[2][1].name[0]}{Style.RESET_ALL}-------{visual_board[2][2].color}{visual_board[2][2].name[0]}{Style.RESET_ALL}   |   |")
    print(f"|   |   |               |   |   |")
    print(
        f"{visual_board[3][0].color}{visual_board[3][0].name[0]}{Style.RESET_ALL}---{visual_board[3][1].color}{visual_board[3][1].name[0]}{Style.RESET_ALL}---{visual_board[3][2].color}{visual_board[3][2].name[0]}{Style.RESET_ALL}               {visual_board[4][0].color}{visual_board[4][0].name[0]}{Style.RESET_ALL}---{visual_board[4][1].color}{visual_board[4][1].name[0]}{Style.RESET_ALL}---{visual_board[4][2].color}{visual_board[4][2].name[0]}{Style.RESET_ALL}")
    print(f"|   |   |               |   |   |")
    print(
        f"|   |   {visual_board[5][0].color}{visual_board[5][0].name[0]}{Style.RESET_ALL}-------{visual_board[5][1].color}{visual_board[5][1].name[0]}{Style.RESET_ALL}-------{visual_board[5][2].color}{visual_board[5][2].name[0]}{Style.RESET_ALL}   |   |")
    print(f"|   |           |           |   |")
    print(
        f"|   {visual_board[6][0].color}{visual_board[6][0].name[0]}{Style.RESET_ALL}-----------{visual_board[6][1].color}{visual_board[6][1].name[0]}{Style.RESET_ALL}-----------{visual_board[6][2].color}{visual_board[6][2].name[0]}{Style.RESET_ALL}   |")
    print(f"|               |               |")
    print(
        f"{visual_board[7][0].color}{visual_board[7][0].name[0]}{Style.RESET_ALL}---------------{visual_board[7][1].color}{visual_board[7][1].name[0]}{Style.RESET_ALL}---------------{visual_board[7][2].color}{visual_board[7][2].name[0]}{Style.RESET_ALL}")


def perform_placement_or_remove_action_to_console(action_type_string, player, player_made_action_string, result):
    print_and_sleep(to_print=action_type_string.format(player_name=player))
    print_result = (player_made_action_string.format(player_name=player) + str(result) + Style.RESET_ALL + SEPERATOR)
    return print_result


def perform_move_action_to_console(action_type_string, player, player_made_action_string, result):
    print_and_sleep(to_print=action_type_string.format(player_name=player))
    print_result = (player_made_action_string.format(player_name=player) + str(result[0])
                    + TO_LOCATION + str(result[1]) + Style.RESET_ALL + SEPERATOR)
    return print_result


def print_and_sleep(to_print):
    print(to_print)
    time.sleep(TIME_TO_SLEEP)


def convert_piece_moves_to_player_actions(moves, piece_position=None):
    actions = []
    for move in moves:
        correlated_action = convert_move_to_action(desired_move=move, piece_position=piece_position)
        actions.append((piece_position, correlated_action))

    return actions


def get_piece_position_in_gui(row, col):
    return POSITIONS[row][col]
