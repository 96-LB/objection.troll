from functools import cached_property

from ..context import Context
from .component import Component
from util.pod import PList


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
    def time(self):
        return sum(child.time for child in self.children)
    
    
    @cached_property
    def audio(self) -> tuple[tuple[float, str], ...]:
        audio = []
        time = 0
        for child in self.children:
            for t, a in child.audio:
                audio.append((time + t, a))
            time += child.time
        return tuple(audio)
    
    
    def draw(self, ctx: Context):
        for child in self.children:
            child.draw(ctx)
            ctx = ctx.plus(time=-child.time, x=child.size[0], y=child.size[1])
