from video.components.gif import Gif
from video.components.scene import Scene
from video.components.frame import Frame


scene = Scene(
    children=(
        Frame(
            width=1920,
            height=1080,
            background=Gif.open('image.gif'),
            foreground=None,
            textbox=None,
            character=(),
            active_character=0,
        ),
    ),
)

for time in range(120):
    a = scene.render_frame(time / 60)
    a.save(f'temp/frame_{time:03d}.png')
