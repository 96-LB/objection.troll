from ..char import Char
from .command import Command
from video.effects import FlashEffect


class FlashCommand(Command, prefix='f'):
    length: float
    
    @classmethod
    def from_input(cls, input: str):
        return cls({
            'l': .5,
            'm': .25,
            's': .1,
        }.get(input) or float(input) / 1000)
    
    def get_char(self, prev: Char):
        return super().get_char(prev).but(fx=(FlashEffect(0, self.length),))
