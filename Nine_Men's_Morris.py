from game_state import GameState, CellState
from game import Game
from player_types.user_player import UserPlayer
from move import MoveType
from player_types.random_player import RandomPlayer
from player_types.minimax_player import MinimaxPlayer
from search_agents.minimax_agent import MiniMaxAgent

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

    user_player1 = UserPlayer("Player 1", NUM_OF_PIECES, CellState.GREEN)
    user_player2 = UserPlayer("Player 2", NUM_OF_PIECES, CellState.BLUE)

    minimax_agent = MiniMaxAgent()
    minimax_player = MinimaxPlayer("Minimax Player", NUM_OF_PIECES, CellState.GREEN, minimax_agent)
    random_player = RandomPlayer("Random Player", NUM_OF_PIECES, CellState.BLUE)

    game_manager = GameManager(player_1=minimax_player, player_2=random_player)
    game_manager.start_game()


if __name__ == '__main__':
    main()
