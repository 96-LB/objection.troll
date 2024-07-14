from PIL import ImageFont

from video.renderer import Renderer

from .container import Container
from .line import Line

font = ImageFont.truetype('aa.otf', 96)
limit = 1600
class Textbox(Container[Line]):
    ...
    
    
    @classmethod
    def from_text(cls, text: str) -> 'Textbox':
        if not text:
            return cls(())
        
        words: list[str] = []
        
        space = False
        word = ''
        for char in text:
            if space != char.isspace():
                words.append(word)
                space = not space
                word = ''
            word += char
        words.append(word)
        
        lines: list[str] = []
        line = words[0]
        for i in range(1, len(words), 2):
            space = words[i]
            word = words[i + 1]
            
            for j, char in enumerate(space):
                if char == '\n':
                    lines.append(line)
                    line = ''
                    space = space[j + 1:]
            
            if not line:
                line = space + word
            elif font.getlength(line + space + word) > limit:
                lines.append(line)
                line = word
            else:
                line += space + word
        lines.append(line)
        
        return cls(tuple(Line.from_text(line) for line in lines))
    
        
    def draw(self, renderer: Renderer, x: int, y: int, time: float, global_time: float):
        x += 100
        y += 100
        renderer.draw.rectangle((x, y, x + 1680, y + 1232), fill=(0, 32, 64, 255), outline=(0, 64, 128, 255))
        
        
        
        
        
        
        
        
        super().draw(renderer, x + 40, y + 40, time, global_time)
