"""General helper functions."""

from __future__ import annotations

from datetime import datetime


def format_currency(value: float) -> str:
    """Format a number as Indian rupees."""

    return f"Rs. {value:,.0f}"


def format_datetime(value: datetime | str | None) -> str:
    """Format stored prediction date values for display."""

    if isinstance(value, datetime):
        return value.strftime("%d %b %Y, %I:%M %p")
    if isinstance(value, str):
        return value
    return "-"

