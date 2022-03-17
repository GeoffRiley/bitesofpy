import difflib

import pytest
from fastapi import HTTPException
from fastapi.testclient import TestClient

from app import app


@pytest.fixture
def client():
    client = TestClient(app)
    return client


@pytest.fixture(autouse=True)
def create_foods(client):
    """
    Payload for two food objects, "autouse" runs this
    automatically before the tests.
    """
    food1_payload = dict(
        id=1,
        name="egg",
        serving_size="piece",
        kcal_per_serving=78,
        protein_grams=6.2,
        fibre_grams=0,
    )
    food2_payload = dict(
        id=2,
        name="oatmeal",
        serving_size="100 grams",
        kcal_per_serving=336,
        protein_grams=13.2,
        fibre_grams=10.1,
    )
    for payload in (food1_payload, food2_payload):
        client.post("/", json=payload)


def test_update_food(client):
    orig_egg = client.get("/1").json()
    resp = client.get("/2")
    orig_food = resp.json()
    food = orig_food.copy()
    food["kcal_per_serving"] = 350
    client.put("/2", json=food)
    resp = client.get("/2")
    updated_food = resp.json()
    diff = set(updated_food.values()) - set(orig_food.values())
    assert diff == {350}
    # the other item is not updated
    egg = client.get("/1").json()
    assert orig_egg == egg


def test_update_nonexisting_food_returns_404(client):
    resp = client.get("/2")
    payload = resp.json()
    resp = client.put("/3", json=payload)
    assert resp.status_code == 404
    assert resp.json() == {"detail": "Food not found"}


def test_delete_food(client):
    resp = client.get("/")
    assert len(resp.json()) == 2
    resp = client.delete("/2")
    assert resp.json() == {"ok": True}
    # oatmeal deleted
    with pytest.raises(KeyError):
        client.get("/2")
    resp = client.get("/")
    data = resp.json()
    assert len(data) == 1
    # only egg remains
    assert data[0]["id"] == 1
    assert data[0]["name"] == "egg"


def test_delete_nonexisting_food_returns_404(client):
    resp = client.delete("/3")
    assert resp.status_code == 404
    assert resp.json() == {"detail": "Food not found"}