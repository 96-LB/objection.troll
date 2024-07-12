from abc import ABC
from dataclasses import dataclass, replace

from typing import Any, Self, dataclass_transform


@dataclass_transform(frozen_default=True)
@dataclass(frozen=True)
class Pod(ABC):
    def __init_subclass__(cls) -> None:
        super().__init_subclass__()
        
        cls = dataclass(frozen=True)(cls)
    
    
    def but(self, **attrs: Any) -> Self:
        return replace(self, **attrs)
    
    
    def plus(self, **attrs: Any) -> Self:
        for attr in attrs:
            attrs[attr] = getattr(self, attr) + attrs[attr]
        return self.but(**attrs)
