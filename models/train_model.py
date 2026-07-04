"""Train the crop recommendation model."""

from __future__ import annotations

import sys
from pathlib import Path

import joblib
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import LabelEncoder, OneHotEncoder

sys.path.append(str(Path(__file__).resolve().parents[1]))

from config import Config
from utils.constants import CROP_METADATA, SEASONS, SOIL_TYPES


def build_training_data(path: Path = Config.PROCESSED_DATA_PATH) -> pd.DataFrame:
    """Load or create a compact agronomic training dataset."""

    if path.exists():
        return pd.read_csv(path)

    rows: list[dict[str, object]] = []
    crop_rules = [
        ("Rice", "Alluvial", "Monsoon", 29, 82, 18),
        ("Rice", "Clay", "Kharif", 28, 80, 16),
        ("Millets", "Red", "Summer", 32, 56, 5),
        ("Millets", "Sandy", "Zaid", 34, 50, 3),
        ("Maize", "Loamy", "Kharif", 30, 65, 9),
        ("Maize", "Alluvial", "Rabi", 26, 62, 7),
        ("Sugarcane", "Clay", "Winter", 27, 76, 12),
        ("Sugarcane", "Black", "Summer", 31, 72, 10),
        ("Groundnut", "Red", "Rabi", 27, 58, 6),
        ("Groundnut", "Sandy", "Kharif", 30, 60, 8),
        ("Cotton", "Black", "Kharif", 31, 64, 7),
        ("Cotton", "Black", "Monsoon", 29, 70, 9),
        ("Banana", "Loamy", "Summer", 30, 78, 12),
        ("Banana", "Alluvial", "Zaid", 31, 74, 11),
        ("Turmeric", "Red", "Monsoon", 28, 79, 14),
        ("Turmeric", "Laterite", "Kharif", 27, 76, 13),
        ("Pulses", "Laterite", "Rabi", 25, 55, 4),
        ("Pulses", "Red", "Winter", 24, 57, 5),
        ("Vegetables", "Loamy", "Winter", 23, 68, 6),
        ("Vegetables", "Alluvial", "Summer", 29, 70, 8),
    ]
    for crop, soil, season, temp, humidity, rainfall in crop_rules:
        for delta in range(-3, 4):
            rows.append(
                {
                    "soil_type": soil,
                    "season": season,
                    "temperature": temp + delta * 0.7,
                    "humidity": humidity + delta,
                    "rainfall": max(0, rainfall + delta * 0.8),
                    "crop": crop,
                }
            )

    for soil in SOIL_TYPES:
        for season in SEASONS:
            fallback_crop = "Rice" if season == "Monsoon" else "Maize"
            if soil == "Black":
                fallback_crop = "Cotton"
            if soil == "Loamy":
                fallback_crop = "Vegetables"
            rows.append(
                {
                    "soil_type": soil,
                    "season": season,
                    "temperature": 28,
                    "humidity": 65,
                    "rainfall": 8,
                    "crop": fallback_crop if fallback_crop in CROP_METADATA else "Rice",
                }
            )

    path.parent.mkdir(parents=True, exist_ok=True)
    dataframe = pd.DataFrame(rows)
    dataframe.to_csv(path, index=False)
    return dataframe


def train() -> None:
    """Train and save the Random Forest crop classifier."""

    dataframe = build_training_data()
    dataframe = dataframe.dropna().drop_duplicates()
    features = dataframe[["soil_type", "season", "temperature", "humidity", "rainfall"]]
    labels = dataframe["crop"]

    encoder = LabelEncoder()
    encoded_labels = encoder.fit_transform(labels)

    transformer = ColumnTransformer(
        transformers=[
            ("categorical", OneHotEncoder(handle_unknown="ignore"), ["soil_type", "season"]),
            ("numeric", "passthrough", ["temperature", "humidity", "rainfall"]),
        ]
    )
    model = Pipeline(
        steps=[
            ("preprocess", transformer),
            (
                "classifier",
                RandomForestClassifier(
                    n_estimators=180,
                    max_depth=12,
                    random_state=42,
                    class_weight="balanced",
                ),
            ),
        ]
    )

    x_train, x_test, y_train, y_test = train_test_split(
        features, encoded_labels, test_size=0.22, random_state=42, stratify=encoded_labels
    )
    model.fit(x_train, y_train)
    predictions = model.predict(x_test)
    print(f"Accuracy: {accuracy_score(y_test, predictions):.2%}")
    print(classification_report(y_test, predictions, target_names=encoder.classes_))

    Config.MODEL_PATH.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(model, Config.MODEL_PATH)
    joblib.dump(encoder, Config.LABEL_ENCODER_PATH)
    print(f"Saved model to {Config.MODEL_PATH}")


if __name__ == "__main__":
    train()
