from PIL import Image, ImageDraw


class Renderer:
    
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.image = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        self.draw = ImageDraw.Draw(self.image)
    
    
    def alpha_composite(self, image: Image.Image, position: tuple[int, int]):
        self.image.alpha_composite(image, position)
