from django.db import models


class SessionModel(models.Model):

    # Se opta por no declarar los "id" en los modelos pues Django lo añade automáticamente:
    # id = AutoField(primary_key=True)

    workshop_id = models.IntegerField()
    title = models.CharField(max_length=200)
    starts_at = models.DateTimeField()
    ends_at = models.DateTimeField()
    capacity_max = models.IntegerField()

    STATUS_DRAFT = "draft"
    STATUS_ANNOUNCED = "announced"
    STATUS_PUBLISHED = "published"
    STATUS_FULL = "full"
    STATUS_CANCELLED = "cancelled"
    STATUS_COMPLETED = "completed"
    STATUS_ARCHIVED = "archived"

    STATUS_CHOICES = [
        (STATUS_DRAFT, "Draft"),
        (STATUS_ANNOUNCED, "Announced"),
        (STATUS_PUBLISHED, "Published"),
        (STATUS_FULL, "Full"),
        (STATUS_CANCELLED, "Cancelled"),
        (STATUS_COMPLETED, "Completed"),
        (STATUS_ARCHIVED, "Archived"),
    ]

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=STATUS_DRAFT,
    )

    class Meta:
        db_table = "sessions"

    def __str__(self) -> str:
        return f"La sesión {self.title} se encuentra en estado {self.get_status_display()}"  # type: ignore -> (se ignora error pues 'get_status_display()' lo añade Django en runtime para campos con CHOICES y
        # el analizador de tipos está mirando tan solo el código estático).


class RegistrationModel(models.Model):

    # Relación con SessionModel (clave foránea en Django)
    session_id = models.ForeignKey(
        "django_app.SessionModel",
        on_delete=models.CASCADE,
        related_name="registrations",
    )

    user_id = models.IntegerField()

    STATUS_RESERVED = "reserved"
    STATUS_PENDING = "pending"
    STATUS_CONFIRMED = "confirmed"
    STATUS_CANCELLED_BY_USER = "cancelled_by_user"
    STATUS_CANCELLED_BY_ORGANIZER = "cancelled_by_organizer"
    STATUS_ATTENDED = "attended"
    STATUS_NO_SHOW = "no_show"

    STATUS_CHOICES = [
        (STATUS_RESERVED, "Reserved"),
        (STATUS_PENDING, "Pending"),
        (STATUS_CONFIRMED, "Confirmed"),
        (STATUS_CANCELLED_BY_USER, "Cancelled by user"),
        (STATUS_CANCELLED_BY_ORGANIZER, "Cancelled by organizer"),
        (STATUS_ATTENDED, "Attended"),
        (STATUS_NO_SHOW, "No show"),
    ]

    status = models.CharField(
        max_length=30,
        choices=STATUS_CHOICES,
        default=STATUS_PENDING,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    confirmation_date = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "registrations"

    def __str__(self) -> str:
        return f"El registro del usuario {self.user_id} para la sesión {self.session_id} se encuentra en estado ({self.get_status_display()})"  # type: ignore
