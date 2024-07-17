from functools import cached_property

from .command import Command


class PauseCommand(Command, prefix='p'):
    pause: float
    
    @classmethod
    def from_input(cls, input: str):
        return cls(float(input) / 1000)
    
    
    @cached_property
    def time(self):
        return self.pause
