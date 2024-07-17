from time import time

from video.components.gif import Gif
from video.components.scene import Scene
from video.components.frame import Frame
from video.components.textboxes import TrilogyTextbox
from video.video import render_scene


scene = Scene(
    children=(
        Frame(
            width=1920,
            height=1080,
            background=Gif.open('image.gif'),
            foreground=Gif.open('image.gif'),
            textbox=TrilogyTextbox.from_input('[/bgswhack][/ts2]Nooooooooooooooooo! [/ts20][/bgs realization][/cg]Why do you hate me?[/cw] Is it because[/p500] ...wait, never mind.'),
            character=(),
            active_character=0,
        ),
    ),
)


start = time()
render_scene(scene, 'output', 'temp', 30)
out = time() - start

print(f'Finished in {out:.2f}s')