from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class SessionStatus(Enum):
    DRAFT = "draft"
    ANNOUNCED = "announced"
    PUBLISHED = "published"
    FULL = "full"
    CANCELLED = "cancelled"
    COMPLETED = "completed"
    ARCHIVED = "archived"


@dataclass
class Session:
    id: int  # TODO tendrá que ser "int|NONE", por el mismo motivo que lo es Registration
    workshop_id: int
    title: str
    starts_at: datetime
    ends_at: datetime
    capacity_max: int
    status: SessionStatus

    def can_accept_registrations(self) -> bool:
        return self.status == SessionStatus.PUBLISHED
