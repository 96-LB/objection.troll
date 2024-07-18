from functools import cached_property

from ..context import Context
from .component import Component
from .gif import Gif


class Character(Component):
    pre: Gif
    idle: Gif
    talk: Gif
    bgs: str
    
    @cached_property
    def size(self):
        return 0, 0
    
    
    @cached_property
    def time(self):
        return self.pre.time
    
    
    @cached_property
    def audio(self):
        return ((0, self.bgs),) if self.bgs else ()
    
    
    def draw(self, ctx: Context, talking: bool = False):
        if talking:
            self.talk.draw(ctx)
        else:
            self.idle.draw(ctx)
