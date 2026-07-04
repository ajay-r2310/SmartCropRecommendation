"""High-level crop recommendation orchestration."""

from __future__ import annotations

import logging
from datetime import datetime, timezone

from models.predict import CropPredictor
from services.profit_service import ProfitService
from services.weather_service import WeatherService

LOGGER = logging.getLogger(__name__)


class PredictionService:
    """Builds complete crop recommendations."""

    def __init__(self) -> None:
        self.predictor = CropPredictor()

    def recommend(
        self,
        location: str,
        soil_type: str,
        season: str,
        land_area: float,
    ) -> dict[str, object]:
        weather = WeatherService.get_weather(location)
        model_result = self.predictor.predict(
            soil_type=soil_type,
            season=season,
            temperature=float(weather["temperature"]),
            humidity=float(weather["humidity"]),
            rainfall=float(weather["rainfall"]),
        )
        estimates = ProfitService.estimate(
            crop=str(model_result["crop"]),
            land_area=land_area,
            rainfall=float(weather["rainfall"]),
        )
        result = {
            "location": location,
            "soil_type": soil_type,
            "season": season,
            "land_area": land_area,
            "temperature": weather["temperature"],
            "humidity": weather["humidity"],
            "rainfall": weather["rainfall"],
            "weather_source": weather["source"],
            "predicted_crop": model_result["crop"],
            "expected_yield": estimates["expected_yield"],
            "estimated_profit": estimates["estimated_profit"],
            "sowing_month": estimates["sowing_month"],
            "confidence": model_result["confidence"],
            "prediction_time": datetime.now(timezone.utc),
        }
        LOGGER.info("Prediction generated for %s: %s", location, result)
        return result
