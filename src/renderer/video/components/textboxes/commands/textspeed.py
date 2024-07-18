from ..char import Char
from .command import Command


class TextSpeedCommand(Command, prefix='ts'):
    speed: float
    
    @classmethod
    def from_input(cls, input: str):
        return cls(float(input) / 1000)
    
    def get_char(self, prev: Char):
        return super().get_char(prev).but(text_speed=self.speed)
