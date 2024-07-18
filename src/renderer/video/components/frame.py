from functools import cached_property


from ..context import Context
from .character import Character
from .component import Component
from .gif import Gif
from .textboxes import Textbox
from .textboxes.char import Char
from .textboxes.commands.pause import PauseCommand
from util.pod import PList


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
    def audio(self) -> tuple[tuple[float, str], ...]:
        return self.character.audio + tuple((t + self.character.time, a) for t, a in self.textbox.audio)
    
    
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
                if isinstance(char, (Char, PauseCommand)) and char.pause:
                    if talking:
                        talking = False
                        talk = 0
                elif not talking:
                    talking = True
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
