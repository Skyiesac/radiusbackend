from datetime import timedelta

from django.db import models
from django.utils import timezone

from .tasks import delete_file


# Create your models here.
class FileUploaded(models.Model):
    name = models.CharField(max_length=100)
    file = models.FileField(upload_to="file-shared/", null=True)
    text = models.TextField(null=True)
    access_code = models.CharField(max_length=10, unique=True)
    latitude = models.FloatField()
    longitude = models.FloatField()
    created_at = models.DateTimeField(auto_now=True)
    delete_at = models.DateTimeField(null=True)

    def __str__(self):
        return self.text

    def generate_access_code(self):
        import random
        import string

        return "".join(random.choices(string.ascii_uppercase + string.digits, k=10))

    def save(self, *args, **kwargs):
        if not self.access_code:
            self.access_code = self.generate_access_code()
        is_new = self._state.adding
        if is_new:
            deletion_time = FileDeletionTime.objects.first()
            if deletion_time:
                self.delete_at = timezone.now() + timedelta(
                    minutes=deletion_time.deletion_mins,
                )

        super().save(*args, **kwargs)

        if is_new and self.delete_at:
            delete_file.apply_async(
                args=[self.id],
                eta=self.delete_at,
            )


class FileDeletionTime(models.Model):
    deletion_mins = models.IntegerField()

    def __str__(self):
        return self.deletion_mins
