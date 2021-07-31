from django.db import models
import uuid
import os


def csv_file_path(instance, filename) -> str:
    """Generate file path for new csv file"""
    ext = filename.split(".")[-1]
    filename = f"{uuid.uuid4()}.{ext}"

    # Destination path
    return os.path.join("uploads/csv_files/", filename)


class Csv(models.Model):
    """Csv Object"""

    file = models.FileField(blank=False, null=False, upload_to=csv_file_path)
    uploaded_at = models.DateTimeField(auto_now_add=True)
