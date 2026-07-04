"""MongoDB Atlas access layer."""

from __future__ import annotations

import logging
from typing import Any

from pymongo import DESCENDING, MongoClient
from pymongo.collection import Collection
from pymongo.errors import PyMongoError

from config import Config

LOGGER = logging.getLogger(__name__)


class MongoDB:
    """Small repository wrapper for prediction documents."""

    def __init__(self) -> None:
        self.client: MongoClient | None = None
        self.collection: Collection | None = None

        if Config.MONGO_URI:
            try:
                self.client = MongoClient(
                    Config.MONGO_URI,
                    serverSelectionTimeoutMS=5000
                )

                # Test MongoDB Connection
                self.client.admin.command("ping")
                print("✅ Connected to MongoDB Atlas Successfully!")

                database = self.client[Config.MONGO_DB_NAME]
                self.collection = database[Config.MONGO_COLLECTION]

                # Create index
                self.collection.create_index(
                    [("prediction_time", DESCENDING)]
                )

            except Exception as e:
                print("❌ MongoDB Connection Error:", e)
                LOGGER.exception("MongoDB connection failed: %s", e)
                self.collection = None

        else:
            LOGGER.warning("MONGO_URI missing; database writes are disabled.")

    def insert_prediction(self, prediction: dict[str, Any]) -> str | None:
        """Insert prediction into MongoDB."""

        print("\n========== INSERT FUNCTION CALLED ==========")
        print("Prediction Data:")
        print(prediction)

        if self.collection is None:
            print("❌ Collection is None")
            return None

        try:
            result = self.collection.insert_one(prediction)

            print("✅ Insert Successful")
            print("Inserted ID:", result.inserted_id)

            LOGGER.info("Database Insert success: %s", result.inserted_id)

            return str(result.inserted_id)

        except PyMongoError as exc:
            print("❌ MongoDB Insert Error:", exc)
            LOGGER.exception("Database Insert failed: %s", exc)
            return None

    def get_predictions(
        self,
        crop: str = "",
        season: str = "",
    ) -> list[dict[str, Any]]:
        """Fetch prediction history."""

        if self.collection is None:
            return []

        query: dict[str, Any] = {}

        if crop:
            query["predicted_crop"] = crop

        if season:
            query["season"] = season

        try:
            return list(
                self.collection.find(query).sort(
                    "prediction_time",
                    DESCENDING
                )
            )

        except PyMongoError as exc:
            print("❌ Fetch Error:", exc)
            LOGGER.exception("History fetch failed: %s", exc)
            return []