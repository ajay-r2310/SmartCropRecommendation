"""Model loading and prediction utilities."""

from __future__ import annotations

import logging
from pathlib import Path
from typing import Any

import joblib
import pandas as pd

from config import Config
from utils.constants import CROP_METADATA

LOGGER = logging.getLogger(__name__)


class CropPredictor:
    """Loads the trained model and returns crop predictions."""

    def __init__(
        self,
        model_path: Path = Config.MODEL_PATH,
        encoder_path: Path = Config.LABEL_ENCODER_PATH,
    ) -> None:
        self.model_path = model_path
        self.encoder_path = encoder_path
        self.model: Any | None = None
        self.encoder: Any | None = None
        self._load()

    def _load(self) -> None:
        if self.model_path.exists() and self.encoder_path.exists():
            self.model = joblib.load(self.model_path)
            self.encoder = joblib.load(self.encoder_path)
            LOGGER.info("ML model loaded from %s", self.model_path)
        else:
            LOGGER.warning("Model files missing; using rules fallback prediction.")

    def predict(
        self,
        soil_type: str,
        season: str,
        temperature: float,
        humidity: float,
        rainfall: float,
    ) -> dict[str, float | str]:
        """Predict best crop and confidence."""

        if self.model is None or self.encoder is None:
            crop = self._fallback_crop(soil_type, season, rainfall)
            return {"crop": crop, "confidence": 72.0}

        features = pd.DataFrame(
            [
                {
                    "soil_type": soil_type,
                    "season": season,
                    "temperature": temperature,
                    "humidity": humidity,
                    "rainfall": rainfall,
                }
            ]
        )
        prediction = self.model.predict(features)[0]
        crop = str(self.encoder.inverse_transform([prediction])[0])
        confidence = 0.0
        if hasattr(self.model, "predict_proba"):
            confidence = round(float(max(self.model.predict_proba(features)[0]) * 100), 1)
        return {"crop": crop, "confidence": confidence}

    @staticmethod
    def _fallback_crop(soil_type: str, season: str, rainfall: float) -> str:
        if soil_type == "Black" and season in {"Kharif", "Monsoon"}:
            return "Cotton"
        if soil_type == "Alluvial" and rainfall > 10:
            return "Rice"
        if soil_type == "Red" and season in {"Rabi", "Winter"}:
            return "Groundnut"
        if soil_type == "Loamy" and season in {"Summer", "Zaid"}:
            return "Vegetables"
        if soil_type == "Clay":
            return "Sugarcane"
        return next(iter(CROP_METADATA))
