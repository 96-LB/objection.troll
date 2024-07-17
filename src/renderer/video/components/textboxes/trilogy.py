from ...context import Context
from .textbox import Textbox

from PIL import ImageFont


FONT = ImageFont.truetype('aa.otf', 32)
class TrilogyTextbox(Textbox, x=380, y=880, width=1160, line_height=48, font=FONT, blip_speed=0.064):
    
    def draw(self, ctx: Context):
        ctx.draw.rectangle((0, 860, 1920, 1040), fill=(0, 32, 64, 255), outline=(0, 64, 128, 255))
        super().draw(ctx)
