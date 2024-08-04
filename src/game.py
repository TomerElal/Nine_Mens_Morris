from utils import strings

from src.piece import Piece
from src.game_state import GameState
from src.game_state import MoveType
from utils.utils import move_performed_a_mill, display_board
from exceptions.piece_not_exist import PieceNotExistException
from colorama import Style

PLAYER_REMOVE_ERROR_TEMPLATE = (
    "Player {name} tried to remove opponent's piece at location {location} but there is no piece in this location"
)


class Game:
    def __init__(self, player_1, player_2, initial_state, num_of_initial_pieces, player_1_starts_the_game):
        self.num_of_pieces_left_to_provide = num_of_initial_pieces * 2
        self.player_1 = player_1
        self.player_2 = player_2
        self.game_state = initial_state
        self.board_connections = GameState.BOARD_CONNECTIONS
        self.player_1_turn = player_1_starts_the_game
        self.current_move_type = MoveType.PLACE_PIECE
        self.prev_move_type = MoveType.PLACE_PIECE
        self.winner = None

    def run(self):
        self.game_loop()
        winner = self.get_game_result()
        announcement = strings.WINNER_ANNOUNCEMENT_TEMPLATE.format(
            color=winner.player_color.color,
            name=winner.name,
            reset=Style.RESET_ALL
        )
        print(announcement)

    def quit(self):
        pass

    def game_loop(self):

        while True:
            display_board(self.game_state.board)
            curr_player, other_player = self.decide_turn()
            player_color = curr_player.get_player_color()

            if self.current_move_type == MoveType.PLACE_PIECE:
                self.play_turn_of_piece_placement(curr_player, other_player, player_color)

            elif self.current_move_type == MoveType.MOVE_PIECE:
                self.play_turn_of_piece_movement(curr_player, player_color)

            else:  # Case of MoveType.REMOVE_OPPONENT_PIECE
                self.play_turn_of_piece_removal(curr_player, other_player)

            if other_player.is_lost_game(self.game_state, self.current_move_type):
                self.winner = curr_player
                break

    def play_turn_of_piece_removal(self, curr_player, other_player):
        opponent_remove_location = curr_player.get_action(self.game_state, MoveType.REMOVE_OPPONENT_PIECE)
        if not other_player.remove_piece(opponent_remove_location):
            raise PieceNotExistException(PLAYER_REMOVE_ERROR_TEMPLATE.format(
                name=curr_player.name,
                location=opponent_remove_location
            ))
        self.game_state.update_board(prev_position=opponent_remove_location)
        self.current_move_type = self.prev_move_type
        curr_player.move_type = self.prev_move_type
        self.game_state.move_type = self.prev_move_type

    def play_turn_of_piece_movement(self, curr_player, player_color):
        prev_pos, new_pos = curr_player.get_action(self.game_state, MoveType.MOVE_PIECE)
        curr_player.handle_piece_movement_action(position_of_desired_piece_to_move=prev_pos,
                                                 new_position=new_pos, new_connections=self.board_connections[new_pos])
        self.game_state.update_board(prev_position=prev_pos, new_position=new_pos, piece_color=player_color)
        if move_performed_a_mill(new_pos, self.game_state, player_color):
            self.player_1_turn = not self.player_1_turn  # We need the same player to play in the next turn.
            self.current_move_type = MoveType.REMOVE_OPPONENT_PIECE
            curr_player.move_type = MoveType.REMOVE_OPPONENT_PIECE
            self.game_state.move_type = MoveType.REMOVE_OPPONENT_PIECE

    def play_turn_of_piece_placement(self, curr_player, other_player, player_color):
        self.num_of_pieces_left_to_provide -= 1
        desired_piece_position = curr_player.get_action(self.game_state, MoveType.PLACE_PIECE)
        player_new_piece = Piece(player_color, desired_piece_position,
                                 self.board_connections[desired_piece_position])
        curr_player.add_piece(player_new_piece)
        self.game_state.update_board(new_position=desired_piece_position, piece_color=player_color)
        if self.num_of_pieces_left_to_provide == 0:
            self.current_move_type = MoveType.MOVE_PIECE
            self.prev_move_type = MoveType.MOVE_PIECE
            curr_player.move_type = MoveType.MOVE_PIECE
            other_player.move_type = MoveType.MOVE_PIECE
            self.game_state.move_type = MoveType.MOVE_PIECE
        if move_performed_a_mill(desired_piece_position, self.game_state, player_color):
            self.player_1_turn = not self.player_1_turn  # We need the same player to play in the next turn.
            self.current_move_type = MoveType.REMOVE_OPPONENT_PIECE
            curr_player.move_type = MoveType.REMOVE_OPPONENT_PIECE
            self.game_state.move_type = MoveType.REMOVE_OPPONENT_PIECE

    def decide_turn(self):
        if self.player_1_turn:
            curr_player = self.player_1
            other_player = self.player_2
            self.player_1_turn = False
        else:
            curr_player = self.player_2
            other_player = self.player_1
            self.player_1_turn = True
        return curr_player, other_player

    def get_game_result(self):
        return self.winner
