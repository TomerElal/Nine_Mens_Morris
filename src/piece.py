from src import game_state

from src.move import Move
from utils.utils import compute_adjacent_cell_pos


class Piece:
    def __init__(self, color, position, connections):
        self.color = color
        self.position = position
        self.connections_in_board = connections

    def move_piece(self, new_position, new_connections):
        self.position = new_position
        self.connections_in_board = new_connections

    def remove_piece(self):
        self.position = None
        self.connections_in_board = None

    def get_possible_moves(self, state):
        possible_moves = []
        piece_row_index = self.position[0]
        piece_col_index = self.position[1]

        if (Move.UP in self.connections_in_board and piece_row_index > 0 and
                state.get_cell_state(compute_adjacent_cell_pos(self.position)) == game_state.CellState.EMPTY):
            possible_moves.append(Move.UP)

        if (Move.DOWN in self.connections_in_board and piece_row_index < game_state.NUM_OF_ROWS and
                state.get_cell_state(compute_adjacent_cell_pos(self.position, Move.DOWN)) == game_state.CellState.EMPTY):
            possible_moves.append(Move.DOWN)

        if (Move.RIGHT in self.connections_in_board and piece_col_index < game_state.NUM_OF_COLS and
                state.get_cell_state((piece_row_index, piece_col_index + 1)) == game_state.CellState.EMPTY):
            possible_moves.append(Move.RIGHT)

        if (Move.LEFT in self.connections_in_board and piece_col_index > 0 and
                state.get_cell_state((piece_row_index, piece_col_index - 1)) == game_state.CellState.EMPTY):
            possible_moves.append(Move.LEFT)

        return possible_moves
