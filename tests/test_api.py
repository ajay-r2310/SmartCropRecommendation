from app import create_app


def test_home_page_loads():
    app = create_app()
    app.config.update(TESTING=True)
    client = app.test_client()
    response = client.get("/")
    assert response.status_code == 200
    assert b"Farm Input Details" in response.data
    assert b'data-lang="ta"' in response.data
    assert b'data-translate-value="district"' in response.data
    assert b'data-translate-value="soil"' in response.data
    assert b'data-translate-value="season"' in response.data


def test_invalid_recommendation_redirects():
    app = create_app()
    app.config.update(TESTING=True)
    client = app.test_client()
    response = client.post("/recommend", data={}, follow_redirects=False)
    assert response.status_code == 302


def test_valid_recommendation_renders_result():
    app = create_app()
    app.config.update(TESTING=True)
    client = app.test_client()
    response = client.post(
        "/recommend",
        data={
            "location": "Thanjavur",
            "soil_type": "Alluvial",
            "season": "Monsoon",
            "land_area": "2.5",
        },
    )
    assert response.status_code == 200
    assert b"Recommendation Generated" in response.data
