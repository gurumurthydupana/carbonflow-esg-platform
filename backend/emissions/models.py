import uuid
from django.db import models
from core.models import Organization


class DataUpload(models.Model):
    SOURCE_CHOICES = [
        ('sap', 'SAP Export'),
        ('utility', 'Utility CSV'),
        ('travel', 'Travel Data'),
    ]

    STATUS_CHOICES = [
        ('processing', 'Processing'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name='uploads'
    )

    source_type = models.CharField(max_length=50, choices=SOURCE_CHOICES)

    file_name = models.CharField(max_length=255)

    upload_status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='processing'
    )

    total_rows = models.IntegerField(default=0)

    failed_rows = models.JSONField(default=list, blank=True)

    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.file_name} ({self.source_type})"


class EmissionRecord(models.Model):
    REVIEW_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        related_name='records'
    )

    upload = models.ForeignKey(
        DataUpload,
        on_delete=models.CASCADE,
        related_name='records'
    )

    source_type = models.CharField(max_length=50)

    activity_type = models.CharField(max_length=255)

    raw_quantity = models.FloatField()

    raw_unit = models.CharField(max_length=50)

    normalized_quantity = models.FloatField()

    normalized_unit = models.CharField(max_length=50)

    estimated_co2e_kg = models.FloatField()

    scope = models.CharField(max_length=20)

    period_start = models.DateField()

    period_end = models.DateField()

    suspicious_flag = models.BooleanField(default=False)

    suspicious_reason = models.TextField(blank=True)

    review_status = models.CharField(
        max_length=20,
        choices=REVIEW_CHOICES,
        default='pending'
    )

    source_metadata = models.JSONField(default=dict, blank=True)

    is_locked = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.activity_type} - {self.estimated_co2e_kg} kg CO2e"


class AuditLog(models.Model):
    ACTION_CHOICES = [
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('locked', 'Locked'),
        ('updated', 'Updated'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    emission_record = models.ForeignKey(
        EmissionRecord,
        on_delete=models.CASCADE,
        related_name='audit_logs'
    )

    action = models.CharField(max_length=50, choices=ACTION_CHOICES)

    performed_by = models.CharField(max_length=255)

    notes = models.TextField(blank=True)

    performed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.action} - {self.performed_by}"