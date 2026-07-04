from database.mongodb import MongoDB


def test_database_without_uri_is_safe(monkeypatch):
    monkeypatch.setattr("config.Config.MONGO_URI", "")
    database = MongoDB()
    assert database.insert_prediction({"predicted_crop": "Rice"}) is None
    assert database.get_predictions() == []

