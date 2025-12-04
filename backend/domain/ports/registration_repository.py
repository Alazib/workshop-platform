from domain.entities.registration import Registration
from typing import Optional, Protocol


class RegistrationRepository(Protocol):
    def get_registration_by_id(
        self, registration_id: int
    ) -> Optional[Registration]: ...

    def save_registration(self, registration: Registration) -> None: ...
