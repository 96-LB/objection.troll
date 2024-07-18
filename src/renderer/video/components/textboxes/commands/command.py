import re
from abc import ABC, abstractmethod

from util.pod import Pod

from typing import ClassVar, Generator, Self

from video.components.textboxes.char import Char


class Command(Pod, ABC):
    REGEX: ClassVar[re.Pattern[str]] = re.compile(r'\[/([^\]]+)\]')
    SIG: ClassVar[str] = '§'
    COMMANDS: ClassVar[dict[str, type[Self]]] = {}
    
    
    def __init_subclass__(cls, prefix: str):
        Command.COMMANDS[prefix] = cls
        return super().__init_subclass__()
    
    
    @classmethod
    @abstractmethod
    def from_input(cls, input: str) -> 'Command':
        for prefix, command in Command.COMMANDS.items():
            if input.startswith(prefix):
                return command.from_input(input[len(prefix):].strip())
    
    
    def get_char(self, prev: Char):
        return Char.from_input('', prev)
    
    
    @staticmethod
    def parse(text: str):
        matches: list[str] = re.findall(Command.REGEX, text)
        commands = tuple(Command.from_input(match) for match in matches)
        text = re.sub(Command.REGEX, Command.SIG, text)
        return text, commands
    
    
    @staticmethod
    def clean(text: str):
        return re.sub(Command.REGEX, '', text)
    
    
    @staticmethod
    def text_indices(text: str) -> Generator[int, None, None]:
        i = 0
        matches = re.finditer(Command.REGEX, text)
        for match in matches:
            yield from range(i, match.start())
            i = match.end()
        yield from range(i, len(text))
