from enum import Enum


class Move(Enum):
    UP = 1
    DOWN = 2
    LEFT = 3
    RIGHT = 4
    STOP = 5


class MoveType(Enum):
    PLACE_PIECE = 1
    MOVE_PIECE = 2
    REMOVE_OPPONENT_PIECE = 3

