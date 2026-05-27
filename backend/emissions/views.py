from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import AuditLog, EmissionRecord
from .serializers import AuditLogSerializer, EmissionRecordSerializer
from .services import get_emissions_summary


@api_view(["GET"])
def list_emission_records(request):
    queryset = EmissionRecord.objects.select_related("organization", "upload").order_by(
        "-created_at"
    )
    organization_id = request.query_params.get("organization_id")
    if organization_id:
        queryset = queryset.filter(organization_id=organization_id)

    if request.query_params.get("suspicious") == "true":
        queryset = queryset.filter(suspicious_flag=True)
    review_status = request.query_params.get("review_status")
    if review_status:
        queryset = queryset.filter(review_status=review_status)

    return Response(EmissionRecordSerializer(queryset, many=True).data)


@api_view(["GET"])
def emissions_summary(request):
    organization_id = request.query_params.get("organization_id")
    return Response(get_emissions_summary(organization_id))


@api_view(["GET"])
def list_audit_logs(request):
    queryset = AuditLog.objects.select_related("emission_record").order_by("-performed_at")
    organization_id = request.query_params.get("organization_id")
    if organization_id:
        queryset = queryset.filter(emission_record__organization_id=organization_id)
    return Response(AuditLogSerializer(queryset, many=True).data)
