from ..char import Char
from .command import Command


class PauseCommand(Command, prefix='p'):
    pause: float
    
    @classmethod
    def from_input(cls, input: str):
        return cls(float(input) / 1000)
    
    def get_char(self, prev: Char):
        return super().get_char(prev).but(pause=self.pause)
