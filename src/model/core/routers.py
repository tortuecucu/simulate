from abc import ABC, abstractmethod
from typing import Set, Iterable, Optional, Union
from model.items.bookings import Transaction, BookingState
from model.items.bookings.transfer import TranferBooking, DirectTransfer
from src.model.items import Item
from src.model.items.holders import ItemsHolder
from src.model.core import Singleton
from src.model.exceptions import TransfertException, TransfertExceptionCause

def router()->'Router':
    return Router()

class Router(Singleton, ABC):
    @abstractmethod
    def transfer(self, item:Item, destination:Union[str, ItemsHolder], transaction:Optional[Transaction]=None)->None:
        """handles the transfert of items from an holder to another

        Args:
            items (Iterable[Item]): items to be transferred
            destination (Union[str, ItemsHolder]): final destination of items
            use_transaction (Optional[bool], optional): If True all transferts must be successuf, otherwise all transferts are aborted. Defaults to True.
        """
        try:
            destination:ItemsHolder = destination if isinstance(destination, ItemsHolder) else self.find_destination(destination)
            assert destination, "destination not set"
            booking=DirectTransfer(item=item, destination=destination)
            assert item.holder.accept_booking(booking)
            assert destination.accept_booking(booking)
            booking.state=BookingState.VALIDATED
            if not transaction:
                booking.commit()
        except AssertionError as e:
            raise TransfertExceptionCause(TransfertExceptionCause.UNKNOWN_DESTINATION) from e
        except TransfertException as e:
            raise e
        except Exception as e:
            raise TransfertException() from e

    def find_destination(identifier:str)->ItemsHolder:
        return ItemsHolder.find(identifier)
