from pathlib import Path

from models.predict import CropPredictor
from services.profit_service import ProfitService


def test_fallback_prediction_returns_crop():
    predictor = CropPredictor(
        model_path=Path("missing.pkl"),
        encoder_path=Path("missing_encoder.pkl"),
    )
    result = predictor.predict("Black", "Kharif", 31, 65, 8)
    assert result["crop"] == "Cotton"
    assert result["confidence"] > 0


def test_profit_estimate_scales_with_land_area():
    one_acre = ProfitService.estimate("Rice", 1, 10)
    two_acres = ProfitService.estimate("Rice", 2, 10)
    assert two_acres["estimated_profit"] == one_acre["estimated_profit"] * 2
