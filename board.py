from piece import PieceColor
from colorama import Style
from move import Move

NUM_OF_ROWS = 8
NUM_OF_COLS = 3
MIDDLE_ROW_LEFT_SIDE = 3
MIDDLE_ROW_RIGHT_SIDE = 4


def initialize_board():
    return [[PieceColor.EMPTY for _ in range(NUM_OF_COLS)] for _ in range(NUM_OF_ROWS)]


def initialize_board_connections():
    connections = dict()

    for i in range((NUM_OF_ROWS // 2) - 1):
        handle_board_connections_in_diagonals(connections, i)
        handle_board_connections_in_middle_row_col(connections, i)


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


class Board:
    def __init__(self):
        self.board = initialize_board()
        self.board_connections = initialize_board_connections()

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

    def update_board(self, prev_position, new_position, piece_color):
        # Update the board with the given move
        self.board[prev_position[0]][prev_position[1]] = PieceColor.EMPTY
        self.board[new_position[0]][new_position[1]] = piece_color
        self.display_board()


# Example usage
if __name__ == "__main__":
    board = Board()
    board.display_board()
    board.update_board((0, 0), (0, 1), PieceColor.BLUE)
    board.update_board((0, 0), (1, 1), PieceColor.GREEN)
