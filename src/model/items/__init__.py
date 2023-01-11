from model.core import Identifiable
from typing import Optional, Union
from src.model.items.holders import ItemsHolder
from enum import Enum
from src.model.exceptions import TransfertException, TransfertExceptionCause
from src.model.core.routers import Router, router
from datetime import datetime
from src.model.items.bookings import ItemBooking
import logging
from src.model.items.bookings import Transaction

class ItemStatus(Enum):
    STORED=1
    PROCESSED=2
    CARRIED=3
    DESTROYED=-1
    DELIVERED=4

class Item(Identifiable):
    router:Router=router()
    def __init__(self, holder:ItemsHolder, name: Optional[str] = None) -> None:
        super().__init__(name)
        self._holder=holder
        self._created=datetime.now()
        self._status=ItemStatus.STORED
        self._booking=None
        self._pending_bookings=set()
    
    @property
    def holder(self)->ItemsHolder:
        return self._holder
    
    @holder.setter
    def holder(self,holder:ItemsHolder)->None:
        from src.model.items.bookings.transfer import TranferBooking
        try:
            if self._booking and isinstance(self._booking, TranferBooking):
                assert holder==self._booking._destination
            elif self._booking:
                logging.warn(f"holder assignation not verified for {self}")
            self._holder=holder
        except AssertionError as e:
            raise ValueError() from e

    @property
    def status(self)->ItemStatus:
        return self._status
    
    @status.setter
    def status(self, value:ItemStatus)->None:
        assert isinstance(value, ItemStatus)
        self._changed('status', self._status, value)
        self._status=value

    @property
    def is_free(self)->bool:  
        return not self._booking
    
    @property
    def booking(self)->'ItemBooking':
        return self._booking
    
    @booking.setter
    def booking(self,booking:ItemBooking)->None:
        if booking:
            assert not self._booking, "another booking is already associated with this item"
        elif not booking:
            from src.model.items.bookings import BookingState
            assert self._booking.state in (BookingState.CANCELLED, BookingState.COMMITING, BookingState.ROLLBACKED)
        self._booking=booking

    def transfer(self, destination:Union[ItemsHolder, str], transaction:Optional[Transaction]=None)->None:
        try:
            assert self.is_free, "item is already booked"
            self.router.transfer(self, destination)
        except TransfertException as e:
            raise e
        except AssertionError as e:
            raise TransfertException(TransfertExceptionCause.ALREADY_BOOKED) from e