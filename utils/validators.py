"""Input validation helpers."""

from __future__ import annotations

from utils.constants import SEASONS, SOIL_TYPES, TAMIL_NADU_DISTRICTS


def validate_prediction_payload(form_data: dict[str, str]) -> tuple[bool, list[str]]:
    """Validate recommendation form data."""

    errors: list[str] = []
    location = form_data.get("location", "").strip()
    soil_type = form_data.get("soil_type", "").strip()
    season = form_data.get("season", "").strip()
    land_area_raw = form_data.get("land_area", "").strip()

    if location not in TAMIL_NADU_DISTRICTS:
        errors.append("Choose a valid Tamil Nadu district.")
    if soil_type not in SOIL_TYPES:
        errors.append("Choose a valid soil type.")
    if season not in SEASONS:
        errors.append("Choose a valid season.")

    try:
        land_area = float(land_area_raw)
        if land_area <= 0 or land_area > 10000:
            errors.append("Land area must be between 0.01 and 10,000 acres.")
    except ValueError:
        errors.append("Land area must be a valid number.")

    return not errors, errors


def normalize_land_area(value: str) -> float:
    """Convert land area to a rounded float."""

    return round(float(value), 2)

