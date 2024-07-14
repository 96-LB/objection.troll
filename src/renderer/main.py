from video.components.gif import Gif
from video.components.scene import Scene
from video.components.frame import Frame
from video.components.textbox import Textbox

scene = Scene(
    children=(
        Frame(
            width=1920,
            height=1080,
            background=Gif.open('image2.gif'),
            foreground=Gif.open('image2.webp'),
            textbox=Textbox.from_text('Kerning test! TofjTjkjtjfiTiT_foToToilrTofjTjkjtjfiTiT_foToToilrTofjTjkjtjfiTiT_foToToilr'),
            character=(),
            active_character=0,
        ),
    ),
)


from video.video import render_scene

render_scene(scene, 'output', 'temp', 30)
