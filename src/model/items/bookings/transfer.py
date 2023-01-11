from src.model.items import Item, ItemStatus
from src.model.items.bookings import ItemBooking, BookingState
from src.model.items.bookings import CommitException, RollbackException

class TranferBooking(ItemBooking):
    def __init__(self, item: Item, destination) -> None:
        super().__init__(item)
        self._origin=item._holder
        self._destination=destination

class DirectTransfer(TranferBooking):
    def commit(self) -> None:
        try:
            assert self.item.status not in (ItemStatus.DELIVERED, ItemStatus.DESTROYED)
            assert self.state not in (BookingState.CANCELLED, BookingState.COMMITTED, BookingState.ROLLBACKED)
            self.state=BookingState.COMMITING
            self._origin.transfer_out(self)
            self._destination.transfer_in(self)
            self.state=BookingState.COMMITTED
            self.item.booking=None
        except AssertionError as e:
            raise CommitException from e

    def rollback(self) -> None:
        try:
            assert self.state not in (BookingState.COMMITTED, BookingState.ROLLBACKED)
            self.state=BookingState.ROLLBACKED
            self.item.booking=None
        except AssertionError as e:
            raise RollbackException from e

class RoutedTransfer(TranferBooking):
    pass