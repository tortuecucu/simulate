from src.model.items import Item
from abc import ABC, abstractmethod
from typing import Set, Iterable, Optional
from enum import Enum
from datetime import datetime

class BookingState(Enum):
    INIT=1
    VALIDATED=2
    WAITING_TRANSACTION=3
    COMMITTED=4
    ROLLBACKED=5
    CANCELLED=6
    COMMITING=7

class BaseBooking(ABC):
    def __init__(self) -> None:
        self._state:BookingState=BookingState.INIT
        self.created=datetime.now()
    @abstractmethod
    def commit(self)->None:
        pass
    @abstractmethod
    def rollback(self)->None:
        pass
    @property
    def state(self)->BookingState:
        return self._state

class CommitException(RuntimeError):
    pass

class RollbackException(RuntimeError):
    pass

class Transaction(BaseBooking):
    def __init__(self,items:Optional[Iterable['ItemBooking']]=None, auto_Commit:Optional[bool]=True) -> None:
        super().__init__()
        self._bookings=set()
        self._auto_commit=auto_Commit
        [self.add(i) for i in items]
    
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if not exc_tb and self._auto_commit and self._state==BookingState.VALIDATED:
            self.commit()
        elif not exc_tb:
            self.rollback()    
        else:
            raise RuntimeError()
    
    def commit(self) -> None:
        try:
            assert len(self._bookings)>0, "no bookings to commit"
            assert self._state==BookingState.VALIDATED, ""
        except AssertionError as e:
            raise ValueError() from e
        try:
            [b.commit() for b in self._bookings]
            self._state=BookingState.COMMITTED
        except CommitException as e:
            raise e
    
    def add(self, booking:'ItemBooking')->None:
        try:
            assert booking._state < BookingState.COMMITTED
            assert booking._transaction == None
            booking._transaction=self
            booking._state=BookingState.WAITING_TRANSACTION
            self._bookings.add(booking)
        except AssertionError as e:
            raise ValueError() from e
        else:
            self._state==BookingState.VALIDATED


    def rollback(self) -> None:
        try:
            [b.rollback() for b in self._bookings]
        except AssertionError as e:
            raise RollbackException() from e
        else:
            self._state=BookingState.ROLLBACKED
        

class ItemBooking(BaseBooking):
    def __init__(self, item:Item) -> None:
        assert item._booking == None
        self._item=item
        self._transaction=None
        item._booking=self

    @property
    def item(self)->Item:
        return self._item



class ProcessBooking(ItemBooking):
    ...