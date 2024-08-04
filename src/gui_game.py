import pygame

from src.piece import Piece
from src.game_state import GameState, CellState
from src.game_state import MoveType
from utils.utils import *
from exceptions.piece_not_exist import PieceNotExistException
from src.game_state import NUM_OF_ROWS, NUM_OF_COLS

PLAYER_REMOVE_ERROR_TEMPLATE = (
    "Player {name} tried to remove opponent's piece at location {location} but there is no piece in this location"
)

# Constants
WINDOW_SIZE = (1000, 700)
BOARD_COLOR = (245, 222, 179)
LINE_COLOR = (0, 0, 0)
BLACK_COLOR = (0, 0, 0)
HIGHLIGHT_COLOR = (0, 255, 0)
BLACK_PIECE_SIZE = (95, 95)  # Desired size for the pieces
WHITE_PIECE_SIZE = (100, 100)  # Desired size for the pieces

# Board dimensions
BOARD_SIZE = 600
BOARD_OFFSET_X = (WINDOW_SIZE[0] - BOARD_SIZE) // 2
BOARD_OFFSET_Y = (WINDOW_SIZE[1] - BOARD_SIZE) // 2
POSITIONS = [
    [(BOARD_OFFSET_X, BOARD_OFFSET_Y), (BOARD_OFFSET_X + 300, BOARD_OFFSET_Y), (BOARD_OFFSET_X + 600, BOARD_OFFSET_Y)],
    [(BOARD_OFFSET_X + 100, BOARD_OFFSET_Y + 100), (BOARD_OFFSET_X + 300, BOARD_OFFSET_Y + 100),
     (BOARD_OFFSET_X + 500, BOARD_OFFSET_Y + 100)],
    [(BOARD_OFFSET_X + 200, BOARD_OFFSET_Y + 200), (BOARD_OFFSET_X + 300, BOARD_OFFSET_Y + 200),
     (BOARD_OFFSET_X + 400, BOARD_OFFSET_Y + 200)],
    [(BOARD_OFFSET_X, BOARD_OFFSET_Y + 300), (BOARD_OFFSET_X + 100, BOARD_OFFSET_Y + 300),
     (BOARD_OFFSET_X + 200, BOARD_OFFSET_Y + 300)],
    [(BOARD_OFFSET_X + 400, BOARD_OFFSET_Y + 300), (BOARD_OFFSET_X + 500, BOARD_OFFSET_Y + 300),
     (BOARD_OFFSET_X + 600, BOARD_OFFSET_Y + 300)],
    [(BOARD_OFFSET_X + 200, BOARD_OFFSET_Y + 400), (BOARD_OFFSET_X + 300, BOARD_OFFSET_Y + 400),
     (BOARD_OFFSET_X + 400, BOARD_OFFSET_Y + 400)],
    [(BOARD_OFFSET_X + 100, BOARD_OFFSET_Y + 500), (BOARD_OFFSET_X + 300, BOARD_OFFSET_Y + 500),
     (BOARD_OFFSET_X + 500, BOARD_OFFSET_Y + 500)],
    [(BOARD_OFFSET_X, BOARD_OFFSET_Y + 600), (BOARD_OFFSET_X + 300, BOARD_OFFSET_Y + 600),
     (BOARD_OFFSET_X + 600, BOARD_OFFSET_Y + 600)]
]

# Load and resize images
black_piece_img = pygame.image.load('images/light_black_piece.png')
white_piece_img = pygame.image.load('images/beige_piece.png')
black_piece_img = pygame.transform.scale(black_piece_img, BLACK_PIECE_SIZE)
white_piece_img = pygame.transform.scale(white_piece_img, WHITE_PIECE_SIZE)

# Load and resize the background image
background_img = pygame.image.load('images/wood_background_resized.jpg')
background_img = pygame.transform.scale(background_img, WINDOW_SIZE)


