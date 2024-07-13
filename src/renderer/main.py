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

for i, frame in enumerate(scene.render_frames(20)):
    frame.save(f'temp/frame_{i:05d}.png')
    print(i)
