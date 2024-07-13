from PIL import Image, ImageDraw

from .frame import Frame
from .sequence import Sequence


class Scene(Sequence[Frame]):
    def render_frame(self, time: float):
        image = Image.new('RGBA', self.size, (0, 0, 0, 0))
        draw = ImageDraw.Draw(image)
        self.draw(draw, 0, 0, time, time)
        return image
