from enum import Enum
from typing import Optional

class TransfertExceptionCause(Enum):
    CAUSE_UNKNOWN=0
    MAX_CAPACITY=1
    ITEM_NOT_CONTAINED=2
    EMPTY_COLLECTION=3
    ALREADY_BOOKED=4
    UNKNOWN_DESTINATION=5
    CONTAINER_FROZEN=6
    BOOKING_NOT_ACEPTED=7


class TransfertException(Exception):
    def __init__(self, cause:Optional[TransfertExceptionCause], *args: object) -> None:
        super().__init__(*args)
        self._cause=cause