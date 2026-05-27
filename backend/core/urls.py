from django.urls import path

from .views import health_check, organizations_list

urlpatterns = [
    path('health/', health_check),
    path("organizations/", organizations_list),
]