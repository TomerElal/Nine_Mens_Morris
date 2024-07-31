import copy

from colorama import Style, Fore
from move import Move, MoveType
from enum import Enum
from exceptions.uncorrelated_piece_color_exception import UnCorrelatedPieceColor

NUM_OF_ROWS = 8
NUM_OF_COLS = 3
MIDDLE_ROW_LEFT_SIDE = 3
MIDDLE_ROW_RIGHT_SIDE = 4


class CellState(Enum):
    EMPTY = 0
    BLUE = 1
    GREEN = 2

    @property
    def color(self):
        if self == CellState.BLUE:
            return Fore.LIGHTBLUE_EX
        elif self == CellState.GREEN:
            return Fore.LIGHTGREEN_EX
        else:
            return Fore.LIGHTBLACK_EX


def initialize_board():
    return [[CellState.EMPTY for _ in range(NUM_OF_COLS)] for _ in range(NUM_OF_ROWS)]


def initialize_board_connections():
    connections = dict()

    for i in range((NUM_OF_ROWS // 2) - 1):
        handle_board_connections_in_diagonals(connections, i)
        handle_board_connections_in_middle_row_col(connections, i)

    return connections


def handle_board_connections_in_middle_row_col(connections, i):
    # Handle vertical middle row.
    vertical_poss_moves = set([Move.RIGHT, Move.LEFT] +
                              [Move.DOWN] if i == 0 else [Move.UP] +
                                                         [Move.UP, Move.DOWN] if i == 1 else [])
    connections[(i, 1)] = vertical_poss_moves
    connections[((MIDDLE_ROW_RIGHT_SIDE + 1) + i, 1)] = vertical_poss_moves

    # Handle horizontal middle col.
    horizontal_poss_moves = set([Move.UP, Move.DOWN] +
                                [Move.RIGHT] if i == 0 else [Move.LEFT] +
                                                            [Move.RIGHT, Move.LEFT] if i == 1 else [])
    connections[(MIDDLE_ROW_LEFT_SIDE, i)] = horizontal_poss_moves
    connections[(MIDDLE_ROW_RIGHT_SIDE, i)] = horizontal_poss_moves


def handle_board_connections_in_diagonals(connections, i):
    # Handle (top left corner to bottom right corner) diagonal cells.
    connections[(i, 0)] = {Move.RIGHT, Move.DOWN}
    connections[((NUM_OF_COLS - 1) - i, 2)] = {Move.LEFT, Move.UP}

    # Handle (bottom left corner to top right corner) diagonal cells.
    connections[((NUM_OF_COLS - 1) - i, 0)] = {Move.RIGHT, Move.UP}
    connections[(i, 2)] = {Move.LEFT, Move.DOWN}


class GameState:
    BOARD_CONNECTIONS = initialize_board_connections()

    def __init__(self, existing_board=None):
        self.board = existing_board if existing_board else initialize_board()

    def display_board(self):
        # Create a visual representation of the Nine Men's Morris board
        visual_board = self.board
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

    def get_empty_cells(self):
        empty_cells = []
        for row in range(NUM_OF_ROWS):
            for col in range(NUM_OF_COLS):
                if self.board[row][col] == CellState.EMPTY:
                    empty_cells.append((row, col))
        return empty_cells

    def update_board(self, prev_position=None, new_position=None, piece_color=CellState.EMPTY):
        if prev_position:
            self.board[prev_position[0]][prev_position[1]] = CellState.EMPTY
        if new_position:
            self.board[new_position[0]][new_position[1]] = piece_color
        self.display_board()

    def generate_new_state_successor(self, action, piece_color, action_type=MoveType.MOVE_PIECE):

        prev_position, new_position = None, None

        if action_type == MoveType.MOVE_PIECE:
            prev_position, new_position = action[0], action[1]
            if self.board[prev_position[0]][prev_position[1]] != piece_color:
                raise UnCorrelatedPieceColor()

        if action_type == MoveType.PLACE_PIECE:
            new_position = action

        if action_type == MoveType.REMOVE_OPPONENT_PIECE:
            prev_position = action

        copy_current_board = copy.deepcopy(self.board)
        new_state = GameState(existing_board=copy_current_board)
        new_state.update_board(prev_position, new_position, piece_color)
        return new_state


# Example usage
if __name__ == "__main__":
    board = GameState()
    board.display_board()
    print(board.board)
    board.update_board((0, 0), (0, 1), CellState.BLUE)
    board.update_board((0, 0), (1, 1), CellState.GREEN)
