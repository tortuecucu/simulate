from src.model.items.holders import ItemsHolder
from typing import Optional
from src.model.items.collections import ItemsCollection
from src.model.items import Item
from src.model.core.routers import Router, router
from src.model.items.bookings import Transaction

class Lot(ItemsHolder):
    """Lot buffer items before transferring until the lot size is reached

    """
    def __init__(self, lot_size:int, destination, name: Optional[str] = None, items: Optional[ItemsCollection[Item]] = None, maxlen: Optional[int] = None) -> None:
        super().__init__(name, items, maxlen)
        self._lot_size=lot_size
        self._destination=destination
        self._router:Router=router()
        if items: self._flush()
    
    def input(self, item:Item):
        super().input(item)
        self._flush()
    
    def _flush(self)->None:
        if len(self._items)>=self._lot_size:
            with Transaction() as t:
                [i.transfer(self._destination, t) for i in self._items]
                t.commit()