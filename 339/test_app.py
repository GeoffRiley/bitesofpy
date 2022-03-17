import pytest
from fastapi.testclient import TestClient

from app import app

EXPECTED_FOOD1 = {
    "id": 1,
    "name": "egg",
    "serving_size": "piece",
    "kcal_per_serving": 78,
    "protein_grams": 6.2,
    "fibre_grams": 0,
}
EXPECTED_FOOD2 = {
    "id": 2,
    "name": "oatmeal",
    "serving_size": "100 grams",
    "kcal_per_serving": 336,
    "protein_grams": 13.2,
    "fibre_grams": 10.1,
}


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


def test_get_all_foods(client):
    resp = client.get("/")
    assert resp.status_code == 200
    expected = [EXPECTED_FOOD1, EXPECTED_FOOD2]
    assert resp.json() == expected


def test_get_first_food(client):
    resp = client.get("/1")
    assert resp.status_code == 200
    assert resp.json() == EXPECTED_FOOD1


def test_get_second_food(client):
    resp = client.get("/2")
    assert resp.status_code == 200
    assert resp.json() == EXPECTED_FOOD2


def test_get_single_non_existing_food(client):
    # oops! We'll add exception handling in a later Bite
    with pytest.raises(KeyError):
        client.get("/3")