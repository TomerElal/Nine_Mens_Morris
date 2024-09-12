import csv
import os
import pygame
import argparse
import torch

from src.game_state import GameState, CellState
from src.console_game import ConsoleGame
from player_types.gui_user_player import GuiUserPlayer
from src.move import MoveType
from player_types.random_player import RandomPlayer
from player_types.smart_player import SmartPlayer
from player_types.gui_multi_agent_player import GuiMultiAgentsPlayer
from search_agents.alpha_beta_pruning import AlphaBetaAgent
from common.utils import *
from search_agents.deep_q_learning import DQNAgent
from common.strings import *
from src.gui_game import GuiGame
from search_agents.mcts_agent import MCTSAgent

NUM_OF_PIECES = 9
MODEL_PATH = "dqn_model.pth"  # Path to save or load the model

# Constants for GUI
GUI_WINDOW_SIZE = (1000, 700)
BUTTON_WIDTH = 500
BUTTON_HEIGHT = 57
BUTTON_COLOR = (134, 84, 57)
BUTTON_HOVER_COLOR = (222, 172, 128)
TEXT_COLOR = (175, 143, 111)
BACKGROUND_COLOR = (254, 216, 177)
EXIT_BUTTON_SIZE = 40
EXIT_BUTTON_COLOR = (134, 84, 57)
EXIT_BUTTON_HOVER_COLOR = (64, 34, 24)
HEADLINE_COLOR = (64, 34, 24)
DELAY_BUTTON_WIDTH = 250
DELAY_BUTTON_HEIGHT = 40
OPTIONS_BUTTON_WIDTH = 150
OPTIONS_BUTTON_HEIGHT = 40

dqn_agent = DQNAgent(state_size=74, action_size=24)


# Init DQN agent with loading a saved model
def load_dqn_agent():
    if os.path.exists(MODEL_PATH):
        print(f"Loading model from {MODEL_PATH}...")
        dqn_agent.policy_net.load_state_dict(torch.load(MODEL_PATH))
        dqn_agent.target_net.load_state_dict(torch.load(MODEL_PATH))
        print("Model loaded successfully!")
    else:
        print(f"Model file {MODEL_PATH} not found! Training a new model.")


