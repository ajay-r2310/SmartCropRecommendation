"""OpenWeatherMap weather integration."""

from __future__ import annotations

import logging
from typing import Any

import requests

from config import Config

LOGGER = logging.getLogger(__name__)


class WeatherService:
    """Fetches live weather values with a deterministic local fallback."""

    API_URL = "https://api.openweathermap.org/data/2.5/weather"

    @staticmethod
    def get_weather(location: str) -> dict[str, float | str]:
        """Return temperature, humidity and rainfall for a location."""

        if not Config.OPENWEATHER_API_KEY:
            LOGGER.warning("Weather API key missing; using regional fallback values.")
            return WeatherService._fallback_weather(location)

        params = {
            "q": f"{location},IN",
            "appid": Config.OPENWEATHER_API_KEY,
            "units": "metric",
        }
        try:
            response = requests.get(WeatherService.API_URL, params=params, timeout=8)
            response.raise_for_status()
            payload: dict[str, Any] = response.json()
            rainfall = payload.get("rain", {}).get("1h") or payload.get("rain", {}).get("3h") or 0
            weather = {
                "temperature": round(float(payload["main"]["temp"]), 1),
                "humidity": round(float(payload["main"]["humidity"]), 1),
                "rainfall": round(float(rainfall), 1),
                "source": "OpenWeatherMap",
            }
            LOGGER.info("Weather API success for %s: %s", location, weather)
            return weather
        except requests.RequestException as exc:
            LOGGER.exception("Weather API request failed for %s: %s", location, exc)
            return WeatherService._fallback_weather(location)

    @staticmethod
    def _fallback_weather(location: str) -> dict[str, float | str]:
        """Use stable Tamil Nadu-like fallback values for local demos."""

        seed = sum(ord(char) for char in location)
        return {
            "temperature": round(25 + seed % 9 + ((seed % 4) * 0.3), 1),
            "humidity": round(58 + seed % 30, 1),
            "rainfall": round(2 + seed % 18, 1),
            "source": "Regional fallback",
        }

