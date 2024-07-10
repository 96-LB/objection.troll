import re
from dataclasses import replace

from objectionpy.assets import Background
from objectionpy.enums import Easing, FadeDirection, FadeTarget, PresetBlip, PresetPopup
from objectionpy.frames import Color, Fade, OptionModifiers, Transition
from objectionpy.objection import Scene, loadJSONDict


bg_map = {
    # pw courtroom
    189: (72269, 0),
    197: (72269, .5),
    194: (72269, 1),
    # aj courtroom
    177: (118549, 0),
    186: (118549, .5),
    182: (118549, 1),
    # aj judge
    178: (118583, 0)
}


def process(data):
    scene = loadJSONDict(data)
    assert isinstance(scene, Scene)
    
    
    i = len(scene.frames)
    while i > 0:
        i -= 1
        frame = scene.frames[i]
        
        if '[@al]' in frame.text:
            frame.text = frame.text.replace('[@al]', '')
            scene.frames[i - 1].text += frame.text # amend last frame
            scene.frames.pop(i)
        elif '[@dl]' in frame.text:
            frame.text = frame.text.replace('[@dl]', '')
            scene.frames.pop(i - 1) # deletes last frame
            i -= 1
        elif '[@pl]' in frame.text:
            frame.text = frame.text.replace('[@pl]', '')
            scene.frames[i - 1].poseAnim ^= True # toggles preanimation of last frame
    # TODO: do all [@al] first, then all [@dl], etc
    
    i = 0
    while i < len(scene.frames):
        frame = scene.frames[i]
        
        if not frame.char or frame.char.character.id not in (102, ): # TODO: add pw gallery here
            bg = frame.background or (frame.char.character.background if frame.char else Background(0))
            if bg.id in bg_map:
                new_bg, x = bg_map[bg.id]
                frame.background = Background(new_bg)
                frame.wideX = x if not frame.backgroundFlip else 1 - x
                frame.transition = Transition(0, Easing.EASE_IN_OUT_EXPONENTIAL)
                
        if frame.presetPopup is PresetPopup.CROSS_EXAMINATION:
            frame.centerText = True
            frame.presetBlip = PresetBlip.TYPEWRITER
            frame.customName = '.'
            frame.talk = False
            frame.poseAnim = False
            frame.text = '\n' + frame.text.strip()
            if not scene.frames[i - 1].fade:
                frame.text += '[@fl]'
        
        if '[@fl]' in frame.text or '[@fs]' in frame.text:
            long = '[@fl]' in frame.text
            frame.text = frame.text.replace('[@fl]', '').replace('[@fs]', '')
            
            last = scene.frames[i - 1]

            duration = 1000 if long else 500
            fade = Fade(
                    direction=FadeDirection.OUT,
                    target=FadeTarget.EVERYTHING,
                    duration=duration,
                    easing=Easing.LINEAR,
                    color=Color('#000000')
                )
            
            out_frame = replace(
                last,
                text='',
                popup=None,
                presetPopup=None,
                fade=fade
            )

            duration /= 2
            fade = replace(fade, direction=FadeDirection.IN, duration=duration)
            
            in_frame = replace(
                frame,
                text=f'[#p{int(duration)}]',
                popup=None,
                presetPopup=None,
                options=OptionModifiers(dialogueBoxVisible=False),
                fade=fade
            )

            scene.frames.insert(i, in_frame)
            scene.frames.insert(i, out_frame)
            i += 2
            
        if frame.bubble or '[@t]' in frame.text:
            frame.text = frame.text.replace('[@t]', '')
            frame.transition = Transition(375, Easing.EASE_IN_OUT_EXPONENTIAL)

        if '[@m]' in frame.text:
            frame.text = frame.text.replace('[@m]', '')
            frame.merge = True

        if '[@i]' in frame.text:
            frame.text = frame.text.replace('[@i]', '')
            frame.goNext = True

        if '[@nt]' in frame.text:
            frame.text = frame.text.replace('[@nt]', '')
            frame.talk = False
        
        frame.text = frame.text.strip()
        frame.text = re.sub(r'([.?!;:])(\s)', r'\1[#p250]\2', frame.text)
        frame.text = re.sub(r'([,-])(\s)', r'\1[#p100]\2', frame.text)
        frame.text = re.sub(r'(Mr.|Ms.|Mrs.|Dr.)(\[#p250\])', r'\1', frame.text)
        frame.text = re.sub(r'(--)(\[#p100\])( )', r'\1\3', frame.text)
        if frame.text and frame.text[-1] not in '.?!-)]':
            frame.text += '.'
        
        i += 1
    
    return scene.compile()