class GameManager:
    def __init__(self, player_1=None, player_2=None, player_1_starts_the_game=True, delay_between_moves=0,
                 num_of_games=1, num_of_pieces_in_game=NUM_OF_PIECES, gui_display=True):
        self.delay_between_moves = delay_between_moves
        self.gui_display = gui_display
        self.num_of_pieces_in_game = num_of_pieces_in_game
        self.player_1 = player_1
        self.player_2 = player_2
        self.num_of_games = num_of_games
        self.initial_state = GameState(player_1, player_2, MoveType.PLACE_PIECE)
        self.player_1_starts = player_1_starts_the_game
        if player_1 is not None and player_2 is not None:
            self.csv_file_name = f"{player_1.name}_vs_{player_2.name}_{num_of_games}_games.csv"

            # Initialize CSV file with headers
            self.init_csv_file()

    def init_csv_file(self):
        """Initialize the CSV file with column headers."""
        if not os.path.exists(self.csv_file_name):
            with open(self.csv_file_name, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["Winner", "PiecesLeft", "TotalMoves", "Score"])

    def save_results_to_csv(self, winner_player_number, num_of_pieces_left_of_winner, num_of_moves_in_the_game, score):
        """Save the game results to the CSV file."""
        with open(self.csv_file_name, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([winner_player_number, num_of_pieces_left_of_winner, num_of_moves_in_the_game, score])

    def start_game(self):
        for _ in range(self.num_of_games):
            self.run_single_game()

            # Reinitialize player attributes after each game
            self.player_1.pieces_on_board = set()
            self.player_2.pieces_on_board = set()
            self.player_1.move_type = self.player_2.move_type = MoveType.PLACE_PIECE
            self.player_1.num_of_pieces_left_to_place = self.player_2.num_of_pieces_left_to_place = NUM_OF_PIECES

    def run_single_game(self):
        if self.gui_display:
            self.initial_state = GameState(self.player_1, self.player_2, MoveType.PLACE_PIECE)
            new_game = GuiGame(self.player_1, self.player_2, self.initial_state, self.num_of_pieces_in_game,
                               self.player_1_starts, self, self.delay_between_moves, self.num_of_games)
        else:
            new_game = ConsoleGame(self.player_1, self.player_2, self.initial_state,
                                   self.num_of_pieces_in_game, self.player_1_starts)

        # Run the game and get the results
        winner_player_number, winner = new_game.run()
        num_of_pieces_left_of_winner = len(winner.pieces_on_board)
        num_of_moves_in_the_game = new_game.curr_num_of_moves
        score = (num_of_pieces_left_of_winner * 100) - num_of_moves_in_the_game

        # Save results to CSV file
        self.save_results_to_csv(winner_player_number, num_of_pieces_left_of_winner, num_of_moves_in_the_game, score)

    def opening_screen(self):
        pygame.init()
        screen = pygame.display.set_mode(GUI_WINDOW_SIZE)
        pygame.display.set_caption("Nine Men's Morris")

        options = [
            "User player vs User player",
            "User player vs AlphaBeta-AI",
            "User player vs MCTS-AI",
            "AlphaBeta-AI player vs Random player",
            "AlphaBeta-AI player vs Smart player",
            "MCTS-AI player vs Smart player",
            "AlphaBeta-AI player vs MCTS-AI player",
            "DQN-AI player vs User player",
        ]

        delay_options = [0, 1, 2, 3]
        selected_delay = [self.delay_between_moves]  # Store the selected delay

        def draw_text(text, position, color, font_size=32):
            text_font = pygame.font.SysFont('Cooper Black', font_size)
            text_surface = text_font.render(text, True, color)
            text_rect = text_surface.get_rect(center=position)
            screen.blit(text_surface, text_rect)

        def button(text, x, y, w, h, inactive_color, active_color, action=None):
            is_button_pressed(action, active_color, h, inactive_color, w, x, y)

            draw_text(text, (x + w / 2, y + h / 2), TEXT_COLOR, 24)

        def is_button_pressed(action, active_color, h, inactive_color, w, x, y):
            mouse = pygame.mouse.get_pos()
            click = pygame.mouse.get_pressed()
            if x + w > mouse[0] > x and y + h > mouse[1] > y:
                pygame.draw.rect(screen, active_color, (x, y, w, h))
                if click[0] == 1 and action is not None:
                    action()
            else:
                pygame.draw.rect(screen, inactive_color, (x, y, w, h))

        def exit_button(x, y, size, inactive_color, active_color, action=None):
            is_button_pressed(action, active_color, size, inactive_color, size, x, y)

            draw_text("X", (x + size / 2, y + size / 2), TEXT_COLOR, 24)

        def select_delay(delay):
            selected_delay[0] = delay
            set_game_delay(delay)

        def show_delay_menu():
            delay_menu_open = True
            while delay_menu_open:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()

                screen.fill(BACKGROUND_COLOR)
                draw_text("Select Delay Between Moves", (GUI_WINDOW_SIZE[0] // 2, GUI_WINDOW_SIZE[1] // 6),
                          HEADLINE_COLOR, 48)

                for idx, delay_option in enumerate(delay_options):
                    button(f"{delay_option} seconds", (GUI_WINDOW_SIZE[0] // 2 - DELAY_BUTTON_WIDTH // 2),
                           (GUI_WINDOW_SIZE[1] // 3 + idx * 50), DELAY_BUTTON_WIDTH, DELAY_BUTTON_HEIGHT,
                           BUTTON_COLOR, BUTTON_HOVER_COLOR, lambda d=delay_option: select_delay(d))

                exit_button(40, 20, EXIT_BUTTON_SIZE, EXIT_BUTTON_COLOR, EXIT_BUTTON_HOVER_COLOR,
                            lambda: return_to_opening_screen())

                pygame.display.update()

        def set_game_delay(delay):
            self.delay_between_moves = delay
            return_to_opening_screen()

        def return_to_opening_screen():
            time.sleep(0.1)
            self.opening_screen()

        def start_user_vs_user():
            self.player_1 = GuiUserPlayer(PLAYER1, NUM_OF_PIECES, CellState.WHITE, is_computer_player=False)
            self.player_2 = GuiUserPlayer(PLAYER2, NUM_OF_PIECES, CellState.BLACK, is_computer_player=False)
            self.start_game()

        def start_user_vs_alphabeta():
            self.player_1 = GuiMultiAgentsPlayer(ALPHA_BETA_PLAYER, NUM_OF_PIECES, CellState.WHITE, AlphaBetaAgent(),
                                                 is_computer_player=True)
            self.player_2 = GuiUserPlayer(PLAYER1, NUM_OF_PIECES, CellState.BLACK, is_computer_player=False)
            self.start_game()

        def start_user_vs_mcts():
            self.player_1 = GuiUserPlayer(PLAYER1, NUM_OF_PIECES, CellState.WHITE, is_computer_player=False)
            self.player_2 = GuiMultiAgentsPlayer(MCTS_PLAYER, NUM_OF_PIECES, CellState.BLACK, MCTSAgent(1),
                                                 is_computer_player=True)
            self.start_game()

        def start_alphabeta_vs_smart():
            self.player_1 = GuiMultiAgentsPlayer(ALPHA_BETA_PLAYER, NUM_OF_PIECES, CellState.WHITE, AlphaBetaAgent(),
                                                 is_computer_player=True)
            self.player_2 = SmartPlayer(SMART_PLAYER, NUM_OF_PIECES, CellState.BLACK,
                                        is_computer_player=True, is_gui_game=True)
            self.start_game()

        def start_alphabeta_vs_random():
            self.player_1 = GuiMultiAgentsPlayer(ALPHA_BETA_PLAYER, NUM_OF_PIECES, CellState.WHITE, AlphaBetaAgent(),
                                                 is_computer_player=True)
            self.player_2 = RandomPlayer(RANDOM_PLAYER, NUM_OF_PIECES, CellState.BLACK,
                                         is_computer_player=True, is_gui_game=True)
            self.start_game()

        def start_smart_vs_mcts():
            self.player_1 = SmartPlayer(SMART_PLAYER, NUM_OF_PIECES, CellState.WHITE,
                                        is_computer_player=True, is_gui_game=True)
            self.player_2 = GuiMultiAgentsPlayer(MCTS_PLAYER, NUM_OF_PIECES, CellState.BLACK, MCTSAgent(1),
                                                 is_computer_player=True)
            self.start_game()

        def start_alphabeta_vs_mcts():
            self.player_1 = GuiMultiAgentsPlayer(MCTS_PLAYER, NUM_OF_PIECES, CellState.WHITE, MCTSAgent(1),
                                                 is_computer_player=True)
            self.player_2 = GuiMultiAgentsPlayer(ALPHA_BETA_PLAYER, NUM_OF_PIECES, CellState.BLACK,
                                                 AlphaBetaAgent(player_number=2), is_computer_player=True)
            self.start_game()

        def start_user_vs_dqn():
            self.player_1 = GuiUserPlayer(PLAYER1, NUM_OF_PIECES, CellState.WHITE, is_computer_player=False)
            self.player_2 = GuiMultiAgentsPlayer(DQN_PLAYER, NUM_OF_PIECES, CellState.BLACK, dqn_agent,
                                                 is_computer_player=True)
            self.start_game()

        def exit_game():
            pygame.quit()
            exit()

        actions = [start_user_vs_user, start_user_vs_alphabeta, start_user_vs_mcts, start_alphabeta_vs_random,
                   start_alphabeta_vs_smart, start_smart_vs_mcts, start_alphabeta_vs_mcts, start_user_vs_dqn]

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

            screen.fill(BACKGROUND_COLOR)
            draw_text("Nine Men's Morris", (GUI_WINDOW_SIZE[0] // 2, GUI_WINDOW_SIZE[1] // 8), HEADLINE_COLOR, 64)

            for idx, option in enumerate(options):
                button(option, (GUI_WINDOW_SIZE[0] // 2 - BUTTON_WIDTH // 2), (GUI_WINDOW_SIZE[1] // 4.8 + idx * 70),
                       BUTTON_WIDTH, BUTTON_HEIGHT, BUTTON_COLOR, BUTTON_HOVER_COLOR, actions[idx])

            # Options button for setting delay
            button("Options", GUI_WINDOW_SIZE[0] - OPTIONS_BUTTON_WIDTH - 20, 20,
                   OPTIONS_BUTTON_WIDTH, OPTIONS_BUTTON_HEIGHT, BUTTON_COLOR, BUTTON_HOVER_COLOR, show_delay_menu)

            exit_button(40, 20, EXIT_BUTTON_SIZE, EXIT_BUTTON_COLOR, EXIT_BUTTON_HOVER_COLOR, exit_game)

            pygame.display.update()


def train_model():
    player1 = SmartPlayer(SMART_PLAYER, NUM_OF_PIECES, CellState.WHITE, is_computer_player=True, is_gui_game=False)
    player2 = GuiMultiAgentsPlayer(DQN_PLAYER, NUM_OF_PIECES, CellState.BLACK, dqn_agent, is_computer_player=True)
    num_episodes = 2000
    print(num_episodes)
    dqn_agent.train(player1, player2, num_episodes)
    dqn_agent.save_model(MODEL_PATH)


def get_player_by_type(player_type, color):
    """Initialize the player based on the type and color."""
    if player_type == "random":
        return RandomPlayer(RANDOM_PLAYER, NUM_OF_PIECES, color, is_computer_player=True, is_gui_game=True)
    elif player_type == "smart":
        return SmartPlayer(SMART_PLAYER, NUM_OF_PIECES, color, is_computer_player=True, is_gui_game=True)
    elif player_type == "alphabeta":
        return GuiMultiAgentsPlayer(ALPHA_BETA_PLAYER, NUM_OF_PIECES, color, AlphaBetaAgent(), is_computer_player=True)
    elif player_type == "mcts":
        return GuiMultiAgentsPlayer(MCTS_PLAYER, NUM_OF_PIECES, color, MCTSAgent(1), is_computer_player=True)
    elif player_type == "dqn":
        return GuiMultiAgentsPlayer(DQN_PLAYER, NUM_OF_PIECES, color, dqn_agent, is_computer_player=True)
    else:
        return GuiUserPlayer("User", NUM_OF_PIECES, color, is_computer_player=False, is_gui_game=True)


def main():
    parser = argparse.ArgumentParser(description="Nine Men's Morris - AI Game")

    # Define possible arguments
    parser.add_argument('--train', action='store_true', help="Train the DQN agent")
    parser.add_argument('--load', action='store_true', help="Load a pre-trained DQN model")
    parser.add_argument('--player1', choices=['random', 'smart', 'alphabeta', 'mcts', 'dqn', 'user'],
                        help="Type of player 1")
    parser.add_argument('--player2', choices=['random', 'smart', 'alphabeta', 'mcts', 'dqn', 'user'],
                        help="Type of player 2")
    parser.add_argument('--num_games', type=int, default=1, help="Number of games to run")
    parser.add_argument('--first_player', choices=['player1', 'player2'], default='player1', help="Who starts the game")
    parser.add_argument('--delay', type=int, default=0, help="Delay between moves in seconds")

    args = parser.parse_args()

    # Handle DQN training or loading
    if args.train:
        train_model()
        print("Training complete!")
    elif args.load:
        dqn_agent.load_model(MODEL_PATH)

    # If arguments for player types are provided, initialize the game with those
    if args.player1 and args.player2:
        player_1_color = CellState.WHITE if args.first_player == 'player1' else CellState.BLACK
        player_2_color = CellState.BLACK if args.first_player == 'player1' else CellState.WHITE

        player_1 = get_player_by_type(args.player1, player_1_color)
        player_2 = get_player_by_type(args.player2, player_2_color)

        game_manager = GameManager(player_1=player_1, player_2=player_2, delay_between_moves=args.delay,
                                   num_of_games=args.num_games, player_1_starts_the_game=args.first_player == 'player1')
        game_manager.start_game()
    else:
        # If no player arguments are given, show the opening screen
        game_manager = GameManager(gui_display=True)
        game_manager.opening_screen()


if __name__ == '__main__':
    main()
