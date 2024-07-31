from enum import Enum
from colorama import Fore
from move import Move
import board


class PieceColor(Enum):
    EMPTY = 0
    BLUE = 1
    GREEN = 2

    @property
    def color(self):
        if self == PieceColor.BLUE:
            return Fore.LIGHTBLUE_EX
        elif self == PieceColor.GREEN:
            return Fore.LIGHTGREEN_EX
        else:
            return Fore.LIGHTBLACK_EX


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
                state[piece_row_index - 1][piece_col_index] == PieceColor.EMPTY):
            possible_moves.append(Move.UP)

        if (Move.DOWN in self.connections_in_board and piece_row_index < board.NUM_OF_ROWS and
                state[piece_row_index + 1][piece_col_index] == PieceColor.EMPTY):
            possible_moves.append(Move.DOWN)

        if (Move.RIGHT in self.connections_in_board and piece_col_index < board.NUM_OF_COLS and
                state[piece_col_index][piece_col_index + 1] == PieceColor.EMPTY):
            possible_moves.append(Move.RIGHT)

        if (Move.LEFT in self.connections_in_board and piece_col_index < 0 and
                state[piece_col_index][piece_col_index - 1] == PieceColor.EMPTY):
            possible_moves.append(Move.LEFT)

        return possible_moves



