from functools import cached_property

from .command import Command


class PauseCommand(Command, prefix='p'):
    
    @cached_property
    def data(self):
        return float(self.input) / 1000
