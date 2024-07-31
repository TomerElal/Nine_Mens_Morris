# exceptions/uncorrelated_piece_color_exception.py

class UnCorrelatedPieceColor(Exception):
    def __init__(self, message="The piece color does not match the expected color"):
        self.message = message
        super().__init__(self.message)
