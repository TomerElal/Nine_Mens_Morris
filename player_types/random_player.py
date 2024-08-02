import random
import time

from player import Player
from move import MoveType
from strings import *


class RandomPlayer(Player):

    def get_action(self, state, type_of_required_action=MoveType.MOVE_PIECE):

        if type_of_required_action == MoveType.MOVE_PIECE:
            print(RANDOM_CHOOSE_MOVEMENT)
            time.sleep(TIME_TO_SLEEP)
            result = random.choice(self.get_possible_move_pieces_actions(game_state=state))
            print_result = RANDOM_MOVED_PIECE + str(result[0]) + TO_LOCATION + str(
                result[1]) + Style.RESET_ALL + SEPERATOR

        elif type_of_required_action == MoveType.PLACE_PIECE:
            print(RANDOM_CHOOSE_PLACEMENT)
            time.sleep(TIME_TO_SLEEP)
            result = random.choice(self.get_possible_piece_placements(game_state=state))
            print_result = RANDOM_PLACED_PIECE + str(result) + Style.RESET_ALL + SEPERATOR

        else:
            print(RANDOM_CHOOSE_REMOVAL)
            time.sleep(TIME_TO_SLEEP)
            result = random.choice(self.get_possible_opponent_remove_pieces(game_state=state))
            print_result = RANDOM_REMOVED_PIECE + str(result) + Style.RESET_ALL + SEPERATOR

        print(print_result)
        return result
