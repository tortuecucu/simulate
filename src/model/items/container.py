from src.model.items import Item
from model.items.bookings import ItemBooking
from src.model.items.holders import ItemsHolder
from typing import Optional, Iterable, Set, Union, Callable
from collections import namedtuple
from src.model.exceptions import TransfertException, TransfertExceptionCause

LeveledItem=namedtuple('LeveledItem', ['level', 'item'])

class ContainerBooking(ItemBooking):
    ...

class Container(Item, ItemsHolder):
    """Containers are special items that are able to contains other items
    """
    def __init__(self, holder: ItemsHolder, name: Optional[str] = None, items:Optional[Iterable[Item]]=None, maxlen:Optional[int]=None, frozen:Optional[bool]=False, reusable:Optional[bool]=True) -> None:
        super().__init__(holder, name)
        ItemsHolder.__init__(holder,name, items, maxlen)
        self._frozen=frozen
        self._reusable=reusable
    
    def unpack(self, destination:Optional[Union[str, ItemsHolder]]=None)->Set[Item]:
        #TODO: check item bookings
        ...
    
    def extend(self, items:Iterable[Item])->None:
        try:
            assert not self._frozen, "container is frozen"
            #TODO: check item bookings
            ...
        except AssertionError as e:
            raise TransfertException(TransfertExceptionCause.CONTAINER_FROZEN) from e
    
    @property
    def is_reusable(self)->bool:
        return self._reusable
    
    @property
    def is_frozen(self)->bool:
        return self._frozen
    
    def input(self, item:Item):
        try:
            assert not self._frozen, "container is frozen"
            item.transfer(self)

            
        except AssertionError as e:
            raise TransfertException(TransfertExceptionCause.CONTAINER_FROZEN) from e
    
    def output(self, item:Optional[Union[Item, str]]=None):
        try:
            assert not self._frozen, "container is frozen"
            #TODO: check item bookings
            ...
        except AssertionError as e:
            raise TransfertException(TransfertExceptionCause.CONTAINER_FROZEN) from e

    def ml(self, filter:Callable)->Set[LeveledItem]:
        return ml(self, filter)


def ml(base:Iterable[Item], filter:Callable)->Set[LeveledItem]:
    ... #TODO: code it