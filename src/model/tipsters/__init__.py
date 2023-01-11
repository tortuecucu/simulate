from abc import ABC, abstractmethod
from typing import Optional, Set, List
from numbers import Number
from model.core import Identifiable
from random import random, gauss, uniform

""" Tipsters are responsible of returning values for parameters that varies between threshold and following rules
    These variations produces aleas on the same way as real world
""" 

def _threshold(f):
    """decorator that ensure the returned walue is under limits
       min or max value is returned if threshold is reached
    """
    def wrapper(*args):
        tipster:Tipster=args[0]
        attempts=0
        def within_limits(value:float)->bool:
            return ((tipster.min and value < tipster.min)or(tipster.min==None)) and ((tipster.max and value > tipster.max)or(tipster.max==None))
        value = f(*args)
        while not within_limits(value):
            if attempts < 500:
                attempts+=1
                value = f(*args)
            else:
                value = uniform(
                    tipster.min if tipster.min else 0,
                    tipster.max if tipster.max else 1
                )
        return value    
    return wrapper

class Tipster(Identifiable):
    """Tipsters are responsible of returning values for parameters that varies between threshold and following rules
    """
    _instances=list()
    def __init__(self, min:Optional[float]=None, max:Optional[float]=None) -> None:
        self.min=min
        self.max=max
        self._history=list()
        self._instances.append(self)
    
    @property
    def history(self)->List[Number]:
        """list all values already returned by calling the forecast() method

        Returns:
            List[Number]: previous results
        """
        return self._history
    
    @_threshold
    def forecast(self)->Number:
        """return a new value for the variable

        Returns:
            Number: current value
        """     
        value=self._calculate()
        self._history.append(value)
        return value
    
    @abstractmethod
    def _calculate(self)->Number:
        """inner function that must be overriden by subclasses

        Returns:
            Number: _description_
        """
        pass

    @classmethod
    def tipster(cls, type:type, id:Optional[int]=None, name:Optional[str]=None)->'Tipster':
        """return a Tipster instance that match criteria

        Args:
            id (int): id of the instance. if id is provided then name is ignored
            type (type): class of the instance
            name (str): case-sentivite name of the instance

        Returns:
            Tipster: _description_
        """
        criteria=('id', id) if id else ('name', name)
        matches=[o for o in cls._instances if isinstance(o, type) and getattr(o, criteria[0])==criteria[1]]
        if len(matches)>0:
            return matches[0]

class RatioTipster(Tipster):
    """base class for tipster that returns a float between 0 and 1

    Args:
        Tipster (_type_): _description_
    """
    def __init__(self) -> None:
        super().__init__(min=0, max=1)

