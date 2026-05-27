from django.urls import path

from .views import emissions_summary, list_audit_logs, list_emission_records

urlpatterns = [
    path("records/", list_emission_records),
    path("summary/", emissions_summary),
    path("audit-logs/", list_audit_logs),
]
