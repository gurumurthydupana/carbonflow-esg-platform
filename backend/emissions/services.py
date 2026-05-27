from django.db.models import Sum

from .models import EmissionRecord


def get_emissions_summary(organization_id=None):
    queryset = EmissionRecord.objects.all()
    if organization_id:
        queryset = queryset.filter(organization_id=organization_id)

    total_kg = queryset.aggregate(total=Sum("estimated_co2e_kg"))["total"] or 0
    by_scope = (
        queryset.values("scope")
        .annotate(total_kg=Sum("estimated_co2e_kg"))
        .order_by("scope")
    )
    by_source = (
        queryset.values("source_type")
        .annotate(total_kg=Sum("estimated_co2e_kg"))
        .order_by("source_type")
    )
    suspicious_count = queryset.filter(suspicious_flag=True).count()

    return {
        "total_kg_co2e": round(total_kg, 2),
        "by_scope": list(by_scope),
        "by_source": list(by_source),
        "suspicious_count": suspicious_count,
        "record_count": queryset.count(),
    }
