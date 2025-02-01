from rest_framework import serializers

from .models import FileUploaded


def trim_field(data):
    if isinstance(data, str):
        return data.strip()
    return data


class FileUploadedSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileUploaded
        fields = [
            "id",
            "name",
            "file",
            "text",
            "access_code",
            "location",
            "created_at",
        ]
        read_only_fields = ["created_at", "delete_at", "access_code"]

    def validate(self, data):
        for field in data:
            data[field] = trim_field(data[field])

        if not data.get("file") and not data.get("text"):
            raise serializers.ValidationError("Either file or text must be provided")

        return data
