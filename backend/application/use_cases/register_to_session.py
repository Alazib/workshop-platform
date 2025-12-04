from domain.ports.registration_repository import RegistrationRepository
from domain.ports.session_repository import SessionRepository
from domain.entities.registration import Registration, RegistrationStatus


class RegisterToSessionUseCase:
    def __init__(
        self, session_repo: SessionRepository, registration_repo: RegistrationRepository
    ) -> None:
        self.session_repo = session_repo
        self.registration_repo = registration_repo

    def execute(self, session_id: int, user_id: int) -> Registration:
        session = self.session_repo.get_session_by_id(session_id)
        if session is None:
            raise ValueError("Sesión no encontrada")

        if not session.can_accept_registrations():
            raise ValueError("La sesión no acepta inscripciones")

        registration = Registration(
            id=0,
            session_id=session.id,
            user_id=user_id,
            status=RegistrationStatus.PENDING,
        )

        self.registration_repo.save_registration(registration)

        return registration
