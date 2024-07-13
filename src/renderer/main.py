from video.components.gif import Gif
from video.components.scene import Scene
from video.components.frame import Frame


scene = Scene(
    children=(
        Frame(
            width=1920,
            height=1080,
            background=Gif.open('image.gif'),
            foreground=Gif.open('image2.gif'),
            textbox=None,
            character=(),
            active_character=0,
        ),
    ),
)

for time in range(400):
    a = scene.render_frame(time / 20)
    a.save(f'temp/frame_{time:03d}.png')
    print(time)
