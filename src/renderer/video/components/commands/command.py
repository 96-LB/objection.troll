import re
from abc import ABC, abstractmethod
from functools import cached_property

from util.pod import Pod

from typing import ClassVar, Self


class Command(Pod, ABC):
    input: str
    
    REGEX: ClassVar[re.Pattern[str]] = re.compile(r'\[/([^\]]+)\]')
    SIG: ClassVar[str] = '§'
    COMMANDS: ClassVar[dict[str, type[Self]]] = {}
    
    
    def __init_subclass__(cls, prefix: str):
        Command.COMMANDS[prefix] = cls
        return super().__init_subclass__()
    
    
    def __post_init__(self):
        self.data # load the data immediately to catch errors
    
    
    @cached_property
    @abstractmethod
    def data(self) -> object:
        ...
    
    
    @classmethod
    def get_command(cls, command_str: str) -> Self:
        for prefix, command in cls.COMMANDS.items():
            if command_str.startswith(prefix):
                return command(command_str[len(prefix):].strip())
        raise ValueError(f'Invalid command: {command_str}')
    
    
    @classmethod
    def parse_commands(cls, text: str) -> tuple[str, tuple[Self, ...]]:
        matches: list[str] = re.findall(cls.REGEX, text)
        commands = tuple(cls.get_command(match) for match in matches)
        text = re.sub(cls.REGEX, cls.SIG, text)
        return text, commands
