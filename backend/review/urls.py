from django.urls import path

from .views import approve_record, lock_record, reject_record, review_queue

urlpatterns = [
    path("queue/", review_queue),
    path("records/<uuid:record_id>/approve/", approve_record),
    path("records/<uuid:record_id>/reject/", reject_record),
    path("records/<uuid:record_id>/lock/", lock_record),
]
