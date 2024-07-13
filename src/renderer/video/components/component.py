from abc import ABC, abstractmethod
from functools import cached_property

from util.pod import Pod
from util.renderer import Renderer


class Component(Pod, ABC):
    @cached_property
    @abstractmethod
    def size(self) -> tuple[int, int]:
        ...
    
    @cached_property
    @abstractmethod
    def delay(self) -> float:
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
    def draw(self, draw: Renderer, x: int, y: int, time: float, global_time: float):
        ...
    
