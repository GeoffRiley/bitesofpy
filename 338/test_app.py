import pytest
from fastapi.testclient import TestClient

from app import Food, app, foods


@pytest.fixture
def client():
    client = TestClient(app)
    return client


@pytest.fixture
def food():
    food = Food(
        id=1,
        name="egg",
        serving_size="piece",
        kcal_per_serving=78,
        protein_grams=6.3,
        fibre_grams=1,
    )
    return food


@pytest.fixture
def food_payload():
    return dict(
        id=1,
        name="egg",
        serving_size="piece",
        kcal_per_serving=78,
        protein_grams=6.3,
        fibre_grams=1,
    )


@pytest.fixture
def second_food_payload():
    return dict(
        id=2,
        name="oatmeal",
        serving_size="100 grams",
        kcal_per_serving=336,
        protein_grams=13.2,
        fibre_grams=10.1,
    )


def test_can_only_post(client):
    resp = client.get("/")
    assert resp.status_code == 405


def test_create_food(client, food_payload, food):
    resp = client.post("/", json=food_payload)
    assert resp.status_code == 201
    assert resp.json() == food
    assert foods == {1: food}


def test_create_two_foods(client, food_payload, second_food_payload):
    for pl in (food_payload, second_food_payload):
        resp = client.post("/", json=pl)
        assert resp.status_code == 201
    assert len(foods) == 2
    names = [food.name for food in foods.values()]
    assert names == ["egg", "oatmeal"]
    total_calories = sum(food.kcal_per_serving for food in foods.values())
    assert total_calories == 414


def test_create_food_default_fibre(client, food_payload):
    del food_payload["fibre_grams"]
    resp = client.post("/", json=food_payload)
    assert resp.status_code == 201
    assert foods[1].fibre_grams == 0


def test_create_food_wrong_food_payload(client, food_payload):
    del food_payload["kcal_per_serving"]
    resp = client.post("/", json=food_payload)
    assert resp.status_code == 422
    error = {
        "detail": [
            {
                "loc": ["body", "kcal_per_serving"],
                "msg": "field required",
                "type": "value_error.missing",
            }
        ]
    }
    assert resp.json() == error