import utils


class Player:
    def __init__(self, name, is_ai=False):
        self.name = name
        self.is_ai = is_ai
        self.pieces = []

    def make_move(self, board):
        # Define how the player makes a move
        pass

    def get_possible_actions(self, board):
        all_possible_actions = []
        for piece in self.pieces:
            curr_piece_poss_moves = piece.get_possible_moves(board)
            for move in curr_piece_poss_moves:
                correlated_action = utils.convert_move_to_action(desired_move=move, piece_position=piece.position)
                all_possible_actions.append(correlated_action)
        return all_possible_actions
