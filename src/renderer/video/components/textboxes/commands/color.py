from .command import Command


class ColorCommand(Command, prefix='c'):
    color: tuple[int, int, int]
    
    @classmethod
    def from_input(cls, input: str):
        match input:
            case 'w':
                return cls((255, 255, 255))
            case 'r':
                return cls((255, 0, 0))
            case 'g':
                return cls((0, 255, 0))
            case 'b':
                return cls((0, 0, 255))
            case _:
                raise ValueError(f'Invalid color: {input}')
