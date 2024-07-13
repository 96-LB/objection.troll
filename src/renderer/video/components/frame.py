from functools import cached_property

from ..renderer import Renderer
from .character import Character
from .component import Component
from .gif import Gif
from .scratch import Textbox
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
    def delay(self):
        return 0
    
    
    @cached_property
    def time(self):
        return 5
    
    
    @cached_property
    def audio(self) -> tuple[tuple[float, str], ...]:
        return ()
    
    
    def draw(self, draw: Renderer, x: int, y: int, time: float, global_time: float):
        self.background.draw(draw, x, y, time, global_time)
        #self.textbox.draw(draw, x, y, time, global_time)
        #for character in self.character:
        #    character.draw(draw, x, y, time, global_time)
        self.foreground.draw(draw, x, y, time, global_time)
