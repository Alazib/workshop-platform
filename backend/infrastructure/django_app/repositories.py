from typing import Optional
from domain.entities.session import Session, SessionStatus
from domain.ports.session_repository import SessionRepository
from .models import SessionModel


class DjangoSessionRepository(SessionRepository):
    """
    Adaptador Django del puerto SessionRepository.

    Traduce entre:
    - SessionModel (ORM / infraestructura)
    - Session (entidad de dominio)
    """

    def get_session_by_id(self, session_id: int) -> Optional[Session]:
        try:
            model = SessionModel.objects.get(id=session_id)
        except SessionModel.DoesNotExist:
            return None

        return self._to_domain(model)

    def save_session(self, session: Session) -> None:
        try:
            model = SessionModel.objects.get(
                id=session.id
            )  # Si existe la recuperaré y se hará un UPDATE
        except SessionModel.DoesNotExist:
            model = None

        if model is None:
            model = (
                SessionModel()
            )  # Si NO existe se hará un INSERT. Ojo! aquí no puedo pasarle 'id=session.id'
            # puesto que (como hemos hecho en models.py) es Django quien asigna los 'id' automáticamente.

        self._update_model_from_domain(model, session)
        model.save()

    # -------------------------
    # MAPEOS (privados)
    # -------------------------

    def _to_domain(self, model: SessionModel) -> Session:
        return Session(
            id=model.id,  # type: ignore -> Django añade 'id' automáticamente; el type checker puede no inferirlo porque el modelo no tiene el id en estático.
            workshop_id=model.workshop_id,
            title=model.title,
            starts_at=model.starts_at,
            ends_at=model.ends_at,
            capacity_max=model.capacity_max,
            status=SessionStatus(model.status),
        )

    def _update_model_from_domain(self, model: SessionModel, session: Session) -> None:
        model.workshop_id = session.workshop_id
        model.title = session.title
        model.starts_at = session.starts_at
        model.ends_at = session.ends_at
        model.capacity_max = session.capacity_max
        model.status = session.status.value
