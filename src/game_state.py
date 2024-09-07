import copy

from colorama import Fore
from common import strings
from exceptions.piece_not_exist import PieceNotExistException
from src.move import Move, MoveType
from enum import Enum
from exceptions.uncorrelated_piece_color_exception import UnCorrelatedPieceColor
from src.piece import Piece
from common.utils import move_performed_a_mill, display_board

NUM_OF_ROWS = 8
NUM_OF_COLS = 3
MIDDLE_ROW_LEFT_SIDE = 3
MIDDLE_ROW_RIGHT_SIDE = 4


class CellState(Enum):
    EMPTY = 0
    BLUE = 1
    GREEN = 2
    BLACK = 3
    WHITE = 4

    @property
    def color(self):
        if self == CellState.BLUE:
            return Fore.LIGHTBLUE_EX
        elif self == CellState.GREEN:
            return Fore.LIGHTGREEN_EX
        elif self == CellState.WHITE:
            return Fore.LIGHTWHITE_EX
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
                              ([Move.DOWN] if i == 0 else [Move.UP]) +
                              ([Move.UP, Move.DOWN] if i == 1 else []))
    connections[(i, 1)] = vertical_poss_moves
    connections[((MIDDLE_ROW_RIGHT_SIDE + 1) + i, 1)] = vertical_poss_moves

    # Handle horizontal middle col.
    horizontal_poss_moves = set([Move.UP, Move.DOWN] +
                                ([Move.RIGHT] if i == 0 else [Move.LEFT]) +
                                ([Move.RIGHT, Move.LEFT] if i == 1 else []))
    connections[(MIDDLE_ROW_LEFT_SIDE, i)] = horizontal_poss_moves
    connections[(MIDDLE_ROW_RIGHT_SIDE, i)] = horizontal_poss_moves


def handle_board_connections_in_diagonals(connections, i):
    # Handle (top left corner to bottom right corner) diagonal cells.
    connections[(i, 0)] = {Move.RIGHT, Move.DOWN}
    connections[((NUM_OF_ROWS - 1) - i, 2)] = {Move.LEFT, Move.UP}

    # Handle (bottom left corner to top right corner) diagonal cells.
    connections[((NUM_OF_ROWS - 1) - i, 0)] = {Move.RIGHT, Move.UP}
    connections[(i, 2)] = {Move.LEFT, Move.DOWN}


def there_are_zero_pieces_left_to_place(player1, player2):
    return player1.num_of_pieces_left_to_place + player2.num_of_pieces_left_to_place == 0


