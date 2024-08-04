from src.game_state import GameState, CellState
from src.game import Game
from player_types.console_user_player import ConsoleUserPlayer
from player_types.gui_user_player import GuiUserPlayer
from src.move import MoveType
from player_types.random_player import RandomPlayer
from player_types.multi_agents_player import MultiAgentsPlayer
from search_agents.minimax_agent import MiniMaxAgent
from search_agents.expectimax_agent import ExpectiMaxAgent
from search_agents.alpha_beta_pruning import AlphaBetaAgent
from utils.strings import *
from src.gui_game import GuiGame

NUM_OF_PIECES = 3


class GameManager:
    def __init__(self, player_1, player_2, player_1_starts_the_game=True,
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
            new_game = GuiGame(self.player_1, self.player_2, self.initial_state,
                               self.num_of_pieces_in_game, self.player_1_starts)
        else:
            new_game = Game(self.player_1, self.player_2, self.initial_state,
                            self.num_of_pieces_in_game, self.player_1_starts)
        new_game.run()


def main():
    tomer = ConsoleUserPlayer("Tomer", NUM_OF_PIECES, CellState.BLUE)
    gui_user_player1 = GuiUserPlayer(PLAYER1, NUM_OF_PIECES, CellState.WHITE)
    gui_user_player2 = GuiUserPlayer(PLAYER2, NUM_OF_PIECES, CellState.BLACK)
    console_user_player1 = ConsoleUserPlayer(PLAYER1, NUM_OF_PIECES, CellState.GREEN)
    console_user_player2 = ConsoleUserPlayer(PLAYER2, NUM_OF_PIECES, CellState.BLUE)

    expectimax_agent = ExpectiMaxAgent()
    minimax_agent = MiniMaxAgent()
    alpha_beta_agent = AlphaBetaAgent()
    multi_agents_player = MultiAgentsPlayer(ALPHA_BETA_PLAYER, NUM_OF_PIECES, CellState.GREEN, alpha_beta_agent)
    random_player = RandomPlayer(RANDOM_PLAYER, NUM_OF_PIECES, CellState.BLUE)

    game_manager = GameManager(player_1=gui_user_player1, player_2=gui_user_player2, gui_display=True)
    game_manager.start_game()


if __name__ == '__main__':
    main()
