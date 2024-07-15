from video.components.gif import Gif
from video.components.scene import Scene
from video.components.frame import Frame
from video.components.textbox import TrilogyTextbox

scene = Scene(
    children=(
        Frame(
            width=1920,
            height=1080,
            background=Gif.open('image2.gif'),
            foreground=Gif.open('image2.webp'),
            textbox=TrilogyTextbox(input='Text speed modifications.[/ts100] Typing really slowly... [/ts10] Typing really quickly! Really really quickly! [/ts30]The default speed is 30.'),
            character=(),
            active_character=0,
        ),
        Frame(
            width=1920,
            height=1080,
            background=Gif.open('image.gif'),
            foreground=Gif.open('image.gif'),
            textbox=TrilogyTextbox(input='There are two frames now!'),
            character=(),
            active_character=0,
        ),
    ),
)


from video.video import render_scene

render_scene(scene, 'output', 'temp', 30)
