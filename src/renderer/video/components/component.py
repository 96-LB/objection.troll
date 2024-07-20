from abc import ABC, abstractmethod
from functools import cached_property

from util.pod import PList, Pod
from video.context import Context
from video.effects import Effect


class Component(Pod, ABC):
    @cached_property
    @abstractmethod
    def size(self) -> tuple[float, float]:
        ...
    
    @cached_property
    @abstractmethod
    def time(self) -> float:
        ...
    
    @cached_property
    @abstractmethod
    def effects(self) -> PList[Effect]:
        ...
    
    # @cache # cache seems to typecast this to Any
    def get_effects[T: Effect](self, type: type[T]):
        return tuple(effect for effect in self.effects if isinstance(effect, type))
    
    @abstractmethod
    def draw(self, ctx: Context):
        ...
