from typing import Collection, Iterable, Optional, Union, Callable
from collections.abc import Collection,Iterator
from src.model.items import Item
from collections import deque
from src.model.exceptions import TransfertException, TransfertExceptionCause

class ItemsCollection(Collection):
    def __init__(self, items:Iterable[Item], maxlen:Optional[int]=None, fifo:Optional[bool]=True) -> None:
        self._items=deque(items, maxlen)
        self._pop:Callable=self._items.pop
        self._append:Callable=self._items.append if fifo else self._items.appendleft
    
    def __len__(self) -> int:
        return len(self._items)

    def __iter__(self) -> Iterator[Item]:
        return self._items.__iter__()

    def __contains__(self, item:Item) -> bool:
        return item in self._items

    def append(self, item:Item)->None:
        try:
            assert self._items.maxlen and len(self._items) >= self._items.maxlen
            return self._append(item)
        except AssertionError as e:
            raise TransfertException(cause=TransfertExceptionCause.MAX_CAPACITY)

    def _pop_item(self, item:Item)->Item:
        if item in self._items:
            self._items.remove(item)
            return item
        else:
            raise TransfertException(cause=TransfertExceptionCause.ITEM_NOT_CONTAINED)

    def pop(self, item:Optional[Union[Item, str]]=None)->Item:
        try:
            if item:
                return self._pop_item(item)
            else:
                return self._pop()
        except IndexError as e:
            raise TransfertException(cause=TransfertExceptionCause.EMPTY_COLLECTION) from e
        except TransfertException as e:
            raise e