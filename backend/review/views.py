from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from emissions.models import EmissionRecord
from emissions.serializers import EmissionRecordSerializer
from .serializers import ReviewActionSerializer
from .services import add_audit_log


@api_view(["GET"])
def review_queue(request):
    queryset = EmissionRecord.objects.filter(
        suspicious_flag=True, review_status="pending"
    ).select_related("organization", "upload")
    organization_id = request.query_params.get("organization_id")
    if organization_id:
        queryset = queryset.filter(organization_id=organization_id)
    return Response(EmissionRecordSerializer(queryset.order_by("-created_at"), many=True).data)


def _update_review_status(record, new_status, action, serializer):
    if record.is_locked:
        return Response(
            {"detail": "Record is locked and cannot be modified"},
            status=status.HTTP_400_BAD_REQUEST,
        )
    record.review_status = new_status
    record.save(update_fields=["review_status"])
    add_audit_log(
        record=record,
        action=action,
        performed_by=serializer.validated_data["performed_by"],
        notes=serializer.validated_data.get("notes", ""),
    )
    return Response(EmissionRecordSerializer(record).data)


@api_view(["POST"])
def approve_record(request, record_id):
    serializer = ReviewActionSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    record = EmissionRecord.objects.filter(id=record_id).first()
    if not record:
        return Response({"detail": "Record not found"}, status=status.HTTP_404_NOT_FOUND)
    return _update_review_status(record, "approved", "approved", serializer)


@api_view(["POST"])
def reject_record(request, record_id):
    serializer = ReviewActionSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    record = EmissionRecord.objects.filter(id=record_id).first()
    if not record:
        return Response({"detail": "Record not found"}, status=status.HTTP_404_NOT_FOUND)
    return _update_review_status(record, "rejected", "rejected", serializer)


@api_view(["POST"])
def lock_record(request, record_id):
    serializer = ReviewActionSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    record = EmissionRecord.objects.filter(id=record_id).first()
    if not record:
        return Response({"detail": "Record not found"}, status=status.HTTP_404_NOT_FOUND)
    record.is_locked = True
    record.save(update_fields=["is_locked"])
    add_audit_log(
        record=record,
        action="locked",
        performed_by=serializer.validated_data["performed_by"],
        notes=serializer.validated_data.get("notes", ""),
    )
    return Response(EmissionRecordSerializer(record).data)
