from typing import Optional

from domain.entities.session import Session, SessionStatus
from domain.entities.registration import Registration, RegistrationStatus

from domain.ports.session_repository import SessionRepository
from domain.ports.registration_repository import RegistrationRepository

from .models import SessionModel
from .models import RegistrationModel

"""
NOTA: Ver punto 6 en "technical_notes/slice0_y_slice1"

"""


class DjangoSessionRepository(SessionRepository):

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
            )  # Si existe la recuperaré y se hará un UPDATE (lo decide automaticamente el método .save() de Django)
        except SessionModel.DoesNotExist:
            model = None

        if model is None:
            model = SessionModel()
            # Si NO existe se hará un INSERT (lo decide automaticamente el método .save() de Django).
            # Ojo! aquí no puedo pasarle 'id=session.id'puesto que (como hemos hecho en models.py) es Django quien asigna los 'id' automáticamente.

        self.apply_domain_to_model(model, session)
        model.save()

    # -------------------------
    # MAPEOS (privados)
    # -------------------------

    def _to_domain(self, model: SessionModel) -> Session:
        return Session(
            id=model.id,  # type: ignore -> Django añade el atributo 'id' de forma dinámica; el type checker puede no inferirlo porque el modelo no tiene el id en estático.
            workshop_id=model.workshop_id,
            title=model.title,
            starts_at=model.starts_at,
            ends_at=model.ends_at,
            capacity_max=model.capacity_max,
            status=SessionStatus(model.status),
        )

    def apply_domain_to_model(self, model: SessionModel, session: Session) -> None:
        model.workshop_id = session.workshop_id
        model.title = session.title
        model.starts_at = session.starts_at
        model.ends_at = session.ends_at
        model.capacity_max = session.capacity_max
        model.status = session.status.value


class DjangoRegistrationRepository(RegistrationRepository):
    def get_registration_by_id(self, registration_id: int) -> Optional[Registration]:
        try:
            model = RegistrationModel.objects.get(id=registration_id)
        except RegistrationModel.DoesNotExist:
            return None

        return self._to_domain(model)

    def save_registration(self, registration: Registration) -> Registration:

        if registration.id is None:
            model = RegistrationModel()
        else:
            try:
                model = RegistrationModel.objects.get(id=registration.id)
            except RegistrationModel.DoesNotExist:
                model = RegistrationModel()

        self._apply_domain_to_model(model, registration)

        model.save()  # Se salva el objeto del modelo en la BBDD y Django inyecta en memoria en "model" el id. Por eso luego podemos hacer self._to_domain(model) y el modelo ya tiene el id

        return self._to_domain(model)

    # -------------------------
    # MAPEOS (privados)
    # -------------------------

    def _to_domain(self, model: RegistrationModel) -> Registration:
        return Registration(
            id=model.id,  # type: ignore[attr-defined]
            session_id=model.session_id,  # type: ignore
            user_id=model.user_id,
            status=RegistrationStatus(model.status),
            created_at=model.created_at,
            confirmation_date=model.confirmation_date,
        )

    def _apply_domain_to_model(
        self, model: RegistrationModel, registration: Registration
    ) -> None:
        model.session = SessionModel.objects.get(id=registration.session_id)
        model.user_id = registration.user_id
        model.status = registration.status.value
        model.confirmation_date = registration.confirmation_date
