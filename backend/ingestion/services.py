import csv
import io
from datetime import date, datetime

from django.db import transaction

from emissions.models import DataUpload, EmissionRecord
from ingestion.models import AirportLookup, PlantLookup


EMISSION_FACTORS = {
    "electricity_kwh": 0.475,
    "diesel_liter": 2.68,
    "natural_gas_m3": 1.9,
    "air_travel_km": 0.15,
}


def _as_float(value, default=0.0):
    try:
        return float(value)
    except (TypeError, ValueError):
        return default


def _parse_date(raw_value):
    if not raw_value:
        return date.today()
    for fmt in ("%Y-%m-%d", "%d-%m-%Y", "%m/%d/%Y"):
        try:
            return datetime.strptime(str(raw_value).strip(), fmt).date()
        except ValueError:
            continue
    return date.today()


def _normalize_quantity(activity_type, raw_quantity, raw_unit):
    unit = (raw_unit or "").strip().lower()
    qty = float(raw_quantity)
    if activity_type == "electricity" and unit in {"mwh"}:
        return qty * 1000, "kwh"
    if activity_type == "diesel" and unit in {"gallon", "gallons"}:
        return qty * 3.785, "liter"
    if activity_type == "air_travel" and unit in {"miles", "mi"}:
        return qty * 1.60934, "km"
    return qty, unit or "unit"


def _calculate_co2e(activity_type, normalized_quantity, normalized_unit):
    key = f"{activity_type}_{normalized_unit}"
    factor = EMISSION_FACTORS.get(key, 0.0)
    return normalized_quantity * factor


def _detect_suspicious(normalized_quantity, estimated_co2e_kg):
    if normalized_quantity <= 0:
        return True, "Quantity is zero or negative"
    if estimated_co2e_kg > 100000:
        return True, "Unusually high estimated emissions"
    return False, ""


def _resolve_scope(activity_type):
    if activity_type in {"electricity"}:
        return "scope2"
    return "scope3" if activity_type == "air_travel" else "scope1"


def _parse_row_by_source(source_type, row):
    if source_type == "sap":
        return {
            "activity_type": (row.get("activity_type") or "diesel").strip().lower(),
            "raw_quantity": _as_float(row.get("quantity")),
            "raw_unit": (row.get("unit") or "liter").strip(),
            "period_start": _parse_date(row.get("period_start")),
            "period_end": _parse_date(row.get("period_end")),
            "metadata": {"cost_center": row.get("cost_center", "")},
        }
    if source_type == "utility":
        return {
            "activity_type": "electricity",
            "raw_quantity": _as_float(row.get("consumption")),
            "raw_unit": (row.get("unit") or "kwh").strip(),
            "period_start": _parse_date(row.get("bill_start")),
            "period_end": _parse_date(row.get("bill_end")),
            "metadata": {"meter_id": row.get("meter_id", "")},
        }
    if source_type == "travel":
        return {
            "activity_type": "air_travel",
            "raw_quantity": _as_float(row.get("distance")),
            "raw_unit": (row.get("unit") or "km").strip(),
            "period_start": _parse_date(row.get("travel_date")),
            "period_end": _parse_date(row.get("travel_date")),
            "metadata": {
                "from_airport": row.get("from_airport", ""),
                "to_airport": row.get("to_airport", ""),
            },
        }
    raise ValueError("Unsupported source type")


def _validate_row(parsed_row):
    errors = []
    if parsed_row["raw_quantity"] <= 0:
        errors.append("Quantity must be greater than zero")
    if parsed_row["period_end"] < parsed_row["period_start"]:
        errors.append("Period end cannot be before period start")
    return errors


def _attach_provenance(organization, source_type, source_metadata):
    provenance = dict(source_metadata)
    if source_type == "sap":
        plant_code = provenance.get("cost_center")
        if plant_code:
            plant = (
                PlantLookup.objects.filter(
                    organization=organization, plant_code=plant_code
                ).first()
            )
            if plant:
                provenance["plant_name"] = plant.plant_name
                provenance["plant_country"] = plant.country
    if source_type == "travel":
        from_airport = provenance.get("from_airport")
        if from_airport:
            airport = AirportLookup.objects.filter(airport_code=from_airport).first()
            if airport:
                provenance["from_city"] = airport.city
                provenance["from_country"] = airport.country
    return provenance


@transaction.atomic
def process_upload(upload, upload_file):
    decoded = upload_file.read().decode("utf-8-sig")
    reader = csv.DictReader(io.StringIO(decoded))
    failed_rows = []
    created_count = 0
    rows = list(reader)

    for idx, row in enumerate(rows, start=1):
        try:
            parsed = _parse_row_by_source(upload.source_type, row)
            errors = _validate_row(parsed)
            if errors:
                failed_rows.append({"row": idx, "errors": errors, "data": row})
                continue

            normalized_quantity, normalized_unit = _normalize_quantity(
                parsed["activity_type"], parsed["raw_quantity"], parsed["raw_unit"]
            )
            estimated_co2e_kg = _calculate_co2e(
                parsed["activity_type"], normalized_quantity, normalized_unit
            )
            suspicious_flag, suspicious_reason = _detect_suspicious(
                normalized_quantity, estimated_co2e_kg
            )

            source_metadata = _attach_provenance(
                upload.organization,
                upload.source_type,
                {
                    **parsed["metadata"],
                    "raw_row": row,
                    "parser": f"{upload.source_type}_parser_v1",
                },
            )

            EmissionRecord.objects.create(
                organization=upload.organization,
                upload=upload,
                source_type=upload.source_type,
                activity_type=parsed["activity_type"],
                raw_quantity=parsed["raw_quantity"],
                raw_unit=parsed["raw_unit"],
                normalized_quantity=normalized_quantity,
                normalized_unit=normalized_unit,
                estimated_co2e_kg=estimated_co2e_kg,
                scope=_resolve_scope(parsed["activity_type"]),
                period_start=parsed["period_start"],
                period_end=parsed["period_end"],
                suspicious_flag=suspicious_flag,
                suspicious_reason=suspicious_reason,
                source_metadata=source_metadata,
            )
            created_count += 1
        except Exception as exc:
            failed_rows.append({"row": idx, "errors": [str(exc)], "data": row})

    upload.total_rows = len(rows)
    upload.failed_rows = failed_rows
    upload.upload_status = "completed" if created_count > 0 else "failed"
    upload.save(update_fields=["total_rows", "failed_rows", "upload_status"])
    return upload, created_count
