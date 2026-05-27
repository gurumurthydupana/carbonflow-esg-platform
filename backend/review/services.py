from emissions.models import AuditLog


def add_audit_log(record, action, performed_by, notes=""):
    AuditLog.objects.create(
        emission_record=record,
        action=action,
        performed_by=performed_by,
        notes=notes or "",
    )
