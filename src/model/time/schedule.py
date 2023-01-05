"""schedules are usefuf for determining if a ressource is opened or closed, busy or free
   as a convention, the term busy is used when a ressource is opened
"""

from datetime import datetime, time, date, timedelta
from abc import ABC, abstractmethod
from typing import Union, Optional, Set, Dict
from datetimerange import DateTimeRange
from src.model.time.timerange import TimeRange
if True==False:
    from src.model.tipster import RatioTipster

class Schedule(ABC):
    @abstractmethod
    def is_busy(self, value:Union[datetime, DateTimeRange])->bool:
        pass

class ConstantSchedule(Schedule):
    def __init__(self, always_busy:bool) -> None:
        super().__init__()
        self.always=always_busy
    def is_busy(self, value:Union[datetime, DateTimeRange])->bool:
        return self.always

class NestedSchedule(Schedule):
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
    def __init__(self,openings=Dict[int, Set[TimeRange]]) -> None:
        super().__init__()
        self.openings=openings
    def is_busy(self, value:Union[datetime, DateTimeRange])->bool:
        if isinstance(value, datetime):
            weekday=value.weekday()
            value=DateTimeRange(value, value)
        elif isinstance(value, DateTimeRange):
            days={value.range(timedelta(days=1))}
            assert len(days)==1
            weekday=days[1].weekday()
        range:DateTimeRange=self.openings.get(weekday)
        if range:
            return range.is_intersection(value)
        else:
            return None
