from utils import utils, strings

from src.move import MoveType
from abc import ABC, abstractmethod
from exceptions.game_phase_exception import GamePhaseException
from exceptions.piece_not_exist import PieceNotExistException
from src.game_state import NUM_OF_ROWS, NUM_OF_COLS, CellState


class Player(ABC):
    def __init__(self, name, initial_num_of_pieces, player_color, is_computer_player, is_gui_game=False):
        self.is_gui_game = is_gui_game
        self.is_computer_player = is_computer_player
        self.player_color = player_color
        self.name = name
        self.pieces_on_board = set()
        self.move_type = MoveType.PLACE_PIECE
        self.num_of_pieces_left_to_place = initial_num_of_pieces

    @abstractmethod
    def get_action(self, state, move_type):
        raise NotImplementedError()

    def get_num_of_pieces_on_board(self):
        return len(self.pieces_on_board)

    def get_player_color(self):
        return self.player_color

    def get_piece_by_position(self, position_of_desired_piece):
        for piece in self.pieces_on_board:
            if piece.position == position_of_desired_piece:
                return piece
        raise PieceNotExistException(strings.PIECE_NOT_EXIST_ERROR_TEMPLATE.format(
            position=position_of_desired_piece
        ))

    def add_piece(self, piece):
        self.num_of_pieces_left_to_place -= 1
        self.pieces_on_board.add(piece)

    def handle_piece_movement_action(self, position_of_desired_piece_to_move, new_position, new_connections):
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
                ((action_type == MoveType.MOVE_PIECE
                  or action_type == MoveType.SELECT_PIECE_TO_MOVE) and len(
                    self.get_possible_actions(state, action_type)) == 0)
        )

    def get_possible_actions(self, state, desired_action_type=MoveType.MOVE_PIECE, selected_piece=None):

        if desired_action_type == MoveType.PLACE_PIECE:
            return self.get_possible_piece_placements(state)
        if desired_action_type == MoveType.MOVE_PIECE:
            return self.get_possible_move_pieces_actions(state)
        if desired_action_type == MoveType.REMOVE_OPPONENT_PIECE:
            return self.get_possible_opponent_remove_pieces(state)
        if desired_action_type == MoveType.SELECT_PIECE_TO_MOVE:
            return self.get_all_pieces_positions(state)
        if desired_action_type == MoveType.MOVE_SELECTED_PIECE:
            return self.get_all_valid_locations_to_move_to(selected_piece, state)

    def get_all_valid_locations_to_move_to(self, selected_piece, state):
        player_move_actions = utils.convert_piece_moves_to_player_actions(selected_piece.get_possible_moves(state),
                                                                          selected_piece.position)
        possible_positions_to_move = [action[1] for action in player_move_actions]
        return possible_positions_to_move

    def get_possible_move_pieces_actions(self, game_state):
        if not (self.move_type == MoveType.MOVE_PIECE
                or self.move_type == MoveType.SELECT_PIECE_TO_MOVE
                or self.move_type == MoveType.MOVE_SELECTED_PIECE):
            raise GamePhaseException(strings.GAME_PHASE_ERROR_TEMPLATE.format(
                move_type=self.move_type.name,
                player_name=self.name
            ))

        all_possible_actions = []
        for piece in self.pieces_on_board:
            curr_piece_poss_moves = piece.get_possible_moves(state=game_state)
            for move in curr_piece_poss_moves:
                correlated_action = utils.convert_move_to_action(desired_move=move, piece_position=piece.position)
                all_possible_actions.append((piece.position, correlated_action))
        return all_possible_actions

    def is_part_of_mill(self, game_state, position, player_color):
        """Check if the piece at the given position is part of a horizontal or vertical mill."""
        row, col = position

        # Check horizontal mill
        horizontal_mill = True
        for c in range(NUM_OF_COLS):
            if game_state.board[row][c] != player_color:
                horizontal_mill = False
                break

        # Check vertical mill
        vertical_mill = True
        for r in range(NUM_OF_ROWS):
            if game_state.board[r][col] != player_color:
                vertical_mill = False
                break

        return horizontal_mill or vertical_mill

    def get_possible_opponent_remove_pieces(self, game_state):
        if not self.move_type == MoveType.REMOVE_OPPONENT_PIECE:
            raise GamePhaseException(strings.GAME_PHASE_ERROR_REMOVE_TEMPLATE.format(
                move_type=self.move_type.name,
                player_name=self.name
            ))

        opponent_cells = []
        non_mill_opponent_cells = []
        for row in range(NUM_OF_ROWS):
            for col in range(NUM_OF_COLS):
                curr_cell = game_state.board[row][col]
                if curr_cell != CellState.EMPTY and curr_cell != self.player_color:
                    opponent_cells.append((row, col))
                    if not self.is_part_of_mill(game_state, (row, col), curr_cell):
                        non_mill_opponent_cells.append((row, col))

        if non_mill_opponent_cells:
            return non_mill_opponent_cells

        # If all opponent pieces are in mills, return all opponent pieces
        return opponent_cells

    def get_possible_piece_placements(self, game_state):
        if not self.move_type == MoveType.PLACE_PIECE:
            raise GamePhaseException(strings.GAME_PHASE_ERROR_PLACE_TEMPLATE.format(
                move_type=self.move_type.name,
                player_name=self.name
            ))

        return game_state.get_empty_cells()

    def get_all_pieces_positions(self, state):
        return [piece.position for piece in self.pieces_on_board if len(piece.get_possible_moves(state)) > 0]
