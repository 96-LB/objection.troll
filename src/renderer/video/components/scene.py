from math import ceil

from ..renderer import Renderer
from .frame import Frame
from .sequence import Sequence


class Scene(Sequence[Frame]):
    
    def render_frame(self, time: float):
        draw = Renderer(*self.size)
        self.draw(draw, 0, 0, time, time)
        return draw.image
    
    
    def render_frames(self, fps: float):
        for time in range(ceil(self.time * fps)):
            yield self.render_frame(time / fps)
