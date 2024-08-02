# exceptions/uncorrelated_piece_color_exception.py

from utils.strings import UNCORRELATED_PIECE_COLOR_DEFAULT_MESSAGE


class UnCorrelatedPieceColor(Exception):
    def __init__(self, message=UNCORRELATED_PIECE_COLOR_DEFAULT_MESSAGE):
        self.message = message
        super().__init__(self.message)
