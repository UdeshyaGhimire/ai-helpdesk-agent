from fastapi.testclient import TestClient

from src.app.main import app


client = TestClient(app)


def test_chat():
    response = client.post(
        "/chat",
        json={"message": "My laptop cannot connect to Wi-Fi"},
    )

    assert response.status_code == 200

    data = response.json()

    assert data["category"] == "Network"
    assert data["priority"] == "Medium"
    assert data["needs_human"] is False