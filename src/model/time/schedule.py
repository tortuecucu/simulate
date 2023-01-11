"""schedules are usefuf for determining if a ressource is opened or closed, busy or free
   as a convention, the term busy is used when a ressource is opened
"""

from datetime import datetime, time, date, timedelta
from abc import ABC, abstractmethod
from typing import Union, Optional, Set, Tuple
from datetimerange import DateTimeRange
from src.model.time.timerange import TimeRange
from evalidate import safeeval, EvalException
if True==False:
    from src.model.tipsters import RatioTipster
import warnings

class Schedule(ABC):
    @abstractmethod
    def is_busy(self, value:Union[datetime, DateTimeRange])->bool:
        pass

class ConstantSchedule(Schedule):
    """returns always the value of the aways_busy parameter
    """
    def __init__(self, always_busy:bool) -> None:
        super().__init__()
        self.always=always_busy
    def is_busy(self, value:Union[datetime, DateTimeRange])->bool:
        return self.always

class NestedSchedule(Schedule):
    """Allows nesting schedules to build a complex schedule.
       If is_busy() is true for the outer schedule, call the next inner schedule and so on until False is returned of the last schedule called

    """
    def __init__(self, schedules:Set[Schedule]) -> None:
        super().__init__()
        self.schedules=schedules
    def is_busy(self, value:Union[datetime, DateTimeRange])->bool:
        result:bool=False
        for s in self.schedules:
            if s.is_busy(value):
                result=True
            else:
                result=False
                break
        return result

class TipsterSchedule(Schedule):
    """Schedule driven by a tipster

    """
    def __init__(self, tipster='RatioTipster', upper:Optional[bool]=True) -> None:
        super().__init__()
        self.tipster=tipster
        self.upper=upper
    
    def is_busy(self, value:Union[datetime, DateTimeRange])->bool:
        score=self.tipster.forecast()
        if (score >= 0.5 and self.upper) or (score <0.5 and not self.upper):
            return True
        else:
            return False

class BankSchedule(Schedule):
    """is_busy() return False if the value is one of the bank days provided

    """
    def __init__(self, bank_days:Set[date]) -> None:
        super().__init__()
        self.bank_days=bank_days
    def is_busy(self, value:Union[datetime, DateTimeRange])->bool:
        if isinstance(value, datetime):
            return not value.date in self.bank_days
        else:
            for day in value.range(timedelta(days=1)):
                if day.date in self.bank_days:
                    return False
                return True

class WeekdaySchedule(Schedule):
    """is_busy() return True if the value weekday is on the open_days set

    """
    def __init__(self, open_days:Set[int]) -> None:
        super().__init__()
        self.open_days=open_days

    def is_busy(self, value:Union[datetime, DateTimeRange])->bool:
        if isinstance(value, datetime):
            days:Set=set([value.weekday()])
        elif isinstance(value, DateTimeRange):
            days=set(map(lambda dt: dt.weekday(), value.range(timedelta(days=1))))
        return days.issubset(self.open_days)

class WeeklySchedule(Schedule):
    """is_busy() return True is a tuple on openings have the same weekday as value and a overlapping timerange

    Args:
        Schedule (_type_): _description_
    """
    def __init__(self,openings=Set[Tuple[int, Set[TimeRange]]]) -> None:
        """init method

        Args:
            openings (Set): list open ranges during the week. Openings are sets containing an integer for the weekday and a timerange.
        """
        super().__init__()
        self.openings=openings

    def is_busy(self, value:Union[datetime, DateTimeRange])->bool:
        """return True if a opening range have the same weekday interger than valand and a matching timerange

        Args:
            value (Union[datetime, DateTimeRange]): value to check busyness

        Returns:
            bool: True if tuple in openings match the weekday & timerange criteria
        """
        if isinstance(value, datetime):
            weekday=value.weekday()
            value=DateTimeRange(value, value)
        elif isinstance(value, DateTimeRange):
            days={value.range(timedelta(days=1))}
            assert len(days)==1
            weekday=days[1].weekday()

        return len((o for o in self.openings if o[0]==weekday and value in o))>0

class ConditionalSchedule(Schedule):
    """check the value agains timerange that for which the function return True

    Args:
        Schedule (_type_): _description_
    """

    def __init__(self,openings=Set[Tuple[str, Set[TimeRange]]]) -> None:
        """init methode

        Args:
            openings (Set): list open ranges composed of a stringified function and a timerange. openings are checked only if the evaluation of the function return true
        """
        super().__init__()
        self.openings=openings
    
    def is_busy(self, value:Union[datetime, DateTimeRange])->bool:
        def _eval(func:str, value:datetime)->bool:
            try:
                return safeeval(func,{'d':value}, addnodes=['Attribute', 'Call'], attrs=['day', 'week_of_year', 'now'])
            except EvalException as e:
                warnings.warn(e)
                return False
        
        return len((o for o in self.openings if _eval(o[0]) and value in o))>0