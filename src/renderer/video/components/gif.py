from functools import cache, cached_property

from PIL import Image
from PIL.GifImagePlugin import GifImageFile
from PIL.WebPImagePlugin import WebPImageFile

from .component import Component
from video.context import Context


class Gif(Component):
    _image: Image.Image
    
    @cached_property
    def size(self):
        return self._image.size
    
    
    @cached_property
    def time(self):
        return sum(self.times)
    
    
    @cached_property
    def effects(self):
        return ()
    
    
    @cached_property
    def times(self):
        if not isinstance(self._image, (GifImageFile, WebPImageFile)):
            return ()
        
        times: list[float] = []
        for frame in range(self._image.n_frames):
            self._image.seek(frame)
            self._image.load()
            try:
                times.append(float(self._image.info['duration']) / 1000)
            except (KeyError, ValueError) as e: # TODO: import catch from lalaverse
                print(f'Error: {e}')
                times.append(0)
        
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
    
    
    def draw(self, ctx: Context):
        frame = self.get_frame(ctx.time)
        self._image.seek(frame)
        ctx.image.alpha_composite(self._image.convert('RGBA'), ctx.pos)
    
    
    @classmethod
    @cache
    def open(cls, filename: str):
        return cls(Image.open(filename))
    
    
    @classmethod
    @cache
    def empty(cls):
        return cls(Image.new('RGBA', (0, 0)))
