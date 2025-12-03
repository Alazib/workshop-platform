from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


class RegistrationStatus(Enum):
    RESERVED = "reserved"
    PENDING = "pending"
    CONFIRMED = "confirmed"
    CANCELLED_BY_USER = "cancelled_by_user"
    CANCELLED_BY_ORGANIZER = "cancelled_by_organizer"
    ATTENDED = "attended"
    NO_SHOW = "no_show"


@dataclass
class Registration:
    id: int
    session_id: int
    user_id: int
    status: RegistrationStatus
    created_at: datetime = field(default_factory=datetime.now)
    confirmation_date: datetime | None = None

    def confirm(self) -> None:

        can_confirm = (
            self.status == RegistrationStatus.RESERVED
            or self.status == RegistrationStatus.PENDING
        )

        if can_confirm:
            self.status = RegistrationStatus.CONFIRMED
            self.confirmation_date = datetime.now()
        else:
            raise ValueError(
                f"El registro no puede pasar de status {self.status} a {RegistrationStatus.CONFIRMED}"
            )
