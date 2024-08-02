import time

from player import Player
from move import MoveType
from colorama import Style, Fore

SEPERATOR = "\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n"
MINIMAX_CHOOSE_MOVEMENT = (SEPERATOR + Fore.LIGHTMAGENTA_EX +
                           "\nIt's time for the Minimax Player to move a piece.\n"
                           + Style.RESET_ALL + SEPERATOR)
MINIMAX_CHOOSE_PLACEMENT = (SEPERATOR + Fore.LIGHTMAGENTA_EX +
                            "\nIt's time for the Minimax Player choose a place for new piece.\n"
                            + Style.RESET_ALL + SEPERATOR)
MINIMAX_CHOOSE_REMOVAL = (SEPERATOR + Fore.LIGHTYELLOW_EX +
                          "\n🚀🚀 It's time for the Minimax Player to remove opponent's piece! 🚀🚀\n"
                          + Style.RESET_ALL + SEPERATOR)
MINIMAX_MOVED_PIECE = SEPERATOR + Fore.LIGHTCYAN_EX + "Minimax Player chose to move piece from location "
MINIMAX_PLACED_PIECE = SEPERATOR + Fore.LIGHTCYAN_EX + "Minimax Player chose to place a piece at location "
MINIMAX_REMOVED_PIECE = SEPERATOR + Fore.LIGHTCYAN_EX + "Minimax Player chose to remove opponent's piece from location "
TO_LOCATION = " to location "
TIME_TO_SLEEP = 0


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
