from django.urls import path

from .views import list_uploads, upload_csv

urlpatterns = [
    path("uploads/", list_uploads),
    path("uploads/csv/", upload_csv),
]
