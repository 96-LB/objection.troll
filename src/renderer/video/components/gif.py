from functools import cache, cached_property

from PIL import Image
from PIL.GifImagePlugin import GifImageFile

from .component import Component
from util.renderer import Renderer

class Gif(Component):
    _image: Image.Image
    
    
    @cached_property
    def size(self):
        return self._image.size
    
    
    @cached_property
    def delay(self):
        return self.time
    
    
    @cached_property
    def time(self):
        return sum(self.times)
    
    
    @cached_property
    def audio(self):
        return ()
    
    
    @cached_property
    def times(self):
        if not isinstance(self._image, GifImageFile):
            print(type(self._image))
            return ()
        
        times: list[float] = []
        for frame in range(self._image.n_frames):
            self._image.seek(frame)
            try:
                times.append(float(self._image.info['duration']) / 1000)
            except (KeyError, ValueError):
                pass
        
        return tuple(times)
    
    
    def get_frame(self, time: float):
        if not self.times:
            return 0
        
        if 'loop' in self._image.info:
            time = time % self.time
        
        for frame, frame_time in enumerate(self.times):
            if time < frame_time:
                return frame
            time -= frame_time
        
        return len(self.times) - 1
    
    
    def draw(self, draw: Renderer, x: int, y: int, time: float, global_time: float):
        frame = self.get_frame(time)
        self._image.seek(frame)
        draw.alpha_composite(self._image.convert('RGBA'), (x, y))
    
    
    @classmethod
    @cache
    def open(cls, filename: str):
        return cls(Image.open(filename))
