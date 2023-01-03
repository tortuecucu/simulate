from datetime import time, timedelta, date, datetime
import re
from typing import Union,Tuple
from datetimerange import DateTimeRange

def parse_time(value:str)->time:
    try:
        reg=re.compile(r"^(?P<h>\d{2})[:h](?P<m>\d{2})(?:\:(?P<s>\d{2}))?")
        return time(*map(lambda x: int(x) if x else 0, reg.match(value).groupdict().values()))
    except AttributeError as e:
        raise ValueError from e


class TimeRange():
    def __init__(self, start:Union[time,str], end:Union[time,str]) -> None:
        try:
            if isinstance(start, str): start=parse_time(start)
            if isinstance(end, str): end=parse_time(end)
            assert start < end, "start must happen before end"
            self.start=start
            self.end=end
        except (AssertionError, ValueError) as e:
            raise ValueError from e
    
    @property
    def delta(self)->timedelta:
        return datetime.combine(date.min, self.end) - datetime.combine(date.min, self.start)
    
    def is_subset(self, subset:'TimeRange')->bool:
        return subset.start>=self.start and subset.end<=self.end
    
    def __contains__(self, v):
        if isinstance(v, datetime):
            v=v.time()
        if isinstance(v, DateTimeRange) and len(v.range(timedelta(days=1))):
            v=TimeRange(v.start_datetime.time(), v.end_datetime.time())
        if isinstance(v, time) and (v >= self.start and v <= self.end):
            return True
        elif isinstance(v, TimeRange):
            self.is_subset(v) 
        return False
