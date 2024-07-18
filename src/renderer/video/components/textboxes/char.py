from functools import cached_property

from PIL import ImageFont

from video.components import Component
from video.context import Context
from video.effects import AudioEffect

from typing import Self


class Char(Component):
    # transient attributes
    char: str
    next: str # used for kerning
    sound: str
    pause: float
    
    # persistent attributes
    text_speed: float
    color: tuple[int, int, int]
    font: ImageFont.FreeTypeFont
    last_blip: float
    
    
    @classmethod
    def from_input(cls, input: str, prev: Self):
        return prev.but(
            char=input[0] if input else '',
            next=input[1] if len(input) > 1 else '',
            sound='',
            pause=0,
            last_blip=prev.time - prev.blip if prev.blip >= 0 else prev.last_blip + prev.time
        )
    
    
    @cached_property
    def time(self):
        return self.text_speed * len(self.char) + self.pause
    
    
    @cached_property
    def size(self):
        return self.font.getlength(self.char + self.next) - self.font.getlength(self.next), 0
    
    
    @cached_property
    def effects(self):
        fx = ()
        if self.sound:
            fx += (AudioEffect(self.time, self.sound),)
        if self.blip >= 0:
            fx += (AudioEffect(self.blip, 'blip.wav'),)
        return fx
    
    
    @cached_property
    def blip(self):
        BLIP_SPEED = 0.064
        if self.char.strip() and BLIP_SPEED - self.last_blip <= self.time:
            return max(0, BLIP_SPEED - self.last_blip)
        return -self.last_blip
    
    
    def draw(self, ctx: Context):
        if ctx.time > 0:
            ctx.draw.text(ctx.pos, self.char, font=self.font, fill=self.color)
