from functools import cached_property

from .component import Component
from .container import Container
from video.renderer import Renderer


class Sequence[T: Component](Container[T]):
    
    @cached_property
    def size(self):
        x, y = 0, 0
        for child in self.children:
            x = max(x, child.size[0])
            y = max(y, child.size[1])
        return x, y
    
    
    def draw(self, renderer: Renderer, x: int, y: int, time: float, global_time: float):
        for child in self.children:
            child.draw(renderer, x, y, time, global_time)
            time -= child.delay
