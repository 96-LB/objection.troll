from PIL.ImageDraw import ImageDraw as Draw

from .component import Component


class Container[T: Component](Component):
    children: tuple[T, ...]
    
    
    @property
    def size(self):
        x, y = 0, 0
        for child in self.children:
            x += child.size[0]
            y += child.size[1]
        return x, y
    
    
    @property
    def delay(self):
        return sum(child.delay for child in self.children)
    
    
    @property
    def time(self):
        if not self.children:
            return 0
        return sum(child.delay for child in self.children[:-1]) + self.children[-1].time
    
    
    def draw(self, draw: Draw, x: float, y: float, time: float, global_time: float):
        for child in self.children:
            child.draw(draw, x, y, time, global_time)
            time -= child.delay
            x += child.size[0]
            y += child.size[1]
    
    
    @property
    def audio(self) -> tuple[tuple[float, str], ...]:
        return sum((child.audio for child in self.children), ())
