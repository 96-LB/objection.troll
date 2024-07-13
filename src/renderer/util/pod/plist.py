# from .pod import Pod

# from typing import Iterable
from lalatypes import T


PList = tuple[T, ...]


# class PList[V](Pod):
#     items: tuple[V, ...] = ()
    
    
#     @staticmethod
#     def new(items: Iterable[T]) -> 'PList[T]':
#         return PList(items=tuple(items))
    
    
#     def __len__(self):
#         return len(self.items)
    
    
#     def __getitem__(self, index: int):
#         return self.items[index]
    
    
#     def __iter__(self):
#         return iter(self.items)
