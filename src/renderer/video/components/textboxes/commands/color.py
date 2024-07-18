from ..char import Char
from .command import Command


class ColorCommand(Command, prefix='c'):
    color: tuple[int, int, int]
    
    @classmethod
    def from_input(cls, input: str):
        try:
            return cls({
                'w': (255, 255, 255),
                'r': (255, 0, 0),
                'g': (0, 255, 0),
                'b': (0, 0, 255),
            }[input])
        except KeyError:
            raise ValueError(f'Invalid color: {input}')
    
    def get_char(self, prev: Char):
        return super().get_char(prev).but(color=self.color)
