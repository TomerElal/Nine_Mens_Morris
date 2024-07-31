import utils

from move import MoveType
from abc import ABC, abstractmethod
from exceptions.game_phase_exception import GamePhaseException
from game_state import NUM_OF_ROWS, NUM_OF_COLS, CellState

MOVING_PIECES_PHASE_ERROR = "The game is the moving pieces phase"


class Player(ABC):
    def __init__(self, name, initial_num_of_pieces, player_color):
        self.player_color = player_color
        self.name = name
        self.pieces_on_board = []
        self.curr_move_type = MoveType.PLACE_PIECE
        self.num_of_pieces_left_to_place = initial_num_of_pieces

    @abstractmethod
    def get_action(self, state, phase_number=2):
        raise NotImplementedError()

    def get_num_of_pieces_on_board(self):
        return len(self.pieces_on_board)

    def get_possible_move_pieces_actions(self, game_state):
        if not self.curr_move_type == MoveType.MOVE_PIECE:
            raise GamePhaseException(f"The current move type is to {self.curr_move_type.name}"
                                     f" and the player {self.name} tried to move his piece")

        all_possible_actions = []
        for piece in self.pieces_on_board:
            curr_piece_poss_moves = piece.get_possible_moves(state=game_state)
            for move in curr_piece_poss_moves:
                correlated_action = utils.convert_move_to_action(desired_move=move, piece_position=piece.position)
                all_possible_actions.append(correlated_action)
        return all_possible_actions

    def get_possible_opponent_remove_pieces(self, game_state):
        if not self.curr_move_type == MoveType.PLACE_PIECE:
            raise GamePhaseException(f"The current move type is to {self.curr_move_type.name}"
                                     f" and the player {self.name} tried to remove opponent's piece")

        opponent_cells = []
        for row in range(NUM_OF_ROWS):
            for col in range(NUM_OF_COLS):
                curr_cell = game_state[row][col]
                if curr_cell != CellState.EMPTY and curr_cell != self.player_color:
                    opponent_cells.append((row, col))
        return opponent_cells

    def get_possible_piece_placements(self, game_state):
        if not self.curr_move_type == MoveType.PLACE_PIECE:
            raise GamePhaseException(f"The current move type is to {self.curr_move_type.name}"
                                     f" and the player {self.name} tried to place a new piece")

        return game_state.get_empty_cells()
