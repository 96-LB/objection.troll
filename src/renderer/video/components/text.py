from functools import cached_property

from PIL.ImageFont import FreeTypeFont

from ..renderer import Renderer
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
    
    def draw(self, renderer: Renderer, x: int, y: int, time: float, global_time: float):
        if time > 0:
            renderer.draw.text((x, y), self.char, font=self.font, fill='white')
