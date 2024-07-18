from math import ceil

from .frame import Frame
from .sequence import Sequence
from video.context import Context


class Scene(Sequence[Frame]):
    
    def render_frame(self, time: float):
        ctx = Context.new(ceil(self.size[0]), ceil(self.size[1])).but(time=time)
        self.draw(ctx)
        return ctx.image
    
    
    def render_frames(self, fps: float):
        for time in range(ceil(self.time * fps)):
            yield self.render_frame(time / fps)
