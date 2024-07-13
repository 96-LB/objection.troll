from functools import cache, cached_property

from .component import Component
from PIL import Image
from PIL.ImageDraw import ImageDraw as Draw
from PIL.GifImagePlugin import GifImageFile


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
        time = time % self.time
        
        for frame, frame_time in enumerate(self.times):
            if time < frame_time:
                return frame
            time -= frame_time
        
        return len(self.times) - 1
        
    
    def draw(self, draw: Draw, x: int, y: int, time: float, global_time: float):
        frame = self.get_frame(time)
        self._image.seek(frame)
        draw._image.paste(self._image, (x, y))
    
    
    @classmethod
    @cache
    def open(cls, filename: str):
        return cls(Image.open(filename))
