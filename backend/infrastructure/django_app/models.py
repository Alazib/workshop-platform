from django.db import models


class SessionModel(models.Model):

    # Se opta por no declarar el "id" de SessionModel pues Django lo añade automáticamente:
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
        return f"{self.title} ({self.get_status_display()})"  # type: ignore -> (se ignora error pues 'get_status_display()' lo añade Django en runtime para campos con CHOICES y
        # el analizador de tipos está mirando tan solo el código estático).
