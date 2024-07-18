from functools import cached_property

from .component import Component
from util.pod import PList
from video.context import Context
from video.effects import Effect


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
    def effects(self):
        fx: list[Effect] = []
        time = 0
        for child in self.children:
            for effect in child.effects:
                fx.append(effect.plus_time(time))
            time += child.time
        return tuple(fx)
    
    
    def draw(self, ctx: Context):
        for child in self.children:
            child.draw(ctx)
            ctx = ctx.plus(time=-child.time, x=child.size[0], y=child.size[1])
