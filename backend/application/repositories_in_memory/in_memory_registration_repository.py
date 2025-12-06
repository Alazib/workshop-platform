from typing import Optional
from domain.entities.registration import Registration
from domain.ports.registration_repository import RegistrationRepository


"""
NOTA: Ver punto 5 en ""technical_notes/slice0_y_slice1"
"""


class InMemoryRegistrationRepository(RegistrationRepository):

    def __init__(self) -> None:
        self._registrations: dict[int, Registration] = {}
        self._counter: int = 1  # Simulador de autoincremento de IDs

    def get_registration_by_id(self, registration_id: int) -> Optional[Registration]:
        return self._registrations.get(registration_id)

    def save_registration(self, registration: Registration) -> None:
        # Si viene con id=0 (nuevo), le damos uno "real"
        if registration.id == 0:
            registration.id = self._counter
            self._counter += 1

        self._registrations[registration.id] = registration
