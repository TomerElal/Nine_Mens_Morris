import game_state
from move import Move


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
