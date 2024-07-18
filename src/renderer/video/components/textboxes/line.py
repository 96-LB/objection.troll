from functools import cached_property

from PIL import ImageFont

from ..container import Container
from .commands import Command
from .char import Char

from typing import Self


class Line(Container[Char]):
    
    text_speed: float
    color: tuple[int, int, int]
    font: ImageFont.FreeTypeFont
    height: int
    last_blip: float
    
    @cached_property
    def size(self):
        return 0, self.height
    
    
    @classmethod
    def from_input(cls, input: str, prev: Self):
        children: list[Char] = []
        text, commands = Command.parse(input + ' ')
        curr, next = '', text.replace(Command.SIG, '')
        child = Char(
            char='',
            next='',
            pause=float('inf'), # so the first char blips
            sound='',
            text_speed=prev.text_speed,
            color=prev.color,
            font=prev.font,
            last_blip=prev.last_blip,
        )
        
        c = 0 # command index
        for i in range(len(text)):
            if text[i] == Command.SIG: # next character is a command
                command = commands[c]
                child = command.get_char(child)
                c += 1
            else:
                char = next[0]
                
                # calculate text delay
                pause = 0
                if char.isspace():
                    if any(curr.endswith(c) for c in ('.', '!', '?', '—', ';')):
                        if not any(curr.lower().endswith(c) for c in ('mr.', 'mrs.', 'ms.', 'dr.', 'prof.')):
                            pause = 0.25
                    elif any(curr.endswith(c) for c in (',', '-', ':')):
                        if not text == '--':
                            pause = 0.1
                
                # build text object
                child = Char.from_input(char, child).but(pause=pause)
                
                # update text buffer
                curr += char
                next = next[1:]
            
            children.append(child)
        
        return prev.but(
            children=tuple(children),
            text_speed=child.text_speed,
            color=child.color,
            last_blip=child.last_blip
        )
