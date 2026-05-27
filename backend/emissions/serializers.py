from rest_framework import serializers

from .models import AuditLog, DataUpload, EmissionRecord


class DataUploadSerializer(serializers.ModelSerializer):
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


class EmissionRecordSerializer(serializers.ModelSerializer):
    organization_name = serializers.CharField(source="organization.name", read_only=True)
    upload_file_name = serializers.CharField(source="upload.file_name", read_only=True)

    class Meta:
        model = EmissionRecord
        fields = [
            "id",
            "organization",
            "organization_name",
            "upload",
            "upload_file_name",
            "source_type",
            "activity_type",
            "raw_quantity",
            "raw_unit",
            "normalized_quantity",
            "normalized_unit",
            "estimated_co2e_kg",
            "scope",
            "period_start",
            "period_end",
            "suspicious_flag",
            "suspicious_reason",
            "review_status",
            "source_metadata",
            "is_locked",
            "created_at",
        ]


class AuditLogSerializer(serializers.ModelSerializer):
    record_id = serializers.UUIDField(source="emission_record.id", read_only=True)
    activity_type = serializers.CharField(source="emission_record.activity_type", read_only=True)

    class Meta:
        model = AuditLog
        fields = [
            "id",
            "record_id",
            "activity_type",
            "action",
            "performed_by",
            "notes",
            "performed_at",
        ]
