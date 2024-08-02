import random
import time

from player import Player
from move import MoveType
from colorama import Style, Fore

SEPERATOR = "\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n"
RANDOM_CHOOSE_MOVEMENT = (SEPERATOR + Fore.LIGHTMAGENTA_EX +
                          "\nIt's time for the Random Player to move a piece.\n"
                          + Style.RESET_ALL + SEPERATOR)
RANDOM_CHOOSE_PLACEMENT = (SEPERATOR + Fore.LIGHTMAGENTA_EX +
                           "\nIt's time for the Random Player choose a place for new piece.\n"
                           + Style.RESET_ALL + SEPERATOR)
RANDOM_CHOOSE_REMOVAL = (SEPERATOR + Fore.LIGHTYELLOW_EX +
                         "\n🚀🚀 It's time for the Random Player to remove opponent's piece! 🚀🚀\n"
                         + Style.RESET_ALL + SEPERATOR)
RANDOM_MOVED_PIECE = SEPERATOR + Fore.LIGHTCYAN_EX + "Random Player chose to move piece from location "
RANDOM_PLACED_PIECE = SEPERATOR + Fore.LIGHTCYAN_EX + "Random Player chose to place a piece at location "
RANDOM_REMOVED_PIECE = SEPERATOR + Fore.LIGHTCYAN_EX + "Random Player chose to remove opponent's piece from location "
TO_LOCATION = " to location "
TIME_TO_SLEEP = 0


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
