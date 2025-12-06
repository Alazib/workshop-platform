from datetime import datetime, timedelta
from domain.entities.session import Session, SessionStatus
from application.use_cases.register_to_session import RegisterToSessionUseCase
from application.repositories_in_memory.in_memory_session_repository import (
    InMemorySessionRepository,
)
from application.repositories_in_memory.in_memory_registration_repository import (
    InMemoryRegistrationRepository,
)
from domain.exceptions import SessionNotFound, SessionNotOpenForRegistration


def test_register_success():
    print("\n---- TEST 1: Registro exitoso ----")

    # 1. Crear repos falsos
    session_repo = InMemorySessionRepository()
    registration_repo = InMemoryRegistrationRepository()

    # 2. Añadir una sesión válida (publicada)
    session = Session(
        id=1,
        workshop_id=10,
        title="Taller de Prueba",
        starts_at=datetime.now() + timedelta(days=1),
        ends_at=datetime.now() + timedelta(days=1, hours=2),
        capacity_max=20,
        status=SessionStatus.PUBLISHED,
    )
    session_repo.save_session(session)

    # 3. Ejecutar caso de uso (Registrase a una sesión)
    use_case = RegisterToSessionUseCase(session_repo, registration_repo)

    # 4. Ejecutar inscripción
    registration = use_case.execute(session_id=1, user_id=99)

    print("Registro creado correctamente:")
    print(registration)
    print("ID asignado:", registration.id)


def test_session_not_found():
    print("\n---- TEST 2: Sesión no encontrada ----")

    session_repo = InMemorySessionRepository()
    registration_repo = InMemoryRegistrationRepository()
    use_case = RegisterToSessionUseCase(session_repo, registration_repo)

    try:
        use_case.execute(session_id=999, user_id=1)
    except SessionNotFound as e:
        print("OK → Lanzó SessionNotFound:", e)


def test_session_not_open():
    print("\n---- TEST 3: Sesión no aceptando inscripciones ----")

    session_repo = InMemorySessionRepository()
    registration_repo = InMemoryRegistrationRepository()

    session = Session(
        id=2,
        workshop_id=10,
        title="Taller Cerrado",
        starts_at=datetime.now() + timedelta(days=1),
        ends_at=datetime.now() + timedelta(days=1, hours=2),
        capacity_max=20,
        status=SessionStatus.DRAFT,  # <--- No publicada
    )
    session_repo.save_session(session)

    use_case = RegisterToSessionUseCase(session_repo, registration_repo)

    try:
        use_case.execute(session_id=2, user_id=44)
    except SessionNotOpenForRegistration as e:
        print("OK → Lanzó SessionNotOpenForRegistration:", e)


if __name__ == "__main__":
    test_register_success()
    test_session_not_found()
    test_session_not_open()
