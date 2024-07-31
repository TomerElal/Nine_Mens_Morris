from board import Board
from player import Player

class Game:
    def __init__(self):
        self.board = Board()
        self.players = [Player("Player 1"), Player("Player 2")]
        self.current_turn = 0

    def start_game(self):
        # Start the game loop
        pass

    def check_winner(self):
        # Check if there is a winner
        pass

    def switch_turn(self):
        self.current_turn = 1 - self.current_turn

    def is_valid_move(self, move):
        # Validate the move
        pass