from enum import Enum

class OrderTime(Enum):
    QUEUE=1
    SETUP=2
    PROCESS=3
    WAIT=4
    MOVE=5

class WorkcenterTime(Enum):
    CLOSED=1
    RUNNING=2
    IDLE=3