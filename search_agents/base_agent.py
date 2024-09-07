from abc import ABC, abstractmethod
from enum import Enum


class AgentType(Enum):
    MAX = 1
    MIN = 2
    EXPECTED = 3


class Agent(ABC):
    @abstractmethod
    def get_action(self, game_state):
        raise NotImplementedError()

    @abstractmethod
    def evaluation_function(self, game_state):
        raise NotImplementedError()

    def __init__(self, player_number=1):
        self.player_number = player_number
