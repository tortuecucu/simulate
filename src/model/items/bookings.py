from src.model.items import Item

class ItemBooking():
    def __init__(self, item:Item) -> None:
        assert item._booking == None
        self._item=item
        item._booking=self


class TranfertBooking(ItemBooking):
    def __init__(self, item: Item, destination) -> None:
        super().__init__(item)
        self._destination=destination

class ProcessBooking(ItemBooking):
    ...