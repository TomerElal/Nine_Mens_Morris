import time

from src.player import Player
from src.move import MoveType
from utils.strings import *


class MinimaxPlayer(Player):

    def __init__(self, name, initial_num_of_pieces, player_color, agent):
        super().__init__(name, initial_num_of_pieces, player_color)
        self.search_agent = agent

    def get_action(self, state, type_of_required_action=MoveType.MOVE_PIECE):
        result = self.search_agent.get_action(state)
        if type_of_required_action == MoveType.MOVE_PIECE:
            print(MINIMAX_CHOOSE_MOVEMENT)
            time.sleep(TIME_TO_SLEEP)
            print_result = MINIMAX_MOVED_PIECE + str(result[0]) + TO_LOCATION + str(
                result[1]) + Style.RESET_ALL + SEPERATOR

        elif type_of_required_action == MoveType.PLACE_PIECE:
            print(MINIMAX_CHOOSE_PLACEMENT)
            time.sleep(TIME_TO_SLEEP)
            print_result = MINIMAX_PLACED_PIECE + str(result) + Style.RESET_ALL + SEPERATOR

        else:
            print(MINIMAX_CHOOSE_REMOVAL)
            time.sleep(TIME_TO_SLEEP)
            print_result = MINIMAX_REMOVED_PIECE + str(result) + Style.RESET_ALL + SEPERATOR

        print(print_result)
        return result
