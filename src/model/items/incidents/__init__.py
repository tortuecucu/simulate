from src.model.items import WorkOrder
from enum import Enum

class IncidentState(Enum):
    NEW=1
    ACTIVE=2
    ON_HOLD=2
    RESOLVED=3

class OnholdReason(Enum):
    USER=1
    OTHER=2

class Incident(WorkOrder):
    #state, holdreason, business_service, priority, number, 
    def __init__(self, id: int, name: str, assigned_to, priority, status) -> None:
        super().__init__(id, name, assigned_to)