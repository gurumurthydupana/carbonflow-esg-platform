from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Organization


@api_view(['GET'])
def health_check(request):
    return Response({
        "status": "success",
        "message": "CarbonFlow backend is running"
    })


@api_view(["GET"])
def organizations_list(request):
    organizations = Organization.objects.all().order_by("name")
    return Response(
        [
            {
                "id": str(org.id),
                "name": org.name,
                "slug": org.slug,
            }
            for org in organizations
        ]
    )