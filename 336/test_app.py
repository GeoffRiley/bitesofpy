import pytest
from fastapi.testclient import TestClient

from app import app


@pytest.fixture
def client():
    client = TestClient(app)
    return client


def test_root_endpoint_with_get(client):
    resp = client.get("/")
    assert resp.status_code == 200
    msg = "Welcome to PyBites' FastAPI Learning Path 🐍 🎉"
    expected = {"message": msg}
    assert resp.json() == expected


def test_root_endpoint_only_get(client):
    resp = client.post("/")
    assert resp.status_code == 405
    assert resp.json() == {"detail": "Method Not Allowed"}