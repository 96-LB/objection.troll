from abc import abstractmethod

from PIL import ImageFont

from ...context import Context
from ..container import Container
from .commands import Command
from .line import Line

from typing import ClassVar


class Textbox(Container[Line]):
    x: ClassVar[int]
    y: ClassVar[int]
    width: ClassVar[int]
    line_height: ClassVar[int]
    font: ClassVar[ImageFont.FreeTypeFont]
    blip_speed: ClassVar[float]
        
    
    def __init_subclass__(cls, x: int, y: int, width: int, line_height: int, font: ImageFont.FreeTypeFont, blip_speed: float):
        cls.x = x
        cls.y = y
        cls.width = width
        cls.line_height = line_height
        cls.font = font
        cls.blip_speed = blip_speed
        return super().__init_subclass__()
    
    
    @classmethod
    def from_input(cls, input: str):
        def split_lines(text: str) -> tuple[str, ...]:
            saved = 0
            for i in Command.text_indices(text):
                if text[i] == '\n':
                    return (text[:i + 1],) + split_lines(text[i + 1:])
                elif text[i].isspace():
                    saved = i
                if cls.font.getlength(Command.clean(text[:i + 1])) > cls.width:
                    return (text[:saved or i],) + split_lines(text[(saved or i) + 1:])
            return (text,)
        
        children = []
        child = Line(
            children=(),
            text_speed=0.03, # TODO: make a constant for text speed
            color=(255, 255, 255),
            font=cls.font,
            height=cls.line_height
        )
        lines = split_lines(input)
        for line in lines:
            child = Line.from_input(line, child)
            children.append(child)
        return cls(children=tuple(children))
        
    
    
    @abstractmethod
    def draw(self, ctx: Context):
        ctx = ctx.plus(x=self.x, y=self.y)
        super().draw(ctx)
