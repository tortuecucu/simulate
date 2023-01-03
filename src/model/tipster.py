from abc import ABC, abstractmethod
from typing import Optional, Set, List
from numbers import Number
from random import randrange

def _threshold(f):
    def wrapper(*args):
        tipster:Tipster=args[0]
        value = f(*args)
        if tipster.min and value < tipster.min:
            value=tipster.min
        if tipster.max and value > tipster.max:
            value=tipster.max
        return value
    return wrapper

class Tipster():
    _instances=list()
    def __init__(self, min:Optional[float]=None, max:Optional[float]=None) -> None:
        self.min=min
        self.max=max
        self._history=list()
        self._instances.append(self)
    
    @property
    def history(self)->List[Number]:
        return self._history
    
    @_threshold
    def forecast(self)->Number:
        value=self._calculate()
        self._history.append(value)
        return value
    
    @abstractmethod
    def _calculate(self)->Number:
        pass

    @classmethod
    def tipster(cls,**kwargs)->'Tipster':
        ... #TODO: code it

class RatioTipster(Tipster):
    def __init__(self) -> None:
        super().__init__(min=0, max=1)