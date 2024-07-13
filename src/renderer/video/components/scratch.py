from .component import Component
from .container import Container


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
