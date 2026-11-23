import pytest

from app import app as flask_app


@pytest.fixture
def client():
    flask_app.config["TESTING"] = True
    with flask_app.test_client() as client:
        yield client


def test_health_returns_ok(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.get_json() == {"status": "ok"}


def test_index_returns_message(client):
    response = client.get("/")
    data = response.get_json()
    assert response.status_code == 200
    assert data["message"] == "Hello from the Linux Platform Homelab"


def test_index_includes_version_and_hostname(client):
    data = client.get("/").get_json()
    assert "version" in data
    assert "hostname" in data
