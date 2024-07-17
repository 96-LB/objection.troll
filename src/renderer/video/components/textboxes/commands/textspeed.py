from .command import Command


class TextSpeedCommand(Command, prefix='ts'):
    data: float
    
    @classmethod
    def from_input(cls, input: str):
        return cls(float(input) / 1000)
