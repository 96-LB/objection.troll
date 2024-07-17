from functools import cached_property

from PIL import ImageFont

from ...context import Context
from ..component import Component


class Char(Component):
    char: str
    next: str # used for kerning
    
    delay: float
    color: tuple[int, int, int]
    font: ImageFont.FreeTypeFont
    last_blip: float
    
    
    @cached_property
    def time(self):
        return self.delay
    
    
    @cached_property
    def size(self):
        return self.font.getlength(self.char + self.next) - self.font.getlength(self.next), 0
    
    
    @cached_property
    def audio(self):
        BLIP_SPEED = 0.064 # TODO: make a constant for blip speed
        if BLIP_SPEED - self.last_blip <= self.time:
            return ((max(0, BLIP_SPEED - self.last_blip), 'blip.wav'),)
        return ()
    
    
    def draw(self, ctx: Context):
        if ctx.time > 0:
            ctx.draw.text(ctx.pos, self.char, font=self.font, fill=self.color)
