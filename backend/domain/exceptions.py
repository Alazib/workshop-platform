class DomainError(Exception):
    pass


class SessionNotFound(DomainError):
    def __init__(self, session_id: int) -> None:
        message = f"La sesión con id={session_id} no existe."
        super().__init__(message)
        self.session_id = session_id


class SessionNotOpenForRegistration(DomainError):
    def __init__(self, session_id: int) -> None:
        message = f"La sesión con id={session_id} no acepta inscripciones."
        super().__init__(message)
        self.session_id = session_id
