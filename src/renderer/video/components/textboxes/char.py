from functools import cached_property

from PIL import ImageFont

from ...context import Context
from ..component import Component

from typing import Self


class Char(Component):
    char: str
    next: str # used for kerning
    
    text_speed: float
    pause: float
    color: tuple[int, int, int]
    font: ImageFont.FreeTypeFont
    last_blip: float
        
    
    @classmethod
    def from_input(cls, input: str, prev: Self):
        return cls(
            char=input[0],
            next=input[1] if len(input) > 1 else '',
            text_speed=prev.text_speed,
            pause=prev.pause,
            color=prev.color,
            font=prev.font,
            last_blip=prev.last_blip
        )
    
    
    @cached_property
    def time(self):
        return self.text_speed * len(self.char) + self.pause
    
    
    @cached_property
    def size(self):
        return self.font.getlength(self.char + self.next) - self.font.getlength(self.next), 0
    
    
    @cached_property
    def audio(self):
        BLIP_SPEED = 0.064 # TODO: make a constant for blip speed
        if not self.char.isspace() and BLIP_SPEED - self.last_blip <= self.time:
            return ((max(0, BLIP_SPEED - self.last_blip), 'blip.wav'),)
        return ()
    
    
    def draw(self, ctx: Context):
        if ctx.time > 0:
            ctx.draw.text(ctx.pos, self.char, font=self.font, fill=self.color)
