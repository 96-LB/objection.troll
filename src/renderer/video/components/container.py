from functools import cached_property

from PIL.ImageDraw import ImageDraw as Draw

from .component import Component
from util.pod.plist import PList


class Container[T: Component](Component):
    children: PList[T]
    
    @cached_property
    def size(self):
        x, y = 0, 0
        for child in self.children:
            x += child.size[0]
            y += child.size[1]
        return x, y
        
        
    @cached_property
    def delay(self):
        return sum(child.delay for child in self.children)
    
    
    @cached_property
    def time(self):
        if not self.children:
            return 0
        return sum(child.delay for child in self.children) - self.children[-1].delay + self.children[-1].time
    
    
    @cached_property
    def audio(self) -> tuple[tuple[float, str], ...]:
        return sum((child.audio for child in self.children), ())
    
    
    def draw(self, draw: Draw, x: int, y: int, time: float, global_time: float):
        for child in self.children:
            child.draw(draw, x, y, time, global_time)
            time -= child.delay
            x += child.size[0]
            y += child.size[1]
