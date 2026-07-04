"""Yield and profit estimation logic."""

from __future__ import annotations

from utils.constants import CROP_METADATA


class ProfitService:
    """Calculates practical agronomic estimates."""

    @staticmethod
    def estimate(crop: str, land_area: float, rainfall: float) -> dict[str, float | str]:
        """Estimate yield and profit from crop metadata and land area."""

        metadata = CROP_METADATA.get(crop, CROP_METADATA["Rice"])
        rainfall_factor = 1 + min(max((rainfall - 8) / 100, -0.12), 0.18)
        expected_yield = round(float(metadata["yield"]) * land_area * rainfall_factor, 2)
        estimated_profit = round(float(metadata["profit"]) * land_area * rainfall_factor, 2)

        return {
            "expected_yield": expected_yield,
            "estimated_profit": estimated_profit,
            "sowing_month": str(metadata["sowing_month"]),
        }

