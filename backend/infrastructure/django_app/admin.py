from django.contrib import admin
from .models import SessionModel, RegistrationModel


@admin.register(SessionModel)
class SessionAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "status", "starts_at", "ends_at", "capacity_max")
    list_filter = ("status", "starts_at")
    search_fields = ("title",)


@admin.register(RegistrationModel)
class RegistrationAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "session_id",
        "user_id",
        "status",
        "created_at",
        "confirmation_date",
    )
    list_filter = ("status", "created_at")
    search_fields = ("user_id",)
