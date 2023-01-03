from enum import Enum
from typing import Optional

class TransfertExceptionCause(Enum):
    MAX_CAPACITY=1
    ITEM_NOT_CONTAINED=2
    EMPTY_COLLECTION=3

class TransfertException(Exception):
    def __init__(self, cause:Optional[TransfertExceptionCause], *args: object) -> None:
        super().__init__(*args)
        self._cause=cause