from functools import cached_property

from ..context import Context
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
    
    
    def draw(self, ctx: Context):
        for child in self.children:
            child.draw(ctx)
            ctx = ctx.plus(time=-child.time)
