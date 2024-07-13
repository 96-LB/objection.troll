from functools import cached_property

from PIL.ImageDraw import ImageDraw as Draw

from .component import Component
from .container import Container


class Sequence[T: Component](Container[T]):
    
    @cached_property
    def size(self):
        x, y = 0, 0
        for child in self.children:
            x = max(x, child.size[0])
            y = max(y, child.size[1])
        return x, y
    
    
    def draw(self, draw: Draw, x: int, y: int, time: float, global_time: float):
        for child in self.children:
            child.draw(draw, x, y, time, global_time)
            time -= child.delay
