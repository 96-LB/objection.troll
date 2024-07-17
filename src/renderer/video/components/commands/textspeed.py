from functools import cached_property

from .command import Command


class TextSpeedCommand(Command, prefix='ts'):
    
    @cached_property
    def data(self):
        return float(self.input) / 1000
