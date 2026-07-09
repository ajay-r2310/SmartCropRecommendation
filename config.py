"""Application configuration loaded from environment variables."""

from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")


class Config:
    """Central Flask configuration."""

    SECRET_KEY: str = os.getenv("SECRET_KEY", "change-this-secret-key")
    OPENWEATHER_API_KEY: str = os.getenv("OPENWEATHER_API_KEY", "")
    MONGO_URI: str = os.getenv("MONGO_URI", "")
    MONGO_DB_NAME: str = os.getenv("MONGO_DB_NAME", "smart_crop_db")
    MONGO_COLLECTION: str = os.getenv("MONGO_COLLECTION", "predictions")
    DEBUG: bool = os.getenv("FLASK_DEBUG", "False").lower() == "true"
    TESTING: bool = False
    MODEL_PATH: Path = BASE_DIR / "models" / "model.pkl"
    LABEL_ENCODER_PATH: Path = BASE_DIR / "models" / "label_encoder.pkl"
    PROCESSED_DATA_PATH: Path = BASE_DIR / "data" / "processed" / "crop_training_data.csv"
    LOG_FILE: Path = BASE_DIR / "logs" / "app.log"
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")

