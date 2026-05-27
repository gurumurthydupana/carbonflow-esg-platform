from django.contrib import admin
from .models import DataUpload, EmissionRecord, AuditLog


@admin.register(DataUpload)
class DataUploadAdmin(admin.ModelAdmin):
    list_display = (
        'file_name',
        'source_type',
        'upload_status',
        'uploaded_at'
    )

    list_filter = ('source_type', 'upload_status')


@admin.register(EmissionRecord)
class EmissionRecordAdmin(admin.ModelAdmin):
    list_display = (
        'activity_type',
        'estimated_co2e_kg',
        'scope',
        'review_status',
        'suspicious_flag',
        'is_locked'
    )

    list_filter = (
        'scope',
        'review_status',
        'suspicious_flag',
        'is_locked'
    )

    search_fields = ('activity_type',)


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = (
        'action',
        'performed_by',
        'performed_at'
    )

    list_filter = ('action',)