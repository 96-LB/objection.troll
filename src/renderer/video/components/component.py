from abc import ABC, abstractmethod

from PIL.ImageDraw import ImageDraw as Draw

from util.pod import Pod


class Component(Pod, ABC):
    @property
    @abstractmethod
    def size(self) -> tuple[float, float]:
        ...
    
    @property
    @abstractmethod
    def delay(self) -> float:
        ...
    
    @property
    @abstractmethod
    def time(self) -> float:
        ...
    
    @property
    @abstractmethod
    def audio(self) -> tuple[tuple[float, str], ...]:
        ...
    
    @abstractmethod
    def draw(self, draw: Draw, x: float, y: float, time: float, global_time: float):
        ...
    
