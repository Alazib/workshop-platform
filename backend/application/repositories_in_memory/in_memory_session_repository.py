from typing import Optional
from domain.entities.session import Session
from domain.ports.session_repository import SessionRepository


"""
NOTA: Ver punto 5 en ""technical_notes/slice0_y_slice1"
"""


class InMemorySessionRepository(SessionRepository):

    def __init__(self) -> None:

        self._sessions: dict[int, Session] = {}
        # Diccionario para almacenar sesiones: id -> Session

    def get_session_by_id(self, session_id: int) -> Optional[Session]:
        return self._sessions.get(session_id)

    def save_session(
        self, session: Session
    ) -> None:  # TODO Tendrá que devolver Sesión por los motivos de ID ya citados
        self._sessions[session.id] = session
