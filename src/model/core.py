from datetime import datetime, timedelta
from typing import Optional, List, Type, Dict
from src.model.signals import Tick


class Identifiable():
    _ids:Dict[Type, int]={}

    @classmethod
    def next_id(cls)->int:
        return Identifiable._ids.get(cls, 0)

    def __new__(cls, *kargs):
        if cls in Identifiable._ids:
            Identifiable._ids[cls]=Identifiable._ids[cls]+1
        else:
            Identifiable._ids[cls]=0
        return object.__new__(cls)

    def __init__(self, name:Optional[str]=None) -> None:
        self._id=self.next_id()
        self._name=name
    
    def __str__(self) -> str:
       return f"{self.__class__.__name__} (name='{self.name}', id='{self.id}')"
    
    @property
    def id(self)->int:
        return self._id
    
    @property
    def name(self)->str:
        return self._name if self._name else f"{__class__.__name__}_{self.id}"
    
class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class Scenario(metaclass=Singleton):
    pass





class Simulation(metaclass=Singleton):
    #clock, orders, workcenters, routes, logger, id, path
    def __init__(self, scenario:Scenario) -> None:
        self.scenario=scenario

    async def run():
        ...

class Clock(metaclass=Singleton):
    def __init__(self, simulation:Simulation, start:datetime, period:Optional[timedelta]=timedelta(hours=1), end:Optional[datetime]=None) -> None:
        self.simulation=simulation
        self.start=start
        self.end=end
        self.period=period
        self.is_running:bool=False
        self.current=start
        self.ticks:int=0
        self.duration:float=0

    def start(self)->None:
        self.is_running=True
        self.tick()

    def stop(self)->None:
        self.is_running=False
    
    def tick(self)->None:
        while self.is_running:
            self.ticks+=1
            tick_start=datetime.now()
            Tick.send(self)
            self.current=self.current+self.period
            tick_end=datetime.now()
            self.duration=self.duration+(tick_end-tick_start)
            if not self.end==None and self.current>self.end:
                self.stop()




