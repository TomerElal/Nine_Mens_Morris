from game_state import GameState, CellState
from player import Player
from game import Game
from player_types.user_player import UserPlayer
from player_types.random_player import RandomPlayer

NUM_OF_PIECES = 9


class GameManager:
    def __init__(self, player_1, player_2, player_1_starts_the_game=True,
                 num_of_games=1, num_of_pieces_in_game=NUM_OF_PIECES):
        self.num_of_pieces_in_game = num_of_pieces_in_game
        self.player_1 = player_1
        self.player_2 = player_2
        self.num_of_games = num_of_games
        self.initial_state = GameState()
        self.player_1_starts = player_1_starts_the_game

    def start_game(self):
        for _ in range(self.num_of_games):
            self.run_single_game()

    def run_single_game(self):
        new_game = Game(self.player_1, self.player_2, self.initial_state,
                        self.num_of_pieces_in_game, self.player_1_starts)
        new_game.run()


def main():
    player1 = UserPlayer("Player 1", NUM_OF_PIECES, CellState.GREEN)
    player2 = UserPlayer("Player 2", NUM_OF_PIECES, CellState.BLUE)
    game_manager = GameManager(player1, player2)
    game_manager.start_game()


if __name__ == '__main__':
    main()
