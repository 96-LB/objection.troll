import os, shutil
from time import time

from moviepy.video.io.ImageSequenceClip import ImageSequenceClip
from moviepy.audio.io.AudioFileClip import AudioFileClip
from moviepy.audio.AudioClip import CompositeAudioClip

from video.components.scene import Scene


def get_image_clip(scene: Scene, path: str, fps: float, *, verbose: bool = True):
    if os.path.exists(path):
        shutil.rmtree(path)
    os.mkdir(path)
    
    start = time()
    i = -1
    for i, frame in enumerate(scene.render_frames(fps)):
        frame.save(f'{path}/{i:05d}.png')
        if verbose:
            print(i)
    out = time() - start
    if verbose:
        print(f'Finished in {out:.2f}s ({(i + 1)/out:.2f}fps)')
    
    return ImageSequenceClip(path, fps)


def get_audio_clip(scene: Scene):
    audio = []
    for time, sound in scene.audio:
        file = sound # TODO: probably subpath this
        if os.path.isfile(file):
            clip = AudioFileClip(file).set_start(time)
            audio.append(clip)
    
    return CompositeAudioClip(audio) if audio else None


def make_video(image_clip: ImageSequenceClip, audio_clip: CompositeAudioClip | None, output: str):
    if audio_clip:
        image_clip.audio = audio_clip.subclip(0, image_clip.duration)
    image_clip.write_videofile(output)


def render_scene(scene: Scene, output: str, temp_path: str, fps: float, *, verbose: bool = True):
    image_clip = get_image_clip(scene, temp_path, fps, verbose=verbose)
    audio_clip = get_audio_clip(scene)
    make_video(image_clip, audio_clip, output + '.mp4')
