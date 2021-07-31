from django.db.models import fields
from core.models import Csv
from rest_framework import serializers


class CsvSerializer(serializers.ModelSerializer):
    """Serializer for uploading csv"""

    class Meta:
        model = Csv
        fields = ("id", "file")
        read_only_fields = ("id",)
