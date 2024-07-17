from functools import cached_property

from ..context import Context
from .character import Character
from .component import Component
from .gif import Gif
from .textboxes import Textbox
from util.pod import PList


class Frame(Component):
    width: int
    height: int
    
    textbox: Textbox
    
    character: PList[Character]
    active_character: int
    
    background: Gif
    foreground: Gif
    
    
    @cached_property
    def size(self):
        return self.width, self.height
        
    
    @cached_property
    def time(self):
        return self.textbox.time + 0.75
    
    
    @cached_property
    def audio(self) -> tuple[tuple[float, str], ...]:
        return self.textbox.audio
    
    
    def draw(self, ctx: Context):
        if not 0 <= ctx.time < self.time:
            return
        
        self.background.draw(ctx)
        for character in self.character:
            character.draw(ctx)
        self.foreground.draw(ctx)
        self.textbox.draw(ctx)
