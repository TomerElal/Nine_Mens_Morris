from move import Move

import game_state


class Piece:
    def __init__(self, color, position, connections):
        self.color = color
        self.position = position
        self.connections_in_board = connections

    def move_piece(self, new_position):
        self.position = new_position

    def remove_piece(self):
        self.position = None

    def get_possible_moves(self, state):
        possible_moves = []
        piece_row_index = self.position[0]
        piece_col_index = self.position[1]

        if (Move.UP in self.connections_in_board and piece_row_index > 0 and
                state[piece_row_index - 1][piece_col_index] == game_state.CellState.EMPTY):
            possible_moves.append(Move.UP)

        if (Move.DOWN in self.connections_in_board and piece_row_index < game_state.NUM_OF_ROWS and
                state[piece_row_index + 1][piece_col_index] == game_state.CellState.EMPTY):
            possible_moves.append(Move.DOWN)

        if (Move.RIGHT in self.connections_in_board and piece_col_index < game_state.NUM_OF_COLS and
                state[piece_col_index][piece_col_index + 1] == game_state.CellState.EMPTY):
            possible_moves.append(Move.RIGHT)

        if (Move.LEFT in self.connections_in_board and piece_col_index < 0 and
                state[piece_col_index][piece_col_index - 1] == game_state.CellState.EMPTY):
            possible_moves.append(Move.LEFT)

        return possible_moves
