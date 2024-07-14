from math import ceil

from ..context import Context
from .frame import Frame
from .sequence import Sequence


class Scene(Sequence[Frame]):
    
    def render_frame(self, time: float):
        ctx = Context.new(*self.size).but(time=time)
        self.draw(ctx)
        return ctx.image
    
    
    def render_frames(self, fps: float):
        for time in range(ceil(self.time * fps)):
            yield self.render_frame(time / fps)
