from abc import abstractmethod
from functools import cached_property

from PIL import ImageFont

from ...context import Context
from ..commands import Command, TextSpeedCommand, PauseCommand, BackgroundSoundCommand
from ..component import Component

from typing import ClassVar


class Textbox(Component):
    x: ClassVar[int]
    y: ClassVar[int]
    width: ClassVar[int]
    line_height: ClassVar[int]
    font: ClassVar[ImageFont.FreeTypeFont]
    blip_speed: ClassVar[float]
    
    input: str
    
    
    def __init_subclass__(cls, x: int, y: int, width: int, line_height: int, font: ImageFont.FreeTypeFont, blip_speed: float):
        cls.x = x
        cls.y = y
        cls.width = width
        cls.line_height = line_height
        cls.font = font
        cls.blip_speed = blip_speed
        return super().__init_subclass__()
    
    
    @cached_property
    def _parsed(self):
        return Command.parse_commands(self.input)
    
    
    @cached_property
    def text(self):
        def split_lines(text: str) -> str:
            saved = 0
            for i in range(len(text)):
                if text[i] == '\n':
                    return text[:i + 1] + split_lines(text[i + 1:])
                elif text[i].isspace():
                    saved = i
                elif self.font.getlength(text[:i + 1]) > self.width:
                    return text[:saved or i] + '\n' + split_lines(text[(saved or i) + 1:])
            return text
        
        return split_lines(self._parsed[0])
    
    
    @cached_property
    def commands(self) -> tuple[Command, ...]:
        return self._parsed[1]
    
    
    def display(self, *, max_time: float = float('inf')):
        text = ''
        time = 0
        c = 0
        delay = 0.03
        audio: list[tuple[float, str]] = []
        blip = -self.blip_speed
        for char in self.text:
            if time >= max_time:
                break
            
            if char == Command.SIG:
                command = self.commands[c]
                if isinstance(command, TextSpeedCommand):
                    delay = command.data
                elif isinstance(command, PauseCommand):
                    time += command.data
                elif isinstance(command, BackgroundSoundCommand):
                    audio.append((time, command.data))
                
                c += 1
                continue
            
            if char.isspace():
                if any(text.endswith(c) for c in ('.', '!', '?', '—', ';')):
                    if not any(text.lower().endswith(c) for c in ('mr.', 'mrs.', 'ms.', 'dr.', 'prof.')):
                        time += 0.25
                elif any(text.endswith(c) for c in (',', '-', ':')):
                    if not text == '--':
                        time += 0.1
            else:
                if time + delay > blip + self.blip_speed:
                    blip = max(time, blip + self.blip_speed)
                    audio.append((blip, 'blip.wav'))
                time += delay
            
            text += char
        
        return text, time, tuple(audio)
    
    
    @cached_property
    def size(self):
        return 0, 0
    
    
    @cached_property
    def time(self):
        return self.display()[1]
    
    
    @cached_property
    def audio(self):
        return self.display()[2]
    
    
    @abstractmethod
    def draw(self, ctx: Context):
        text = self.display(max_time=ctx.time)[0]
        x = ctx.x + self.x
        y = ctx.y + self.y
        for line in text.split('\n'):
            ctx.draw.text((x, y), line, font=self.font, fill='white', spacing=16)
            y += self.line_height
