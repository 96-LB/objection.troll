from functools import cached_property

from PIL.ImageFont import FreeTypeFont

from ..context import Context
from .component import Component


class Text(Component):
    char: str
    font: FreeTypeFont
    textspeed: float
    
    
    @cached_property
    def size(self):
        return int(self.font.getlength(self.char)), 0
    
    @cached_property
    def delay(self):
        delay = self.textspeed
        if self.char in ('.', '!', '?', '—', ';'): # TODO: this needs to be context-aware
            delay += 0.25
        elif self.char in (',', '-', ':'):
            delay += 0.1
        return delay
    
    @cached_property
    def time(self):
        return 0
    
    @cached_property
    def audio(self):
        return () # TODO: text blips
    
    def draw(self, ctx: Context):
        if ctx.time > 0:
            ctx.draw.text(ctx.pos, self.char, font=self.font, fill='white')
