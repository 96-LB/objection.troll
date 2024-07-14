from functools import cached_property

from .container import Container
from .text import Text


from PIL import ImageFont
font = ImageFont.truetype('aa.otf', 96)
class Line(Container[Text]):
    height: int = 120
    
    @cached_property
    def size(self):
        return 0, self.height
    
    
    @classmethod
    def from_text(cls, text: str):
        return cls(tuple(Text(char, font, 0.03) for char in text))
