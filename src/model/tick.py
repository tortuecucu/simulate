from abc import ABC, abstractclassmethod
from typing import Optional
from src.model.core import Simulation
from src.model.core import Identifiable

class Tickable(ABC, Identifiable):
    _instances=list()
    def __init__(self, id:int, simulation:Simulation, name:Optional[str]=None) -> None:
        Identifiable.__init__(self, name=name)
        self.simulation=simulation
        self._instances.append(self)
        
    @abstractclassmethod
    def tick(self)->None:
        pass
