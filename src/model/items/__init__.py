from src.model.core import Identifiable
from typing import Optional, Union
from src.model.items.holder import ItemsHolder
from enum import Enum

class ItemStatus(Enum):
    STORED=1
    PROCESSED=2
    CARRIED=3
    DESTROYED=-1

class Item(Identifiable):
    def __init__(self, holder:ItemsHolder, name: Optional[str] = None, ) -> None:
        super().__init__(name)
        self._holder=holder
        self._status=ItemStatus.STORED
        self._booking=None

    @property
    def status(self)->ItemStatus:
        return self._status

    @property
    def is_free(self)->bool:  
        return not self._booking

    def transfert(self, to:Union[ItemsHolder, str])->bool:
        ...




