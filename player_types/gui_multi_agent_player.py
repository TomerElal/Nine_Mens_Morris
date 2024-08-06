from src.player import Player


class GuiMultiAgentsPlayer(Player):

    def __init__(self, name, initial_num_of_pieces, player_color, agent, is_computer_player):
        super().__init__(name, initial_num_of_pieces, player_color, is_computer_player)
        self.search_agent = agent

    def get_action(self, state, type_of_required_action, events=None, pieces=None, selected_position=None):

        return self.search_agent.get_action(state), True

