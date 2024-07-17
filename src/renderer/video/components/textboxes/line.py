from functools import cached_property

from PIL import ImageFont

from ..container import Container
from .commands import Command, TextSpeedCommand
from .text import Char

from typing import Self


class Line(Container[Char | Command]):
    
    text_speed: float
    color: tuple[int, int, int]
    font: ImageFont.FreeTypeFont
    height: int
    
    
    @cached_property
    def size(self):
        return 0, self.height
    
    
    @classmethod
    def from_input(cls, input: str, prev: Self):
        children: list[Char | Command] = []
        text, commands = Command.parse(input)
        curr, next = '', text.replace(Command.SIG, '')
        blip = 0 # time since last blip
        c = 0
        
        text_speed = prev.text_speed
        color = prev.color
        
        for i in range(len(text)):
            if text[i] == Command.SIG:
                command = commands[c]
                children.append(command)
                if isinstance(command, TextSpeedCommand):
                    text_speed = command.data
                c += 1
            else:
                char = next[0]
                
                # calculate text delay
                delay = text_speed
                if char.isspace():
                    if any(curr.endswith(c) for c in ('.', '!', '?', '—', ';')):
                        if not any(curr.lower().endswith(c) for c in ('mr.', 'mrs.', 'ms.', 'dr.', 'prof.')):
                            delay += 0.25
                    elif any(curr.endswith(c) for c in (',', '-', ':')):
                        if not text == '--':
                            delay += 0.1
                
                # update text buffers
                curr += char
                next = next[1:]
                
                # build text object
                child = Char(
                    char=curr[-1],
                    next=next[0] if next else '',
                    delay=delay,
                    color=color,
                    font=prev.font,
                    last_blip=blip
                )
                
                # update blip time
                if child.audio:
                    blip = child.time - child.audio[0][0] # time since child's blip
                else:
                    blip += child.time # no blip occurred
                
                children.append(child)
        
        return prev.but(
            children=tuple(children),
            text_speed=text_speed,
            color=color
        )
