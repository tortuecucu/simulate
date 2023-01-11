from datetime import datetime, timedelta
from typing import Optional, List, Type, Dict, Callable, Awaitable, Union, Set, Union, Any
from src.model.signals import Tick, NewDay, NewMonth, NewYear, NewWeek, ClockStop
from functools import cached_property
import asyncio

class Identifiable():
    """gives a contenient way to identify objects at runtime

    Returns:
        _type_: type of the subclass used at runtime
    """
    _ids:Dict[Type, int]={}
    _instances:List=[]

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
        self._instances.append(self)
    
    def __str__(self) -> str:
       return f"{self.__class__.__name__} (name='{self.name}', id='{self.id}')"
    
    def _changed(self, field:str, old_value:Any, new_value:Any)->None:
        ... #TODO: code it. complete raw with timestamp, id, name and classname
    
    @property
    def id(self)->int:
        return self._id
    
    @property
    def name(self)->str:
        return self._name if self._name else f"{__class__.__name__}_{self.id}"
    
    @classmethod
    def find(cls, query:Union[str, int, Callable])->Set['Identifiable']:
        """retruns all class instances that match the query
           if query is a function, then return all items for which query(item)==True
           if query is an int, then return the item with item.id==query, if any
           if query is a string, then return the item with item.name==query, case-sensitive, if any
        """
        def _true(instance:Identifiable)->bool:
            if callable(query):
                return query(instance)
            elif isinstance(query, int):
                return instance.id==query
            else:
                return instance.name==query
        return (i for i in cls.instances() if _true(i))
        
    @classmethod
    def instances(cls, query:Union[str, int, Callable])->Set['Identifiable']:
        return (i for i in cls._instances if isinstance(i, cls))
    
class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]

class Scenario(metaclass=Singleton):
    ...
    #TODO: code scenario





class Simulation(metaclass=Singleton):
    #clock, orders, workcenters, routes, logger, id, path
    def __init__(self, scenario:Scenario) -> None:
        self.scenario=scenario

    async def run():
        ...
        #TODO: check scenario, init simulation, run it, post run and closing operations

class Clock(metaclass=Singleton):
    """ handle time while a simulation is running.
        raise an event each time the clock is ticking via blinker and to the attached observers

    Args:
        metaclass (_type_, optional): _description_. Defaults to Singleton.
    """
    def __init__(self, simulation:Simulation, start:datetime, period:Optional[timedelta]=timedelta(hours=1), end:Optional[datetime]=None) -> None:
        self.simulation=simulation
        self.start=start
        self.end=end
        self.period=period
        self.is_running:bool=False
        self.current=start
        self.ticks:int=0
        self.real_duration:float=0
        self._observers=[]

    def start(self)->None:
        self.is_running=True
        self.tick()

    def stop(self)->None:
        self.is_running=False
        ClockStop.send(self)
        ClockStop.send_async(self)
    
    async def tick(self)->None:
        while self.is_running:
            self.ticks+=1
            tick_start=datetime.now()
            await self.notify()
            Tick.send_async(self)
            self._signals(
                self.current,
                self.current+self.period
            )
            self.current=self.current+self.period
            tick_end=datetime.now()
            self.real_duration=self.real_duration+(tick_end-tick_start)
            if not self.end==None and self.current>self.end:
                self.stop()
    
    
    def _signals(self, previous:datetime.date, current:datetime.date)->None:
        if previous != current:
            NewDay.send_async(self)
            if previous.isocalendar().week != current.isocalendar().week:
                NewWeek.send(self)
                NewWeek.send_async(self)
            if previous.month != current.month:
                NewMonth.send(self)
                NewMonth.send_async(self)
            if previous.year != current.year:
                NewYear.send(self)
                NewYear.send_async(self)

    @cached_property
    def total_ticks(self)->int:
        """calculate the total number of ticks necessary to run the simulation

        Returns:
            int: number of ticks that will be runned during the simulation
        """
        import math
        return math.ceil((self.end - self.start) / self.period)
    
    def attach(self, observer:Union[Callable, Awaitable])->None:
        if (callable(observer) or asyncio.iscoroutine(observer)) and observer not in self._observers:
            self._observers.append(observer)
    
    def detach(self, observer)->None:
        try:
            self._observers.remove(observer)
        except ValueError:
            pass
    
    async def notify(self)->None:
        [o(self) for o in self._observers if not asyncio.iscoroutine(o)] #notify regular functions
        coros=[c for c in self._observers if asyncio.iscoroutine(c)]
        if len(coros)>0:
            await asyncio.gather(*[o(self) for o in coros])