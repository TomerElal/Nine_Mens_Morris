import board
from move import Move


def convert_move_to_action(desired_move, piece_position):
    piece_row_position = piece_position[0]
    piece_col_position = piece_position[1]

    if desired_move == Move.UP:
        return convert_up_move_to_action(piece_col_position, piece_row_position)

    if desired_move == Move.DOWN:
        return convert_down_move_to_action(piece_col_position, piece_row_position)

    return convert_right_or_left_move_to_action(piece_col_position, piece_row_position, desired_move)


def convert_right_or_left_move_to_action(piece_col_position, piece_row_position, desired_move):
    return piece_row_position, piece_col_position + 1 if desired_move == Move.RIGHT else - 1


def convert_down_move_to_action(piece_col_position, piece_row_position):
    if piece_row_position == board.MIDDLE_ROW_LEFT_SIDE:
        addition_factor = 1 + board.NUM_OF_COLS - piece_col_position
        return piece_row_position + addition_factor, 0
    if piece_row_position == board.MIDDLE_ROW_RIGHT_SIDE:
        addition_factor = 1 + piece_col_position
        return piece_row_position + addition_factor, board.NUM_OF_COLS - 1
    return piece_row_position + 1, piece_col_position


def convert_up_move_to_action(piece_col_position, piece_row_position):
    if piece_row_position == board.MIDDLE_ROW_LEFT_SIDE:
        subtract_factor = board.NUM_OF_COLS - piece_col_position
        return piece_row_position - subtract_factor, 0
    if piece_row_position == board.MIDDLE_ROW_RIGHT_SIDE:
        subtract_factor = 2 + piece_col_position
        return piece_row_position - subtract_factor, board.NUM_OF_COLS - 1
    return piece_row_position - 1, piece_col_position
