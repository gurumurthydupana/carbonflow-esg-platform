from rest_framework import serializers


class ReviewActionSerializer(serializers.Serializer):
    performed_by = serializers.CharField(max_length=255)
    notes = serializers.CharField(required=False, allow_blank=True, default="")
