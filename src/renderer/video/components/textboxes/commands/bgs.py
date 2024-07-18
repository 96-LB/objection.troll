from ..char import Char
from .command import Command
from video.effects import AudioEffect


class BackgroundSoundCommand(Command, prefix='bgs'):
    sound: str
    
    @classmethod
    def from_input(cls, input: str):
        return cls(sound=input + '.wav') # TODO: we probably want to support different types of audio files
    
    def get_char(self, prev: Char):
        return super().get_char(prev).but(fx=(AudioEffect(0, self.sound),))
