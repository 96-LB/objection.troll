from .textbox import Textbox
from video.context import Context

from PIL import ImageFont


FONT = ImageFont.truetype('aa.otf', 24)
class TrilogyTextbox(Textbox, x=120, y=496, width=740, line_height=32, font=FONT):
    
    def draw(self, ctx: Context):
        if ctx.time > 0:
            ctx.draw.rectangle((0, 480, 960, 608), fill=(0, 32, 64, 255), outline=(0, 64, 128, 255))
        super().draw(ctx)
