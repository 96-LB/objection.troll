from functools import cached_property

from PIL.ImageDraw import ImageDraw as Draw

from .component import Component
from .gif import Gif
from .scratch import Textbox, Character
from util.pod.plist import PList


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
        return 0
    
    
    @cached_property
    def audio(self):
        return ()
    
    
    def draw(self, draw: Draw, x: int, y: int, time: float, global_time: float):
        self.background.draw(draw, x, y, time, global_time)
        #self.textbox.draw(draw, x, y, time, global_time)
        #for character in self.character:
        #    character.draw(draw, x, y, time, global_time)
        #self.foreground.draw(draw, x, y, time, global_time)
