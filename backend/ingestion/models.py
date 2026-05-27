from django.db import models
from core.models import Organization


class PlantLookup(models.Model):
    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE
    )

    plant_code = models.CharField(max_length=50)

    plant_name = models.CharField(max_length=255)

    country = models.CharField(max_length=100)

    def __str__(self):
        return self.plant_name


class AirportLookup(models.Model):
    airport_code = models.CharField(max_length=10, unique=True)

    city = models.CharField(max_length=100)

    country = models.CharField(max_length=100)

    def __str__(self):
        return self.airport_code