class GuiGame:
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

        # Initialize GUI
        pygame.init()
        pygame.display.set_caption("Nine Men's Morris")
        self.pieces_in_gui = {}
        self.screen = pygame.display.set_mode(WINDOW_SIZE)
        self.pieces_should_flash = False
        self.increment = -5
        self.blur = True
        self.alpha = 255
        self.indexes_to_flash = []
        self.selected_piece_to_move_pos = None
        self.selected_piece = None

    def run(self):
        self.game_loop()
        winner = self.get_game_result()

    def quit(self):
        pass

    def game_loop(self):

        while True:
            curr_player, other_player = self.decide_turn()
            player_color = curr_player.get_player_color()
            events = pygame.event.get()

            if self.current_move_type == MoveType.PLACE_PIECE:
                self.play_turn_of_piece_placement(curr_player, other_player, player_color, events)

            elif (self.current_move_type == MoveType.SELECT_PIECE_TO_MOVE or
                  self.current_move_type == MoveType.MOVE_SELECTED_PIECE):
                self.play_turn_of_piece_movement(curr_player, player_color, events)

            else:  # Case of MoveType.REMOVE_OPPONENT_PIECE
                self.play_turn_of_piece_removal(curr_player, other_player, events)

            if other_player.is_lost_game(self.game_state, self.current_move_type):
                self.winner = curr_player
                break

            self.draw_board()
            self.draw_pieces()
            if self.pieces_should_flash:
                self.highlight_valid_spots(
                    curr_player.get_possible_actions(self.game_state, self.current_move_type, self.selected_piece),
                    self.alpha, self.blur)
                self.alpha += self.increment
                if self.alpha <= 100 or self.alpha >= 255:
                    self.increment = -self.increment
            pygame.display.flip()
            pygame.time.delay(20)  # Delay to control flashing speed

    def play_turn_of_piece_removal(self, curr_player, other_player, events):
        opponent_remove_location, self.pieces_should_flash = curr_player.get_action(self.game_state,
                                                                                    MoveType.REMOVE_OPPONENT_PIECE,
                                                                                    events)
        if opponent_remove_location:
            if not other_player.remove_piece(opponent_remove_location):
                raise PieceNotExistException(PLAYER_REMOVE_ERROR_TEMPLATE.format(
                    name=curr_player.name,
                    location=opponent_remove_location
                ))
            self.game_state.update_board(prev_position=opponent_remove_location)
            self.current_move_type = self.prev_move_type
            curr_player.move_type = self.prev_move_type
            self.game_state.move_type = self.prev_move_type
            self.remove_piece_in_gui(opponent_remove_location[0], opponent_remove_location[1])
            self.player_1_turn = not self.player_1_turn  # Turn of the other player.

    def play_turn_of_piece_movement(self, curr_player, player_color, events):
        desired_position, self.pieces_should_flash = curr_player.get_action(self.game_state, self.current_move_type,
                                                                            events, self.pieces_in_gui,
                                                                            self.selected_piece)
        if desired_position:
            if self.current_move_type == MoveType.MOVE_SELECTED_PIECE:
                curr_player.handle_piece_movement_action(
                    position_of_desired_piece_to_move=self.selected_piece_to_move_pos,
                    new_position=desired_position,
                    new_connections=self.board_connections[desired_position])
                self.game_state.update_board(prev_position=self.selected_piece_to_move_pos,
                                             new_position=desired_position, piece_color=player_color)
                self.remove_piece_in_gui(self.selected_piece_to_move_pos[0], self.selected_piece_to_move_pos[1])
                self.place_piece_in_gui(desired_position[0], desired_position[1], player_color)
                self.selected_piece_to_move_pos = self.selected_piece = None
                self.current_move_type = MoveType.SELECT_PIECE_TO_MOVE
                self.player_1_turn = not self.player_1_turn  # Turn of the other player.
                if move_performed_a_mill(desired_position, self.game_state, player_color):
                    self.player_1_turn = not self.player_1_turn  # We need the same player to play in the next turn.
                    self.current_move_type = MoveType.REMOVE_OPPONENT_PIECE
                    curr_player.move_type = MoveType.REMOVE_OPPONENT_PIECE
                    self.game_state.move_type = MoveType.REMOVE_OPPONENT_PIECE
            else:
                self.selected_piece_to_move_pos = desired_position
                self.selected_piece = curr_player.get_piece_by_position(self.selected_piece_to_move_pos)
                self.current_move_type = MoveType.MOVE_SELECTED_PIECE

    def play_turn_of_piece_placement(self, curr_player, other_player, player_color, events):
        desired_piece_position, self.pieces_should_flash = curr_player.get_action(self.game_state, MoveType.PLACE_PIECE,
                                                                                  events, self.pieces_in_gui)
        if desired_piece_position:
            self.num_of_pieces_left_to_provide -= 1
            self.player_1_turn = not self.player_1_turn
            player_new_piece = Piece(player_color, desired_piece_position,
                                     self.board_connections[desired_piece_position])
            curr_player.add_piece(player_new_piece)
            self.place_piece_in_gui(desired_piece_position[0], desired_piece_position[1], player_color)
            self.game_state.update_board(new_position=desired_piece_position, piece_color=player_color)
            if self.num_of_pieces_left_to_provide == 0:
                self.current_move_type = MoveType.SELECT_PIECE_TO_MOVE
                self.prev_move_type = MoveType.SELECT_PIECE_TO_MOVE
                curr_player.move_type = MoveType.SELECT_PIECE_TO_MOVE
                other_player.move_type = MoveType.SELECT_PIECE_TO_MOVE
                self.game_state.move_type = MoveType.SELECT_PIECE_TO_MOVE
            if move_performed_a_mill(desired_piece_position, self.game_state, player_color):
                self.player_1_turn = not self.player_1_turn  # We need the same player to play in the next turn.
                self.current_move_type = MoveType.REMOVE_OPPONENT_PIECE
                curr_player.move_type = MoveType.REMOVE_OPPONENT_PIECE
                self.game_state.move_type = MoveType.REMOVE_OPPONENT_PIECE

    def decide_turn(self):
        if self.player_1_turn:
            curr_player = self.player_1
            other_player = self.player_2
        else:
            curr_player = self.player_2
            other_player = self.player_1
        return curr_player, other_player

    def get_game_result(self):
        return self.winner

    def place_piece_in_gui(self, row, col, piece_color):
        position = get_piece_position_in_gui(row, col)
        self.pieces_in_gui[(row, col)] = {'color': piece_color, 'position': position}

    def draw_board(self):
        self.screen.blit(background_img, (0, 0))  # Draw the background image
        # Draw the squares and lines
        pygame.draw.rect(self.screen, LINE_COLOR, pygame.Rect(BOARD_OFFSET_X, BOARD_OFFSET_Y, BOARD_SIZE, BOARD_SIZE),
                         5)
        pygame.draw.rect(self.screen, LINE_COLOR, pygame.Rect(BOARD_OFFSET_X + 100, BOARD_OFFSET_Y + 100, 400, 400), 5)
        pygame.draw.rect(self.screen, LINE_COLOR, pygame.Rect(BOARD_OFFSET_X + 200, BOARD_OFFSET_Y + 200, 200, 200), 5)
        # Draw the connecting lines
        pygame.draw.line(self.screen, LINE_COLOR, (BOARD_OFFSET_X + 300, BOARD_OFFSET_Y),
                         (BOARD_OFFSET_X + 300, BOARD_OFFSET_Y + 200), 5)
        pygame.draw.line(self.screen, LINE_COLOR, (BOARD_OFFSET_X + 300, BOARD_OFFSET_Y + 400),
                         (BOARD_OFFSET_X + 300, BOARD_OFFSET_Y + 600), 5)
        pygame.draw.line(self.screen, LINE_COLOR, (BOARD_OFFSET_X, BOARD_OFFSET_Y + 300),
                         (BOARD_OFFSET_X + 200, BOARD_OFFSET_Y + 300), 5)
        pygame.draw.line(self.screen, LINE_COLOR, (BOARD_OFFSET_X + 400, BOARD_OFFSET_Y + 300),
                         (BOARD_OFFSET_X + 600, BOARD_OFFSET_Y + 300), 5)
        for i in range(NUM_OF_ROWS):
            for j in range(NUM_OF_COLS):
                position = get_piece_position_in_gui(i, j)
                pygame.draw.circle(self.screen, BLACK_COLOR, position, 10)

    def draw_pieces(self):
        for key, piece in self.pieces_in_gui.items():
            piece_image = black_piece_img if piece['color'] == CellState.BLACK else white_piece_img
            position = piece['position']
            rect = self.screen.blit(piece_image, (position[0] - piece_image.get_width() // 2,
                                                  position[1] - piece_image.get_height() // 2))
            piece['rect'] = rect

    def highlight_valid_spots(self, valid_spots, alpha, blur=False):
        halo_surface = pygame.Surface((WINDOW_SIZE[0], WINDOW_SIZE[1]), pygame.SRCALPHA)
        for spot in valid_spots:
            position = get_piece_position_in_gui(spot[0], spot[1])
            if blur:
                for i in range(1, 3):
                    pygame.draw.circle(halo_surface,
                                       (HIGHLIGHT_COLOR[0], HIGHLIGHT_COLOR[1], HIGHLIGHT_COLOR[2], alpha // i),
                                       position, 30 + i * 10, 5)
            else:
                pygame.draw.circle(halo_surface, (HIGHLIGHT_COLOR[0], HIGHLIGHT_COLOR[1], HIGHLIGHT_COLOR[2], alpha),
                                   position, 30, 5)
        self.screen.blit(halo_surface, (0, 0))

    def remove_piece_in_gui(self, row, col):
        if (row, col) in self.pieces_in_gui:
            rect = self.pieces_in_gui[(row, col)]['rect']
            del self.pieces_in_gui[(row, col)]
            pygame.display.update(rect)  # Update only the area where the piece was removed
            return rect
        return None
