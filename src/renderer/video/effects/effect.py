from abc import ABC

from util.pod import Pod


class Effect(Pod, ABC):
    time: float
    
    def plus_time(self, time: float):
        return self.plus(time=time)
