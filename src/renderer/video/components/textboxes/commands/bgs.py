from functools import cached_property

from .command import Command


class BackgroundSoundCommand(Command, prefix='bgs'):
    sound: str
    
    @classmethod
    def from_input(cls, input: str):
        return cls(sound=input + '.wav') # TODO: we probably want to support different types of audio files
    
    
    @cached_property
    def audio(self):
        return ((0, self.sound),)
