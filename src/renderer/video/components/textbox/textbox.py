import re
from abc import abstractmethod
from functools import cached_property

from PIL import ImageFont

from ...context import Context
from ..component import Component

from typing import ClassVar


COMMAND = re.compile(r'\[/[^\]]+\]')
class Textbox(Component):
    x: ClassVar[int]
    y: ClassVar[int]
    width: ClassVar[int]
    line_height: ClassVar[int]
    font: ClassVar[ImageFont.FreeTypeFont]
    input: str
    
    
    def __init_subclass__(cls, x: int, y: int, width: int, line_height: int, font: ImageFont.FreeTypeFont):
        cls.x = x
        cls.y = y
        cls.width = width
        cls.line_height = line_height
        cls.font = font
        return super().__init_subclass__()
        
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
        
        return split_lines(re.sub(COMMAND, '§', self.input))
    
    
    @cached_property
    def commands(self) -> tuple[str, ...]:
        return tuple(x[2:-1] for x in re.findall(COMMAND, self.input)) # TODO: make these commands
    
    
    def display(self, *, max_time: float = float('inf')):
        text = ''
        time = 0
        c = 0
        delay = 0.03
        audio: list[tuple[float, str]] = []
        blip = -999
        for char in self.text:
            if time >= max_time:
                break
            
            if char == '§':
                command = self.commands[c]
                if command.startswith('ts'):
                    delay = float(command[2:]) / 1000
                elif command.startswith('p'):
                    time += float(command[1:]) / 1000
                elif command.startswith('bgs'):
                    audio.append((time, command[3:].strip() + '.wav'))

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
                time += delay
                if time > blip + 0.064:
                    blip = max(time - delay, blip + 0.064)
                    audio.append((blip, 'blip.wav'))
            
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
