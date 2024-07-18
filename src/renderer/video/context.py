from functools import cached_property

from PIL import Image, ImageDraw

from util.pod import Pod


class Context(Pod):
    
    width: int
    height: int
    
    x: int
    y: int
    
    time: float
    global_time: float
    
    image: Image.Image
    draw: ImageDraw.ImageDraw
    
    
    @classmethod
    def new(cls, width: int, height: int):
        image = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(image)
        return cls(
            width=width,
            height=height,
            x=0,
            y=0,
            time=0,
            global_time=0,
            image=image,
            draw=draw
        )
    
    
    @cached_property
    def pos(self):
        return self.x, self.y
    
    
    def rectangle(self, x1: int, y1: int, x2: int, y2: int, rgba: tuple[int, int, int, int]):
        image = Image.new('RGBA', (x2 - x1, y2 - y1), rgba)
        self.image.alpha_composite(image, (x1, y1))
