import pygame
from src.game_state import GameState, CellState
from src.console_game import ConsoleGame
from player_types.console_user_player import ConsoleUserPlayer
from player_types.gui_user_player import GuiUserPlayer
from src.move import MoveType
from player_types.random_player import RandomPlayer
from player_types.smart_player import SmartPlayer
from player_types.console_multi_agents_player import MultiAgentsPlayer
from player_types.gui_multi_agent_player import GuiMultiAgentsPlayer
from search_agents.minimax_agent import MiniMaxAgent
from search_agents.expectimax_agent import ExpectiMaxAgent
from search_agents.alpha_beta_pruning import AlphaBetaAgent
from utils.strings import *
from utils.utils import *
from src.gui_game import GuiGame

NUM_OF_PIECES = 9

# Constants for GUI
GUI_WINDOW_SIZE = (1000, 700)
BUTTON_WIDTH = 400
BUTTON_HEIGHT = 60
BUTTON_COLOR = (134, 84, 57)
BUTTON_HOVER_COLOR = (222, 172, 128)
TEXT_COLOR = (175, 143, 111)
BACKGROUND_COLOR = (254, 216, 177)
EXIT_BUTTON_SIZE = 40
EXIT_BUTTON_COLOR = (134, 84, 57)
EXIT_BUTTON_HOVER_COLOR = (64, 34, 24)
HEADLINE_COLOR = (64, 34, 24)


