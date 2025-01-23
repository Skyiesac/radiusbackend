from django.contrib import admin

from .models import FileDeletionTime
from .models import FileUploaded


@admin.register(FileUploaded)
class FileUploadedAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "access_code",
        "latitude",
        "longitude",
        "created_at",
        "delete_at",
    )
    search_fields = ("name", "access_code")
    list_filter = ("created_at", "delete_at")
    readonly_fields = ("created_at", "delete_at")


@admin.register(FileDeletionTime)
class FileDeletionTimeAdmin(admin.ModelAdmin):
    list_display = ("deletion_mins",)
    search_fields = ("deletion_mins",)
