import utils

from move import MoveType
from abc import ABC, abstractmethod
from exceptions.game_phase_exception import GamePhaseException
from exceptions.piece_not_exist import PieceNotExistException
from game_state import NUM_OF_ROWS, NUM_OF_COLS, CellState


class Player(ABC):
    def __init__(self, name, initial_num_of_pieces, player_color):
        self.player_color = player_color
        self.name = name
        self.pieces_on_board = set()
        self.move_type = MoveType.PLACE_PIECE
        self.num_of_pieces_left_to_place = initial_num_of_pieces

    @abstractmethod
    def get_action(self, state, move_type=MoveType.MOVE_PIECE):
        raise NotImplementedError()

    def get_num_of_pieces_on_board(self):
        return len(self.pieces_on_board)

    def get_player_color(self):
        return self.player_color

    def get_piece_by_position(self, position_of_desired_piece):
        for piece in self.pieces_on_board:
            if piece.position == position_of_desired_piece:
                return piece
        raise PieceNotExistException(f"Couldn't find a piece with the specified location {position_of_desired_piece}")

    def add_piece(self, piece):
        self.num_of_pieces_left_to_place -= 1
        self.pieces_on_board.add(piece)

    def move_piece(self, position_of_desired_piece_to_move, new_position, new_connections):
        desired_piece = self.get_piece_by_position(position_of_desired_piece_to_move)
        if desired_piece:
            desired_piece.move_piece(new_position, new_connections)
            return True
        return False  # Means there isn't a piece with the specified location.

    def remove_piece(self, position_of_desired_piece_to_remove):
        desired_piece = self.get_piece_by_position(position_of_desired_piece_to_remove)
        if desired_piece:
            desired_piece.remove_piece()
            self.pieces_on_board.remove(desired_piece)
            return True
        return False  # Means there isn't a piece with the specified location.

    def is_lost_game(self, state, action_type=MoveType.MOVE_PIECE):
        return (
                (self.num_of_pieces_left_to_place == 0 and len(self.pieces_on_board) < 3)
                or
                (action_type == MoveType.MOVE_PIECE and len(self.get_possible_actions(state, action_type)) == 0)
        )

    def get_possible_actions(self, state, desired_action_type=MoveType.MOVE_PIECE):

        if desired_action_type == MoveType.PLACE_PIECE:
            return self.get_possible_piece_placements(state)
        if desired_action_type == MoveType.MOVE_PIECE:
            return self.get_possible_move_pieces_actions(state)
        if desired_action_type == MoveType.REMOVE_OPPONENT_PIECE:
            return self.get_possible_opponent_remove_pieces(state)

    def get_possible_move_pieces_actions(self, game_state):
        if not self.move_type == MoveType.MOVE_PIECE:
            print(game_state.player1.name + " got " + str(game_state.player1.num_of_pieces_left_to_place) + " pieces left to place")
            print(game_state.player2.name + " got " + str(game_state.player2.num_of_pieces_left_to_place) + " pieces left to place")
            raise GamePhaseException(f"The current move type is to {self.move_type.name}"
                                     f" and the player {self.name} tried to move his piece")

        all_possible_actions = []
        for piece in self.pieces_on_board:
            curr_piece_poss_moves = piece.get_possible_moves(state=game_state)
            for move in curr_piece_poss_moves:
                correlated_action = utils.convert_move_to_action(desired_move=move, piece_position=piece.position)
                all_possible_actions.append((piece.position, correlated_action))
        return all_possible_actions

    def get_possible_opponent_remove_pieces(self, game_state):
        if not self.move_type == MoveType.REMOVE_OPPONENT_PIECE:
            raise GamePhaseException(f"The current move type is to {self.move_type.name}"
                                     f" and {self.name} tried to remove opponent's piece")

        opponent_cells = []
        for row in range(NUM_OF_ROWS):
            for col in range(NUM_OF_COLS):
                curr_cell = game_state.board[row][col]
                if curr_cell != CellState.EMPTY and curr_cell != self.player_color:
                    opponent_cells.append((row, col))
        return opponent_cells

    def get_possible_piece_placements(self, game_state):
        if not self.move_type == MoveType.PLACE_PIECE:
            raise GamePhaseException(f"The current move type is to {self.move_type.name}"
                                     f" and {self.name} tried to place a new piece")

        return game_state.get_empty_cells()
