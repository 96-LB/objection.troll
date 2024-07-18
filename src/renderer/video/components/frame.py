import math
from functools import cached_property

from .character import Character
from .component import Component
from .gif import Gif
from .textboxes import Textbox
from util.pod import PList
from video.context import Context
from video.effects import FlashEffect


class Frame(Component):
    width: int
    height: int
    
    textbox: Textbox
    
    characters: PList[Character]
    active_index: int
    
    background: Gif
    foreground: Gif
    
    
    @cached_property
    def character(self):
        return self.characters[self.active_index]
    
    
    @cached_property
    def size(self):
        return self.width, self.height
        
    
    @cached_property
    def time(self):
        return self.character.time + self.textbox.time + 0.75
    
    
    @cached_property
    def effects(self):
        return self.character.effects + tuple(effect.plus_time(self.character.time) for effect in self.textbox.effects)
    
    
    def draw(self, ctx: Context):
        if not 0 <= ctx.time < self.time:
            return
        
        # TODO: move this calculation to the textbox
        # determine how long the character's been talking/idling
        time = ctx.time - self.character.time
        talking = True
        talk = 0
        for line in self.textbox.children:
            if time < 0:
                break
            for char in line.children:
                if bool(char.pause) == talking:
                    talking = not talking
                    talk = 0

                time -= char.time
                talk += char.time
                if time < 0:
                    talk += time
                    break
        talk += max(0, time)
        
        self.background.draw(ctx)
        for i, character in enumerate(self.characters):
            if i == self.active_index:
                if ctx.time < self.character.time:
                    character.pre.draw(ctx)
                else:
                    character.draw(ctx.but(time=talk), talking=talking)
            else:
                character.draw(ctx)
        self.foreground.draw(ctx)
        self.textbox.draw(ctx.plus(time=-self.character.time))
        
        for effect in self.effects:
            if isinstance(effect, FlashEffect):
                if effect.time <= ctx.time < effect.time + effect.length:
                    t = 1 - (ctx.time - effect.time) / effect.length
                    a = int(math.sin(t**2 * math.pi/2) * 255) # calculate alpha # TODO: this formula is kinda bad
                    ctx.rectangle(0, 0, self.width, self.height, (255, 255, 255, a))
