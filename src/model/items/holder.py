from src.model.core import Identifiable
from src.model.items import Item
from typing import Union, Optional,Iterable
from src.model.items.collections import ItemsCollection
from src.model.exceptions import TransfertException, TransfertExceptionCause

class ItemsHolder(Identifiable):
    def __init__(self, name: Optional[str] = None, items:Optional[ItemsCollection[Item]]=None, maxlen:Optional[int]=None) -> None:
        super().__init__(name)
        self._items=items if items else ItemsCollection(maxlen=maxlen)
    
    def __iter__(self):
        return self._items.__iter__()
 
    def __next__(self):
        return self._items.__next__()
    
    def __len__(self)->int:
        return len(self._items)

    def input(self, item:Item):
        ... #TODO: handle maxlen
        if self._maxlen and len(self) >= self._maxlen:
            raise TransfertException(cause=TransfertExceptionCause.MAX_CAPACITY)
        self._item_in(item)

    def _item_in(self, item:Item):
        ...

    def _item_out(self, item:Optional[Item]=None):
        ...         
    
    def output(self, item:Optional[Union[Item, str]]=None):
        ...