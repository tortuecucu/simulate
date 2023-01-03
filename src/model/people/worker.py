from abc import ABC, abstractproperty
from src.model.core import Identifiable

class Worker(ABC, Identifiable):
    @abstractproperty
    def is_working(self)->bool:
        pass
    @abstractproperty
    def is_busy(self)->bool:
        pass
    @abstractproperty
    def productivity(self)->float:
        pass
    @abstractproperty
    def attendance_rate(self)->float:
        pass