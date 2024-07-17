from functools import cached_property

from .command import Command


class BackgroundSoundCommand(Command, prefix='bgs'):
    
    @cached_property
    def data(self):
        return self.input + '.wav' # TODO: we probably want to support different types of audio files
