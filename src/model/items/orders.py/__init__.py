from src.model.items import Item, Identifiable
from typing import Optional

class WorkOrder(Item):
    def __init__(self, name:Optional[str]=None) -> None:
        super().__init__(self, name=name)