from abc import ABC, abstractmethod
from functools import cached_property

from ..context import Context
from util.pod import Pod


class Component(Pod, ABC):
    @cached_property
    @abstractmethod
    def size(self) -> tuple[float, float]:
        ...
    
    @cached_property
    @abstractmethod
    def time(self) -> float:
        ...
    
    @cached_property
    @abstractmethod
    def audio(self) -> tuple[tuple[float, str], ...]:
        ...
    
    @abstractmethod
    def draw(self, ctx: Context):
        ...
