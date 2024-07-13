from functools import cached_property

from .component import Component
from .gif import Gif
from .scratch import Textbox, Character
from util.pod import PList
from util.renderer import Renderer


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
        return 10
    
    
    @cached_property
    def audio(self):
        return ()
    
    
    def draw(self, draw: Renderer, x: int, y: int, time: float, global_time: float):
        self.background.draw(draw, x, y, time, global_time)
        #self.textbox.draw(draw, x, y, time, global_time)
        #for character in self.character:
        #    character.draw(draw, x, y, time, global_time)
        self.foreground.draw(draw, x, y, time, global_time)
