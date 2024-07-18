from time import time

from video.components.character import Character
from video.components.gif import Gif
from video.components.frame import Frame
from video.components.scene import Scene
from video.components.textboxes import TrilogyTextbox
from video.video import render_scene


scene = Scene(
    children=(
        Frame(
            width=960,
            height=640,
            background=Gif.open('img/bg.jpg'),
            foreground=Gif.open('img/desk.png'),
            textbox=TrilogyTextbox.from_input('This is bad. Really, really bad.[/p2000] Like really really really really really really really really bad.'),
            characters=(
                Character(
                    pre=Gif.open('img/Damage.gif'),
                    idle=Gif.open('img/Cornered.gif'),
                    talk=Gif.open('img/Cornered_talk.gif'),
                    bgs='explosion.wav',
                )
            ,),
            active_index=0,
        ),
    ),
)

start = time()
render_scene(scene, 'output', 'temp', 60)
out = time() - start

print(f'Finished in {out:.2f}s')