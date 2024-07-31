import random

from player import Player
from move import MoveType


class RandomPlayer(Player):

    def get_action(self, state, type_of_required_action=MoveType.MOVE_PIECE):

        if type_of_required_action == MoveType.MOVE_PIECE:
            return random.choice(self.get_possible_move_pieces_actions(game_state=state))

        elif type_of_required_action == MoveType.PLACE_PIECE:
            return random.choice(self.get_possible_piece_placements(game_state=state))

        return random.choice(self.get_possible_opponent_remove_pieces(game_state=state))
