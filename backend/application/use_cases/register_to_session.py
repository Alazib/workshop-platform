from domain.ports.registration_repository import RegistrationRepository
from domain.ports.session_repository import SessionRepository


class RegisterToSessionUseCase:
    def __init__(
        self, session_repo: SessionRepository, registration_repo: RegistrationRepository
    ) -> None:

        self.session_repo = session_repo
        self.registration_repo = registration_repo

    def execute(self, session_id: int, user_id: int) -> None: ...
