from celery import shared_task
from django.core.files.storage import default_storage


@shared_task
def delete_file(file_id):
    """Delete a specific file by ID"""
    from .models import FileUploaded

    try:
        file = FileUploaded.objects.get(id=file_id)

        if file.file and default_storage.exists(file.file.name):
            default_storage.delete(file.file.name)

        file.delete()

        return f"Successfully deleted file {file_id}"
    except FileUploaded.DoesNotExist:
        return f"File {file_id} already deleted or does not exist"
    except Exception as e:
        return f"Error deleting file {file_id}: {e!s}"
