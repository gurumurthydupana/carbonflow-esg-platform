from rest_framework import serializers

from emissions.models import DataUpload


class UploadCreateSerializer(serializers.Serializer):
    organization_id = serializers.UUIDField()
    source_type = serializers.ChoiceField(choices=DataUpload.SOURCE_CHOICES)
    file = serializers.FileField()


class UploadListSerializer(serializers.ModelSerializer):
    organization_name = serializers.CharField(source="organization.name", read_only=True)

    class Meta:
        model = DataUpload
        fields = [
            "id",
            "organization",
            "organization_name",
            "source_type",
            "file_name",
            "upload_status",
            "total_rows",
            "failed_rows",
            "uploaded_at",
        ]
