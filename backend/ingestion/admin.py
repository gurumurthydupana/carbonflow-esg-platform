from django.contrib import admin
from .models import PlantLookup, AirportLookup


@admin.register(PlantLookup)
class PlantLookupAdmin(admin.ModelAdmin):
    list_display = (
        'plant_code',
        'plant_name',
        'country'
    )

    search_fields = ('plant_code', 'plant_name')


@admin.register(AirportLookup)
class AirportLookupAdmin(admin.ModelAdmin):
    list_display = (
        'airport_code',
        'city',
        'country'
    )

    search_fields = ('airport_code',)