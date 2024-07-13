from video.components.gif import Gif
from video.components.scene import Scene
from video.components.frame import Frame


scene = Scene(
    children=(
        Frame(
            width=1920,
            height=1080,
            background=Gif.open('image.gif'),
            foreground=Gif.open('image.webp'),
            textbox=None,
            character=(),
            active_character=0,
        ),
    ),
)


from video.video import render_scene

render_scene(scene, 'output', 'temp', 20)
