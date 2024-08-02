from src.game_state import GameState, CellState
from src.game import Game
from player_types.user_player import UserPlayer
from src.move import MoveType
from player_types.random_player import RandomPlayer
from player_types.minimax_player import MinimaxPlayer
from search_agents.minimax_agent import MiniMaxAgent
from player_types.expectimax_player import ExpectimaxPlayer
from search_agents.expectimax_agent import ExpectiMaxAgent
from utils.strings import *

NUM_OF_PIECES = 9


class GameManager:
    def __init__(self, player_1, player_2, player_1_starts_the_game=True,
                 num_of_games=1, num_of_pieces_in_game=NUM_OF_PIECES):
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
        new_game = Game(self.player_1, self.player_2, self.initial_state,
                        self.num_of_pieces_in_game, self.player_1_starts)
        new_game.run()


def main():

    user_player1 = UserPlayer(PLAYER1, NUM_OF_PIECES, CellState.GREEN)
    user_player2 = UserPlayer(PLAYER2, NUM_OF_PIECES, CellState.BLUE)

    expectimax_agent = ExpectiMaxAgent()
    expectimax_player = ExpectimaxPlayer(EXPECTIMAX_PLAYER, NUM_OF_PIECES, CellState.GREEN, expectimax_agent)
    random_player = RandomPlayer(RANDOM_PLAYER, NUM_OF_PIECES, CellState.BLUE)

    game_manager = GameManager(player_1=expectimax_player, player_2=random_player)
    game_manager.start_game()


if __name__ == '__main__':
    main()
