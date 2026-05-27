from datetime import date, timedelta

from django.core.management.base import BaseCommand
from django.db import transaction

from core.models import Organization
from emissions.models import AuditLog, DataUpload, EmissionRecord
from ingestion.models import AirportLookup, PlantLookup


class Command(BaseCommand):
    help = "Seed demo ESG data for local development and interview demos"

    def add_arguments(self, parser):
        parser.add_argument(
            "--reset",
            action="store_true",
            help="Delete existing records before seeding",
        )

    @transaction.atomic
    def handle(self, *args, **options):
        if options["reset"]:
            self.stdout.write(self.style.WARNING("Resetting existing demo data..."))
            AuditLog.objects.all().delete()
            EmissionRecord.objects.all().delete()
            DataUpload.objects.all().delete()
            PlantLookup.objects.all().delete()
            AirportLookup.objects.all().delete()
            Organization.objects.all().delete()

        org, _ = Organization.objects.get_or_create(
            slug="acme-manufacturing",
            defaults={"name": "Acme Manufacturing"},
        )

        PlantLookup.objects.get_or_create(
            organization=org,
            plant_code="PLT-1001",
            defaults={"plant_name": "Pune Assembly Plant", "country": "India"},
        )
        PlantLookup.objects.get_or_create(
            organization=org,
            plant_code="PLT-1002",
            defaults={"plant_name": "Chennai Packaging Plant", "country": "India"},
        )

        AirportLookup.objects.get_or_create(
            airport_code="DEL",
            defaults={"city": "Delhi", "country": "India"},
        )
        AirportLookup.objects.get_or_create(
            airport_code="BLR",
            defaults={"city": "Bengaluru", "country": "India"},
        )

        sap_upload, _ = DataUpload.objects.get_or_create(
            organization=org,
            source_type="sap",
            file_name="sap_may_2026.csv",
            defaults={"upload_status": "completed", "total_rows": 2, "failed_rows": []},
        )
        utility_upload, _ = DataUpload.objects.get_or_create(
            organization=org,
            source_type="utility",
            file_name="utility_may_2026.csv",
            defaults={"upload_status": "completed", "total_rows": 2, "failed_rows": []},
        )
        travel_upload, _ = DataUpload.objects.get_or_create(
            organization=org,
            source_type="travel",
            file_name="travel_may_2026.csv",
            defaults={"upload_status": "completed", "total_rows": 2, "failed_rows": []},
        )

        today = date.today()
        first_of_month = today.replace(day=1)
        last_month_end = first_of_month - timedelta(days=1)
        last_month_start = last_month_end.replace(day=1)

        records = [
            {
                "upload": sap_upload,
                "source_type": "sap",
                "activity_type": "diesel",
                "raw_quantity": 900,
                "raw_unit": "liter",
                "normalized_quantity": 900,
                "normalized_unit": "liter",
                "estimated_co2e_kg": 2412,
                "scope": "scope1",
                "suspicious_flag": False,
                "suspicious_reason": "",
                "review_status": "approved",
                "source_metadata": {
                    "cost_center": "PLT-1001",
                    "parser": "sap_parser_v1",
                    "raw_row": {"quantity": "900", "unit": "liter"},
                },
                "is_locked": True,
            },
            {
                "upload": utility_upload,
                "source_type": "utility",
                "activity_type": "electricity",
                "raw_quantity": 12000,
                "raw_unit": "kwh",
                "normalized_quantity": 12000,
                "normalized_unit": "kwh",
                "estimated_co2e_kg": 5700,
                "scope": "scope2",
                "suspicious_flag": False,
                "suspicious_reason": "",
                "review_status": "pending",
                "source_metadata": {
                    "meter_id": "MTR-7781",
                    "parser": "utility_parser_v1",
                    "raw_row": {"consumption": "12000", "unit": "kwh"},
                },
                "is_locked": False,
            },
            {
                "upload": travel_upload,
                "source_type": "travel",
                "activity_type": "air_travel",
                "raw_quantity": 18500,
                "raw_unit": "km",
                "normalized_quantity": 18500,
                "normalized_unit": "km",
                "estimated_co2e_kg": 2775,
                "scope": "scope3",
                "suspicious_flag": True,
                "suspicious_reason": "Unusually high monthly air travel distance",
                "review_status": "pending",
                "source_metadata": {
                    "from_airport": "DEL",
                    "to_airport": "BLR",
                    "parser": "travel_parser_v1",
                    "raw_row": {"distance": "18500", "unit": "km"},
                },
                "is_locked": False,
            },
        ]

        seeded_records = []
        for item in records:
            record, _ = EmissionRecord.objects.get_or_create(
                organization=org,
                upload=item["upload"],
                activity_type=item["activity_type"],
                period_start=last_month_start,
                period_end=last_month_end,
                defaults=item,
            )
            seeded_records.append(record)

        for record in seeded_records:
            if record.review_status == "approved":
                AuditLog.objects.get_or_create(
                    emission_record=record,
                    action="approved",
                    performed_by="demo.analyst@carbonflow.local",
                    defaults={"notes": "Approved in demo baseline seed"},
                )
            if record.is_locked:
                AuditLog.objects.get_or_create(
                    emission_record=record,
                    action="locked",
                    performed_by="demo.manager@carbonflow.local",
                    defaults={"notes": "Locked as part of demo close"},
                )

        self.stdout.write(
            self.style.SUCCESS(
                "Demo data ready: 1 organization, lookups, uploads, records, and audit logs seeded."
            )
        )
