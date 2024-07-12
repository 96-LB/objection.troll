from .component import Component
from .container import Container
from util.pod.plist import PList


class Text(Component):
    ...

class Word(Container[Text]):
    ...

class Line(Container[Word]):
    ...

class Textbox(Container[Line]):
    ...

class Character(Component):
    ...

class Frame(Component):
    textbox: Textbox
    character: PList[Character]
    active_character: int
