from domain.ports.registration_repository import RegistrationRepository
from domain.ports.session_repository import SessionRepository
from domain.entities.registration import Registration, RegistrationStatus
from domain.exceptions import SessionNotFound, SessionNotOpenForRegistration


"""
NOTA: Ver punto 4 en "technical_notes/slice0_y_slice1"

"""


class RegisterToSessionUseCase:
    def __init__(
        self, session_repo: SessionRepository, registration_repo: RegistrationRepository
    ) -> None:
        self.session_repo = session_repo
        self.registration_repo = registration_repo

    def execute(self, session_id: int, user_id: int) -> Registration:
        session = self.session_repo.get_session_by_id(session_id)
        if session is None:
            raise SessionNotFound(session_id)

        if not session.can_accept_registrations():
            raise SessionNotOpenForRegistration(session_id)
        registration = Registration(
            id=None,
            session_id=session.id,
            user_id=user_id,
            status=RegistrationStatus.PENDING,
        )

        registration = self.registration_repo.save_registration(registration)

        return registration
