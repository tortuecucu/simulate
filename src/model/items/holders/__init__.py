from model.core import Identifiable
from src.model.items import Item
from typing import Union, Optional,Set
from src.model.items.collections import ItemsCollection
from src.model.exceptions import TransfertException, TransfertExceptionCause
from src.model.items.bookings import ItemBooking, BookingState
from src.model.items.bookings.transfer import TranferBooking
class ItemsHolder(Identifiable):
    def __init__(self, name: Optional[str] = None, items:Optional[ItemsCollection[Item]]=None, maxlen:Optional[int]=None) -> None:
        super().__init__(name)
        if items and maxlen: assert len(items) >= maxlen
        self._items=items if items else ItemsCollection(maxlen=maxlen)
        self._pending_bookings:Set[ItemBooking]=set() #list all accepted but not applied bookings
    
    def __iter__(self):
        return self._items.__iter__()
 
    def __next__(self):
        return self._items.__next__()
    
    def __len__(self)->int:
        return len(self._items)

    def input(self, item:Item):
        if self._maxlen and len(self) >= self._maxlen:
            raise TransfertException(cause=TransfertExceptionCause.MAX_CAPACITY)
        self._item_in(item)

    def _item_in(self, item:Item):
        return self._items.append(item)

    def _item_out(self, item:Optional[Item]=None):
        return self._items.pop(item)
    
    def output(self, item:Optional[Union[Item, str]]=None):
        return self._item_out(item)
    
    def accept_booking(self, booking:'ItemBooking')->bool:
        try:
            assert booking.state not in (BookingState.CANCELLED, BookingState.COMMITTED, BookingState.ROLLBACKED)
            if isinstance(booking, TranferBooking):
                if self==booking._destination (self._items.maxlen and len(self)<=self._items.maxlen) or self._items.maxlen==None:
                    self._pending_bookings.add(booking)
                    return True
                if self==booking._origin:
                    assert booking.item in self
                    self._pending_bookings.add(booking)
                else:
                    return False
            else:
                return True
        except AssertionError as e:
            raise ValueError from e
    
    def transfer_in(self, booking:TranferBooking)->None:
        try:
            if self._items.maxlen:
                assert len(self)<=self._items.maxlen
        except AssertionError as e:
            raise TransfertException(TransfertExceptionCause.MAX_CAPACITY)
        try:
            assert isinstance(booking, TranferBooking)
        except AssertionError as e:
            raise ValueError from e
        try:
            assert booking in self._pending_bookings
        except:
            raise TransfertException(TransfertExceptionCause.BOOKING_NOT_ACEPTED)
        self._items.append(booking.item)
    
    def transfer_out(self, booking:TranferBooking)->None:
        try:
            assert booking.item in self._items
        except AssertionError:
            raise TransfertException(TransfertExceptionCause.ITEM_NOT_CONTAINED)
        try:
            assert booking in self._pending_bookings
        except:
            raise TransfertException(TransfertExceptionCause.BOOKING_NOT_ACEPTED)
        try:
            self._items._pop_item(booking.item)
        except IndexError as e:
            raise TransfertException(TransfertExceptionCause.ITEM_NOT_CONTAINED) from e

    def cancel_booking(self, booking:ItemBooking)->bool:
        try:
            assert booking.item.holder==self, f"item {booking.item} is not held by {self}"
            if booking.state in (BookingState.INIT, BookingState.VALIDATED, BookingState.WAITING_TRANSACTION):
                booking.state==BookingState.CANCELLED
                booking.item.booking=None
                return True
            else:
                return False

        except AssertionError as e:
            raise ValueError() from e