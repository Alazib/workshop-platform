from domain.entities.session import Session
from typing import Optional, Protocol


class SessionRepository(Protocol):
    def get_session_by_id(self, session_id: int) -> Optional[Session]: ...

    def save_session(
        self, session: Session
    ) -> None: ...  # TODO Tendrá que devolver Sesión por los motivos de ID ya citados
