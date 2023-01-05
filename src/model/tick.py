from abc import ABC, abstractclassmethod
from typing import Optional
from src.model.core import Simulation
from src.model.core import Identifiable
from src.model.signals import Tick

class Tickable(ABC, Identifiable):
    """Tickable is a base class intended to be subclassed. Tickable objects reacts to the ticks of the simulation clock

    Args:
        ABC (_type_): _description_
        Identifiable (_type_): _description_
    """
    _instances=list()
    def __init__(self, id:int, simulation:Simulation, name:Optional[str]=None) -> None:
        Identifiable.__init__(self, name=name)
        self.simulation=simulation
        self._instances.append(self)
        self.attach()
    
    def attach(self)->None:
        Tick.connect(self.tick)
        
    @abstractclassmethod
    async def tick(self)->None:
        pass
