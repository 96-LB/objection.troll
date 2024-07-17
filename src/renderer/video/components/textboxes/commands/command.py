import re
from abc import ABC, abstractmethod
from functools import cached_property

from ....context import Context
from ...component import Component

from typing import ClassVar, Self


class Command(Component, ABC):
    REGEX: ClassVar[re.Pattern[str]] = re.compile(r'\[/([^\]]+)\]')
    SIG: ClassVar[str] = '§'
    COMMANDS: ClassVar[dict[str, type[Self]]] = {}
    
    
    def __init_subclass__(cls, prefix: str):
        Command.COMMANDS[prefix] = cls
        return super().__init_subclass__()
    
    
    @cached_property
    def size(self):
        return 0, 0
    
    
    @cached_property
    def time(self):
        return 0.
    
    
    @cached_property
    def audio(self) -> tuple[tuple[float, str], ...]:
        return ()
    
    
    def draw(self, ctx: Context):
        pass
    
    
    @classmethod
    @abstractmethod
    def from_input(cls, input: str) -> 'Command':
        for prefix, command in Command.COMMANDS.items():
            if input.startswith(prefix):
                return command.from_input(input[len(prefix):].strip())
        raise ValueError(f'Invalid command: {input}')
    
    
    @staticmethod
    def parse(text: str):
        matches: list[str] = re.findall(Command.REGEX, text)
        commands = tuple(Command.from_input(match) for match in matches)
        text = re.sub(Command.REGEX, Command.SIG, text)
        return text, commands
    
    
    @staticmethod
    def clean(text: str):
        return re.sub(Command.REGEX, '', text)
