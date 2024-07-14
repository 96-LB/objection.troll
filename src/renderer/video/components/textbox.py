import re

from functools import cached_property

from PIL import ImageFont

from ..context import Context
from .component import Component


font = ImageFont.truetype('aa.otf', 96)
limit = 1600
line_height: int = 128
pos: tuple[int, int] = (100, 100)
size: tuple[int, int] = (1680, 1232)
margin: int = 40
textspeed: float = .03
COMMAND = re.compile(r'\[/[^\]]+\]')
class Textbox(Component):
    input: str
        
    @cached_property
    def text(self):
        def split_lines(text: str) -> str:
            saved = 0
            for i in range(len(text)):
                if text[i] == '\n':
                    return text[:i + 1] + split_lines(text[i + 1:])
                elif text[i].isspace():
                    saved = i
                elif font.getlength(text[:i + 1]) > limit:
                    return text[:saved or i] + '\n' + split_lines(text[(saved or i) + 1:])
            return text
        
        return split_lines(re.sub(COMMAND, '§', self.input))
    
    
    @cached_property
    def commands(self) -> tuple[str, ...]:
        return tuple(x[2:-1] for x in re.findall(COMMAND, self.input)) # TODO: make these commands
    
    
    def display(self, textspeed: float, max: float = float('inf')):
        text = ''
        time = 0
        c = 0
        delay = textspeed
        for char in self.text:
            if time > max:
                break
            
            if char == '§':
                command = self.commands[c]
                if command.startswith('ts'):
                    delay = float(command[2:]) / 1000
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
            
            text += char
        
        return text, time
    
    
    @cached_property
    def size(self):
        return size
    
    
    @cached_property
    def time(self):
        return self.display(textspeed)[1]
    
    
    def draw(self, ctx: Context):
        x = ctx.x + pos[0]
        y = ctx.y + pos[1]
        ctx.draw.rectangle((x, y, x + size[0], y + size[1]), fill=(0, 32, 64, 255), outline=(0, 64, 128, 255))
        
        text, _ = self.display(textspeed, ctx.time)
        
        for line in text.split('\n'):
            ctx.draw.text((x + margin, y + margin), line, font=font, fill='white', spacing=16)
            y += line_height
