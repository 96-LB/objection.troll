 # TODO: ERIC: create ShakeCommand
from ..char import Char
from .command import Command
from video.effects import ShakeEffect


class ShakeCommand(Command, prefix = "s"):

    length: float
    
    @classmethod
    def from_input(cls, input: str):
        return cls({
            'l': .5,
            'm': .25,
            's': .1,
        }.get(input) or float(input) / 1000)
    
    def get_char(self, prev: Char):
        return super().get_char(prev).but(fx=(ShakeEffect(0, self.length),))