class GameState:
    BOARD_CONNECTIONS = initialize_board_connections()

    def __init__(self, player1, player2, curr_move_type, existing_board=None, last_move=None, player_turn=1):
        self.move_type = curr_move_type
        self.player1 = player1
        self.player2 = player2
        self.board = existing_board if existing_board else initialize_board()
        self.last_move = last_move  # Store the last move
        self.curr_player_turn = player_turn

    def get_last_move(self):
        return self.last_move

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

    def generate_new_state_successor(self, player_number, action):

        prev_position, new_position = None, None
        copy_state = copy.deepcopy(self)
        next_move_type = self.move_type

        curr_player, other_player, player_color = self.decide_player_turn_when_generate_successor(copy_state,
                                                                                                  player_number)

        if self.move_type == MoveType.MOVE_PIECE:
            new_position, prev_position = self.move_piece_when_generate_successor(action, curr_player, player_color,
                                                                                  player_number)

        if self.move_type == MoveType.PLACE_PIECE:
            new_position, next_move_type = self.place_piece_when_generate_successor(action, copy_state, curr_player,
                                                                                    next_move_type,
                                                                                    other_player, player_color)

        if self.move_type == MoveType.REMOVE_OPPONENT_PIECE:
            next_move_type, prev_position = self.remove_opponent_piece_when_generate_successor(action, curr_player,
                                                                                               other_player)
        new_state = GameState(copy_state.player1, copy_state.player2, next_move_type, existing_board=copy_state.board,
                              last_move=action, player_turn=3 - copy_state.curr_player_turn)
        new_state.update_board(prev_position, new_position, player_color)

        self.handle_new_mill_situation_after_generate_successor(curr_player, new_position, new_state, player_color)

        return new_state

    def handle_new_mill_situation_after_generate_successor(self, curr_player, new_position, new_state, player_color):
        if new_position and move_performed_a_mill(new_position, new_state, player_color):
            new_state.move_type = MoveType.REMOVE_OPPONENT_PIECE
            curr_player.move_type = MoveType.REMOVE_OPPONENT_PIECE
            new_state.curr_player_turn = 3 - new_state.curr_player_turn

    def remove_opponent_piece_when_generate_successor(self, action, curr_player, other_player):
        prev_position = action
        if not other_player.remove_piece(prev_position):
            raise PieceNotExistException(strings.PLAYER_REMOVE_ERROR_TEMPLATE.format(
                name=curr_player.name,
                location=prev_position
            ))
        next_move_type = curr_player.move_type = MoveType.MOVE_PIECE \
            if there_are_zero_pieces_left_to_place(curr_player, other_player) else MoveType.PLACE_PIECE
        return next_move_type, prev_position

    def place_piece_when_generate_successor(self, action, copy_state, curr_player, next_move_type,
                                            other_player, player_color):
        new_position = action
        player_new_piece = Piece(player_color, new_position,
                                 self.BOARD_CONNECTIONS[new_position])
        curr_player.add_piece(player_new_piece)
        if there_are_zero_pieces_left_to_place(curr_player, other_player):
            next_move_type = copy_state.player1.move_type = copy_state.player2.move_type = MoveType.MOVE_PIECE
        return new_position, next_move_type

    def move_piece_when_generate_successor(self, action, curr_player, player_color, player_number):
        try:
            prev_position, new_position = action[0], action[1]
        except Exception as e:
            raise Exception(e)
        if self.board[prev_position[0]][prev_position[1]] != player_color:
            display_board(self.board)
            self.get_legal_actions(player_number)
            raise UnCorrelatedPieceColor(strings.UNCORRELATED_PIECE_COLOR_ERROR_TEMPLATE.format(
                player_name=curr_player.name,
                player_color=player_color.name,
                prev_row=prev_position[0],
                prev_col=prev_position[1],
                actual_color=(self.board[prev_position[0]][prev_position[1]]).name
            ))
        curr_player.handle_piece_movement_action(prev_position, new_position, self.BOARD_CONNECTIONS[new_position])
        return new_position, prev_position

    def decide_player_turn_when_generate_successor(self, copy_state, player_number):
        if player_number == 1:
            curr_player = copy_state.player1
            other_player = copy_state.player2
        else:
            curr_player = copy_state.player2
            other_player = copy_state.player1
        player_color = curr_player.get_player_color()
        return curr_player, other_player, player_color

    def get_cell_state(self, location):
        return self.board[location[0]][location[1]]

    def set_cell_state(self, location, new_state):
        self.board[location[0]][location[1]] = new_state

    def is_game_over(self):
        return (self.player1.is_lost_game(self, self.move_type)
                or
                self.player2.is_lost_game(self, self.move_type))

    def get_legal_actions(self, player_number):
        if player_number == 1:
            return self.player1.get_possible_actions(self, self.move_type)
        return self.player2.get_possible_actions(self, self.move_type)

    def get_opponent_legal_actions(self, player_color):
        action_type = MoveType.MOVE_PIECE if (self.player1.num_of_pieces_left_to_place +
                                              self.player2.num_of_pieces_left_to_place == 0) \
            else MoveType.PLACE_PIECE
        if player_color == self.player1.get_player_color():
            return self.player2.get_possible_actions(self, action_type)
        return self.player1.get_possible_actions(self, action_type)

    def get_curr_player_color(self):
        if self.curr_player_turn == 1:
            return self.player1.get_player_color()
        return self.player2.get_player_color()

    def get_opponent_color(self):
        if self.curr_player_turn == 1:
            return self.player2.get_player_color()
        return self.player1.get_player_color()

    def get_player_move_type(self, player_number):
        if player_number == 1:
            return self.player1.move_type
        return self.player2.move_type

    def get_player_number(self, player_color):
        if player_color == self.player1.get_player_color():
            return 1
        return 2
