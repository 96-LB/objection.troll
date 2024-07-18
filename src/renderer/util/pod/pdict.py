from .plist import PList
from .pod import Pod

from typing import Mapping
from lalatypes import T, T2


class PDict[K, V](Pod):
    items: PList[tuple[K, V]] = ()
    
    
    @staticmethod
    def new(items: Mapping[T, T2]) -> 'PDict[T, T2]':
        return PDict(tuple(items.items()))
    
    
    def __contains__(self, key: K) -> bool:
        return any(k == key for k, _ in self.items)
    
    
    def __getitem__(self, key: K):
        try:
            return next(v for k, v in self.items if k == key)
        except StopIteration:
            raise KeyError(key)
    
    
    def get(self, key: K, default: V) -> V:
        try:
            return self[key]
        except KeyError:
            return default
    
    
    def set(self, key: K, value: V):
        items = list(self.items)
        for i in range(len(items)):
            if items[i][0] == key:
                items[i] = (key, value)
                break
        else:
            items.append((key, value))
        return self.but(items=tuple(items))
