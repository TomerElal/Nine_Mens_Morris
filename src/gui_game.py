import pygame

from src.piece import Piece
from src.game_state import GameState, CellState
from src.game_state import MoveType
from utils.utils import *
from exceptions.piece_not_exist import PieceNotExistException
from src.game_state import NUM_OF_ROWS, NUM_OF_COLS

# Load and resize images
black_piece_img = pygame.image.load('images/light_black_piece.png')
white_piece_img = pygame.image.load('images/beige_piece.png')
black_piece_img = pygame.transform.scale(black_piece_img, BLACK_PIECE_SIZE)
white_piece_img = pygame.transform.scale(white_piece_img, WHITE_PIECE_SIZE)

# Load and resize the background image
background_img = pygame.image.load('images/wood_background_resized.jpg')
background_img = pygame.transform.scale(background_img, GUI_WINDOW_SIZE)


class GuiGame:
    def __init__(self, player_1, player_2, initial_state, num_of_initial_pieces, player_1_starts_the_game,
                 game_manager):
        self.game_manager = game_manager
        self.iterations_to_wait_after_computer_played = ITERATIONS_TO_WAIT
        self.ai_selected_position = None
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
        self.player_1_pieces = self.player_2_pieces = num_of_initial_pieces
        self.screen = pygame.display.set_mode(GUI_WINDOW_SIZE)
        self.pieces_should_flash = False
        self.increment = -5
        self.blur = True
        self.alpha = 255
        self.indexes_to_flash = []
        self.selected_piece_to_move_pos = None
        self.selected_piece = None
        self.highlight_color = GREEN_HIGHLIGHT_COLOR
        self.font = pygame.font.SysFont('Cooper Black', 32)
        self.text_display = ''

    def run(self):
        self.game_loop()
        winner = self.get_game_result()
        winner_announcement = WINNER_ANNOUNCEMENT_TEMPLATE.format(
            color=winner.player_color.color,
            name=winner.name,
            reset=Style.RESET_ALL
        )
        win_score = RESULT.format(
            color=Fore.LIGHTYELLOW_EX,
            num_pieces_left=winner.get_num_of_pieces_on_board(),
            reset=Style.RESET_ALL,
            other_color=winner.player_color.color
        )
        print(winner_announcement + '\n' + win_score)

    def quit(self):
        pass

    def game_loop(self):

        while True:
            curr_player, other_player = self.decide_turn()
            player_color = curr_player.get_player_color()
            self.highlight_color = GREEN_HIGHLIGHT_COLOR
            events = pygame.event.get()

            if other_player.is_computer_player and self.iterations_to_wait_after_computer_played > 0:
                self.iterations_to_wait_after_computer_played -= 1
                continue

            if self.ai_selected_position:
                self.update_gui(curr_player)
                self.do_the_actual_piece_move(curr_player, self.ai_selected_position, player_color)
                self.update_gui(curr_player)
                time.sleep(GUI_TIME_TO_SLEEP)
                continue

            elif self.current_move_type == MoveType.PLACE_PIECE:
                self.play_turn_of_piece_placement(curr_player, other_player, player_color, events)

            elif self.current_move_type == MoveType.SELECT_PIECE_TO_MOVE:
                self.select_piece_to_move(curr_player, events, player_color)

            elif self.current_move_type == MoveType.MOVE_SELECTED_PIECE:
                self.move_selected_piece(curr_player, player_color, events)

            else:  # Case of MoveType.REMOVE_OPPONENT_PIECE
                self.play_turn_of_piece_removal(curr_player, other_player, events)

            if other_player.is_lost_game(self.game_state, self.current_move_type):
                self.winner = curr_player
                break

            self.update_gui(curr_player)

    def update_gui(self, curr_player):
        self.draw_board()
        self.draw_pieces()
        self.draw_player_pieces()
        self.display_home_button()
        self.display_exit_button()
        self.display_text(self.text_display, (150, 40))
        if self.pieces_should_flash:
            if self.current_move_type == MoveType.SELECT_PIECE_TO_MOVE:
                possible_actions = curr_player.get_all_pieces_positions(self.game_state)
            elif self.current_move_type == MoveType.MOVE_SELECTED_PIECE:
                possible_actions = curr_player.get_all_valid_locations_to_move_to(self.selected_piece,
                                                                                  self.game_state)
            else:
                possible_actions = curr_player.get_possible_actions(self.game_state, self.current_move_type,
                                                                    self.selected_piece)
            self.highlight_valid_spots(possible_actions, self.alpha, self.highlight_color,
                                       self.highlight_color != RED_HIGHLIGHT_COLOR)
            self.alpha += self.increment
            if self.alpha <= 100 or self.alpha >= 255:
                self.increment = -self.increment
        pygame.display.flip()
        pygame.time.delay(20)  # Delay to control flashing speed

    def play_turn_of_piece_placement(self, curr_player, other_player, player_color, events):
        desired_piece_position, self.pieces_should_flash = curr_player.get_action(self.game_state, MoveType.PLACE_PIECE,
                                                                                  events, self.pieces_in_gui)
        self.text_display = f"{curr_player.name} it's your turn!\nPlace your piece in an empty position."
        self.highlight_color = WHITE_HIGHLIGHT_COLOR if player_color == CellState.WHITE else BLACK_HIGHLIGHT_COLOR

        if desired_piece_position:
            if curr_player.is_computer_player:
                self.text_display = f"{curr_player.name} will now select a position for new piece"
                self.update_gui(curr_player)
                time.sleep(GUI_TIME_TO_SLEEP)
                self.iterations_to_wait_after_computer_played = ITERATIONS_TO_WAIT
            self.num_of_pieces_left_to_provide -= 1
            self.player_1_turn = not self.player_1_turn
            player_new_piece = Piece(player_color, desired_piece_position,
                                     self.board_connections[desired_piece_position])
            curr_player.add_piece(player_new_piece)
            self.place_piece_in_gui(desired_piece_position[0], desired_piece_position[1], player_color)
            self.game_state.update_board(new_position=desired_piece_position, piece_color=player_color)
            # self.game_state.curr_player_turn = 3 - self.game_state.curr_player_turn
            if player_color == CellState.WHITE:
                self.player_1_pieces -= 1
            else:
                self.player_2_pieces -= 1
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

    def select_piece_to_move(self, curr_player, events, player_color):
        desired_position, self.pieces_should_flash = curr_player.get_action(self.game_state, self.current_move_type,
                                                                            events, self.pieces_in_gui,
                                                                            self.selected_piece)
        self.text_display = f"{curr_player.name} it's your turn!\nSelect a Piece to move.."
        self.highlight_color = WHITE_HIGHLIGHT_COLOR if player_color == CellState.WHITE else BLACK_HIGHLIGHT_COLOR

        if desired_position:
            if curr_player.is_computer_player:
                self.text_display = f"{curr_player.name} will now select a piece to move"
                self.update_gui(curr_player)
                time.sleep(GUI_TIME_TO_SLEEP)
                prev_pos = desired_position[0]
                new_pos = desired_position[1]
                self.text_display = f"{curr_player.name} selected the piece at location {prev_pos}"
                self.ai_selected_position = new_pos
                self.selected_piece_to_move_pos = prev_pos
                self.selected_piece = curr_player.get_piece_by_position(self.selected_piece_to_move_pos)
                self.current_move_type = MoveType.MOVE_SELECTED_PIECE
                self.iterations_to_wait_after_computer_played = ITERATIONS_TO_WAIT
                return

            self.selected_piece_to_move_pos = desired_position
            self.selected_piece = curr_player.get_piece_by_position(self.selected_piece_to_move_pos)
            self.current_move_type = MoveType.MOVE_SELECTED_PIECE

    def move_selected_piece(self, curr_player, player_color, events):
        player_changed_selected_piece = self.check_if_player_changed_piece_selection(curr_player, events)
        if player_changed_selected_piece:
            return
        desired_position, self.pieces_should_flash = curr_player.get_action(self.game_state, self.current_move_type,
                                                                            events, self.pieces_in_gui,
                                                                            self.selected_piece)
        self.text_display = f"Now move your piece to a valid position"

        if desired_position:
            self.do_the_actual_piece_move(curr_player, desired_position, player_color)

    def check_if_player_changed_piece_selection(self, curr_player, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                possible_select_actions = curr_player.get_possible_actions(self.game_state,
                                                                           MoveType.SELECT_PIECE_TO_MOVE,
                                                                           self.selected_piece)
                for index_location, piece in self.pieces_in_gui.items():
                    if piece['rect'].collidepoint(mouse_pos):
                        if index_location in possible_select_actions:
                            self.selected_piece_to_move_pos = index_location
                            self.selected_piece = curr_player.get_piece_by_position(self.selected_piece_to_move_pos)
                            return
                        break  # Means the user clicked on invalid spot.
                return False

    def do_the_actual_piece_move(self, curr_player, desired_position, player_color):
        if curr_player.is_computer_player:
            time.sleep(GUI_TIME_TO_SLEEP)
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
        self.ai_selected_position = None

        if curr_player.is_computer_player:
            self.text_display = f"{curr_player.name} moved the piece to location {desired_position}!"
            self.pieces_should_flash = False
            self.iterations_to_wait_after_computer_played = ITERATIONS_TO_WAIT

        if move_performed_a_mill(desired_position, self.game_state, player_color):
            self.player_1_turn = not self.player_1_turn  # We need the same player to play in the next turn.
            self.current_move_type = MoveType.REMOVE_OPPONENT_PIECE
            curr_player.move_type = MoveType.REMOVE_OPPONENT_PIECE
            self.game_state.move_type = MoveType.REMOVE_OPPONENT_PIECE

    def play_turn_of_piece_removal(self, curr_player, other_player, events):
        opponent_remove_location, self.pieces_should_flash = curr_player.get_action(self.game_state,
                                                                                    MoveType.REMOVE_OPPONENT_PIECE,
                                                                                    events)
        self.font = pygame.font.SysFont('Segoe UI Emoji', 30)
        self.font.set_bold(True)
        self.text_display = f"{curr_player.name} it's still your turn!\nRemove a piece of your opponent 🚀🚀"
        self.highlight_color = RED_HIGHLIGHT_COLOR

        if opponent_remove_location:

            if not other_player.remove_piece(opponent_remove_location):
                raise PieceNotExistException(PLAYER_REMOVE_ERROR_TEMPLATE.format(
                    name=curr_player.name,
                    location=opponent_remove_location
                ))

            if curr_player.is_computer_player:
                self.text_display = f"😱😱 {curr_player.name} will now select a piece of yours to remove! 💀"
                self.update_gui(curr_player)
                time.sleep(GUI_TIME_TO_SLEEP)
                self.iterations_to_wait_after_computer_played = ITERATIONS_TO_WAIT

            self.game_state.update_board(prev_position=opponent_remove_location)
            self.current_move_type = self.prev_move_type
            curr_player.move_type = self.prev_move_type
            self.game_state.move_type = self.prev_move_type
            self.remove_piece_in_gui(opponent_remove_location[0], opponent_remove_location[1])
            self.player_1_turn = not self.player_1_turn  # Turn of the other player.

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
        pygame.draw.rect(self.screen, LINE_COLOR,
                         pygame.Rect(BOARD_OFFSET_X + (BOARD_SIZE // 6), BOARD_OFFSET_Y + (BOARD_SIZE // 6),
                                     (4 * BOARD_SIZE // 6), (4 * BOARD_SIZE // 6)), 5)
        pygame.draw.rect(self.screen, LINE_COLOR,
                         pygame.Rect(BOARD_OFFSET_X + (BOARD_SIZE // 3), BOARD_OFFSET_Y + (BOARD_SIZE // 3),
                                     (BOARD_SIZE // 3), (BOARD_SIZE // 3)), 5)
        # Draw the connecting lines
        pygame.draw.line(self.screen, LINE_COLOR, (BOARD_OFFSET_X + (BOARD_SIZE // 2), BOARD_OFFSET_Y),
                         (BOARD_OFFSET_X + (BOARD_SIZE // 2), BOARD_OFFSET_Y + (BOARD_SIZE // 3)), 5)
        pygame.draw.line(self.screen, LINE_COLOR,
                         (BOARD_OFFSET_X + (BOARD_SIZE // 2), BOARD_OFFSET_Y + (4 * BOARD_SIZE // 6)),
                         (BOARD_OFFSET_X + (BOARD_SIZE // 2), BOARD_OFFSET_Y + BOARD_SIZE), 5)
        pygame.draw.line(self.screen, LINE_COLOR, (BOARD_OFFSET_X, BOARD_OFFSET_Y + (BOARD_SIZE // 2)),
                         (BOARD_OFFSET_X + (BOARD_SIZE // 3), BOARD_OFFSET_Y + (BOARD_SIZE // 2)), 5)
        pygame.draw.line(self.screen, LINE_COLOR,
                         (BOARD_OFFSET_X + (4 * BOARD_SIZE // 6), BOARD_OFFSET_Y + (BOARD_SIZE // 2)),
                         (BOARD_OFFSET_X + BOARD_SIZE, BOARD_OFFSET_Y + (BOARD_SIZE // 2)), 5)
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

    def draw_player_pieces(self):
        for i in range(self.player_1_pieces):
            self.screen.blit(white_piece_img, (60, GUI_WINDOW_SIZE[1] // 5 + i * (WHITE_PIECE_SIZE[1] // 2)))
        for i in range(self.player_2_pieces):
            self.screen.blit(black_piece_img, (GUI_WINDOW_SIZE[0] - BLACK_PIECE_SIZE[0] - 70,
                                               GUI_WINDOW_SIZE[1] // 5 + i * (BLACK_PIECE_SIZE[1] // 2)))

    def highlight_valid_spots(self, valid_spots, alpha, color, blur=False):
        halo_surface = pygame.Surface((GUI_WINDOW_SIZE[0], GUI_WINDOW_SIZE[1]), pygame.SRCALPHA)
        for spot in valid_spots:
            position = get_piece_position_in_gui(spot[0], spot[1])
            if blur:
                for i in range(1, 3):
                    pygame.draw.circle(halo_surface,
                                       (color[0], color[1], color[2], alpha // i),
                                       position, (BOARD_SIZE / 25) + i * 10, BOARD_SIZE // 100)
            else:
                pygame.draw.circle(halo_surface, (color[0], color[1], color[2], alpha),
                                   position, (BOARD_SIZE / 20), BOARD_SIZE // 100)
        self.screen.blit(halo_surface, (0, 0))

    def remove_piece_in_gui(self, row, col):
        if (row, col) in self.pieces_in_gui:
            rect = self.pieces_in_gui[(row, col)]['rect']
            del self.pieces_in_gui[(row, col)]
            pygame.display.update(rect)  # Update only the area where the piece was removed
            return rect
        return None

    def display_text(self, text, position, color=(0, 0, 0)):
        lines = text.split('\n')
        for i, line in enumerate(lines):
            text_surface = self.font.render(line, True, color)
            text_rect = text_surface.get_rect(
                center=(GUI_WINDOW_SIZE[0] // 2, position[1] + i * (GUI_WINDOW_SIZE[1] - 80)))
            self.screen.blit(text_surface, text_rect)
        self.font = pygame.font.SysFont('Cooper Black', 32)

    def display_home_button(self):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        x, y, w, h = 20, 625, BUTTON_WIDTH / 2, BUTTON_HEIGHT / 2

        if x + w > mouse[0] > x and y + h > mouse[1] > y:
            pygame.draw.rect(self.screen, BUTTON_HOVER_COLOR, (x, y, w, h))
            if click[0] == 1:
                self.game_manager.opening_screen()
        else:
            pygame.draw.rect(self.screen, BUTTON_COLOR, (x, y, w, h))

        self.font = pygame.font.SysFont('Cooper Black', 20)
        text_surface = self.font.render("Home", True, TEXT_COLOR)
        text_rect = text_surface.get_rect(center=(x + w / 2, y + h / 2))
        self.font = pygame.font.SysFont('Cooper Black', 32)
        self.screen.blit(text_surface, text_rect)

    def display_exit_button(self):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        x, y, w, h = 20, 662, BUTTON_WIDTH / 2, BUTTON_HEIGHT / 2

        if x + w > mouse[0] > x and y + h > mouse[1] > y:
            pygame.draw.rect(self.screen, BUTTON_HOVER_COLOR, (x, y, w, h))
            if click[0] == 1:
                pygame.quit()
                exit()
        else:
            pygame.draw.rect(self.screen, BUTTON_COLOR, (x, y, w, h))

        self.font = pygame.font.SysFont('Cooper Black', 20)
        text_surface = self.font.render("Exit", True, TEXT_COLOR)
        text_rect = text_surface.get_rect(center=(x + w / 2, y + h / 2))
        self.font = pygame.font.SysFont('Cooper Black', 32)
        self.screen.blit(text_surface, text_rect)
