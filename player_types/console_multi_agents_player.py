import time

from src.player import Player
from src.move import MoveType
from utils.strings import *
from utils.utils import perform_placement_or_remove_action_to_console, perform_move_action_to_console


class MultiAgentsPlayer(Player):

    def __init__(self, name, initial_num_of_pieces, player_color, agent, is_computer_player):
        super().__init__(name, initial_num_of_pieces, player_color, is_computer_player)
        self.search_agent = agent

    def get_action(self, state, type_of_required_action=MoveType.MOVE_PIECE, events=None):

        result = self.search_agent.get_action(state)

        if type_of_required_action == MoveType.MOVE_PIECE:
            print_result = perform_move_action_to_console(PLAYER_CHOOSE_MOVEMENT, self.name,
                                                          PLAYER_MOVED_PIECE, result)

        elif type_of_required_action == MoveType.PLACE_PIECE:
            print_result = perform_placement_or_remove_action_to_console(PLAYER_CHOOSE_PLACEMENT, self.name,
                                                                         PLAYER_PLACED_PIECE, result)

        else:
            print_result = perform_placement_or_remove_action_to_console(PLAYER_CHOOSE_REMOVAL, self.name,
                                                                         PLAYER_REMOVED_PIECE, result)

        print(print_result)
        return result
