from functools import cached_property

from .component import Component
from .gif import Gif
from util.pod import PList
from video.context import Context
from video.effects import Effect


class Character(Component):
    pre: Gif
    idle: Gif
    talk: Gif
    fx: PList[Effect]
    x: int
    y: int

    
    @cached_property
    def size(self):
        return 0, 0
    
    
    @cached_property
    def time(self):
        return self.pre.time
    
    
    @cached_property
    def effects(self):
        return self.fx
    
    

    def draw(self, ctx: Context, talking: bool = False):
        ctx = ctx.plus(x=self.x, y=self.y)
        if talking:
            self.talk.draw(ctx)
        else:
            self.idle.draw(ctx)
