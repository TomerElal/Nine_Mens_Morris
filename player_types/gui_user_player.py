import pygame

from src.player import Player
from src.move import MoveType
from utils.utils import get_piece_position_in_gui


class GuiUserPlayer(Player):

    def get_action(self, state, type_of_required_action, events=None, pieces=None, selected_position=None):

        possible_actions = self.get_possible_actions(state, type_of_required_action, selected_position)
        selected_position = None
        should_relevant_pieces_flash = (type_of_required_action == MoveType.PLACE_PIECE or
                                        type_of_required_action == MoveType.MOVE_SELECTED_PIECE)

        for event in events:

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos

                if type_of_required_action == MoveType.PLACE_PIECE:
                    for spot in possible_actions:
                        spot_position = get_piece_position_in_gui(spot[0], spot[1])
                        if pygame.Rect(spot_position[0] - 30, spot_position[1] - 30, 60, 60).collidepoint(mouse_pos):
                            selected_position = spot
                            break

                elif type_of_required_action == MoveType.SELECT_PIECE_TO_MOVE:
                    for index_location, piece in pieces.items():
                        if piece['rect'].collidepoint(mouse_pos):
                            if index_location in possible_actions:
                                selected_position = index_location
                            break  # Means the user clicked on invalid spot.

                else:
                    for valid_position in possible_actions:
                        gui_position = get_piece_position_in_gui(valid_position[0], valid_position[1])
                        if pygame.Rect(gui_position[0] - 30, gui_position[1] - 30, 60, 60).collidepoint(mouse_pos):
                            selected_position = valid_position
                            break


        return selected_position, should_relevant_pieces_flash
