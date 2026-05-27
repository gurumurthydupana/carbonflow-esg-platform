from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from core.models import Organization
from emissions.models import DataUpload
from .serializers import UploadCreateSerializer, UploadListSerializer
from .services import process_upload


@api_view(["POST"])
def upload_csv(request):
    serializer = UploadCreateSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    organization = Organization.objects.filter(
        id=serializer.validated_data["organization_id"]
    ).first()
    if not organization:
        return Response(
            {"detail": "Organization not found"},
            status=status.HTTP_404_NOT_FOUND,
        )

    upload_file = serializer.validated_data["file"]
    upload = DataUpload.objects.create(
        organization=organization,
        source_type=serializer.validated_data["source_type"],
        file_name=upload_file.name,
    )
    upload, created_count = process_upload(upload, upload_file)

    return Response(
        {
            "upload": UploadListSerializer(upload).data,
            "created_records": created_count,
        },
        status=status.HTTP_201_CREATED,
    )


@api_view(["GET"])
def list_uploads(request):
    queryset = DataUpload.objects.select_related("organization").order_by("-uploaded_at")
    organization_id = request.query_params.get("organization_id")
    if organization_id:
        queryset = queryset.filter(organization_id=organization_id)
    return Response(UploadListSerializer(queryset, many=True).data)