class GameManager:
    def __init__(self, player_1=None, player_2=None, player_1_starts_the_game=True,
                 num_of_games=1, num_of_pieces_in_game=NUM_OF_PIECES, gui_display=True):
        self.gui_display = gui_display
        self.num_of_pieces_in_game = num_of_pieces_in_game
        self.player_1 = player_1
        self.player_2 = player_2
        self.num_of_games = num_of_games
        self.initial_state = GameState(player_1, player_2, MoveType.PLACE_PIECE)
        self.player_1_starts = player_1_starts_the_game

    def start_game(self):
        for _ in range(self.num_of_games):
            self.run_single_game()

    def run_single_game(self):
        if self.gui_display:
            self.initial_state = GameState(self.player_1, self.player_2, MoveType.PLACE_PIECE)
            new_game = GuiGame(self.player_1, self.player_2, self.initial_state,
                               self.num_of_pieces_in_game, self.player_1_starts, self)
        else:
            new_game = ConsoleGame(self.player_1, self.player_2, self.initial_state,
                                   self.num_of_pieces_in_game, self.player_1_starts)
        new_game.run()

    def opening_screen(self):
        pygame.init()
        screen = pygame.display.set_mode(GUI_WINDOW_SIZE)
        pygame.display.set_caption("Nine Men's Morris")
        font = pygame.font.SysFont('Cooper Black', 32)

        options = [
            "User player vs User player",
            "User player vs AI",
            "User player vs Smart player",
            "User player vs Random player",
            "AI player vs Smart player",
            "MCTS player vs User player",
        ]

        def draw_text(text, position, color, font_size=32):
            text_font = pygame.font.SysFont('Cooper Black', font_size)
            text_surface = text_font.render(text, True, color)
            text_rect = text_surface.get_rect(center=position)
            screen.blit(text_surface, text_rect)

        def button(text, x, y, w, h, inactive_color, active_color, action=None):
            mouse = pygame.mouse.get_pos()
            click = pygame.mouse.get_pressed()

            if x + w > mouse[0] > x and y + h > mouse[1] > y:
                pygame.draw.rect(screen, active_color, (x, y, w, h))
                if click[0] == 1 and action is not None:
                    action()
            else:
                pygame.draw.rect(screen, inactive_color, (x, y, w, h))

            draw_text(text, (x + w / 2, y + h / 2), TEXT_COLOR, 24)

        def exit_button(x, y, size, inactive_color, active_color, action=None):
            mouse = pygame.mouse.get_pos()
            click = pygame.mouse.get_pressed()

            if x + size > mouse[0] > x and y + size > mouse[1] > y:
                pygame.draw.rect(screen, active_color, (x, y, size, size))
                if click[0] == 1 and action is not None:
                    action()
            else:
                pygame.draw.rect(screen, inactive_color, (x, y, size, size))

            draw_text("X", (x + size / 2, y + size / 2), TEXT_COLOR, 24)

        def start_user_vs_user():
            self.player_1 = GuiUserPlayer(PLAYER1, NUM_OF_PIECES, CellState.WHITE, is_computer_player=False)
            self.player_2 = GuiUserPlayer(PLAYER2, NUM_OF_PIECES, CellState.BLACK, is_computer_player=False)
            self.start_game()

        def start_user_vs_ai():
            self.player_1 = GuiMultiAgentsPlayer(ALPHA_BETA_PLAYER, NUM_OF_PIECES, CellState.WHITE, AlphaBetaAgent(),
                                                 is_computer_player=True)
            self.player_2 = GuiUserPlayer(PLAYER1, NUM_OF_PIECES, CellState.BLACK, is_computer_player=False)
            self.start_game()

        def start_user_vs_random():
            self.player_1 = GuiUserPlayer(PLAYER1, NUM_OF_PIECES, CellState.WHITE, is_computer_player=False)
            self.player_2 = RandomPlayer(RANDOM_PLAYER, NUM_OF_PIECES, CellState.BLACK,
                                         is_computer_player=True, is_gui_game=True)
            self.start_game()

        def start_user_vs_smart():
            self.player_1 = GuiUserPlayer(PLAYER1, NUM_OF_PIECES, CellState.WHITE, is_computer_player=False)
            self.player_2 = SmartPlayer(SMART_PLAYER, NUM_OF_PIECES, CellState.BLACK,
                                        is_computer_player=True, is_gui_game=True)
            self.start_game()

        def start_ai_vs_random():
            self.player_1 = GuiMultiAgentsPlayer(ALPHA_BETA_PLAYER, NUM_OF_PIECES, CellState.WHITE, AlphaBetaAgent(),
                                                 is_computer_player=True)
            self.player_2 = SmartPlayer(SMART_PLAYER, NUM_OF_PIECES, CellState.BLACK,
                                        is_computer_player=True, is_gui_game=True)
            self.start_game()

        from search_agents.mcts_agent import MCTSAgent

        def start_user_vs_mcts():
            self.player_1 = GuiUserPlayer(PLAYER1, NUM_OF_PIECES, CellState.WHITE, is_computer_player=False)
            self.player_2 = GuiMultiAgentsPlayer(MCTS_PLAYER, NUM_OF_PIECES, CellState.BLACK, MCTSAgent(),
                                                 is_computer_player=True)
            self.start_game()

        def exit_game():
            pygame.quit()
            exit()

        actions = [start_user_vs_user, start_user_vs_ai, start_user_vs_smart, start_user_vs_random, start_ai_vs_random,
                   start_user_vs_mcts]

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

            screen.fill(BACKGROUND_COLOR)
            draw_text("Nine Men's Morris", (GUI_WINDOW_SIZE[0] // 2, GUI_WINDOW_SIZE[1] // 4), HEADLINE_COLOR, 64)

            for idx, option in enumerate(options):
                button(option, (GUI_WINDOW_SIZE[0] // 2 - BUTTON_WIDTH // 2), (GUI_WINDOW_SIZE[1] // 2.5 + idx * 70),
                       BUTTON_WIDTH, BUTTON_HEIGHT, BUTTON_COLOR, BUTTON_HOVER_COLOR, actions[idx])

            exit_button(20, 20, EXIT_BUTTON_SIZE, EXIT_BUTTON_COLOR, EXIT_BUTTON_HOVER_COLOR, exit_game)

            pygame.display.update()


def main():
    game_manager = GameManager(gui_display=True)
    game_manager.opening_screen()


if __name__ == '__main__':
    main()
