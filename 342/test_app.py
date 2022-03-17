import pytest
from fastapi.testclient import TestClient

from app import FoodEntry, app, pwd_context

LAME_PASSWORD = "1234"  # noqa S105


# also from https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/
def _verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


@pytest.fixture
def client():
    client = TestClient(app)
    return client


@pytest.fixture
def user1():
    user = dict(id=1, username="user1", password=LAME_PASSWORD)
    return user


@pytest.fixture
def user2():
    user = dict(id=2, username="user2", password=LAME_PASSWORD)
    return user


@pytest.fixture
def food1():
    food = dict(
        id=1,
        name="egg",
        serving_size="piece",
        kcal_per_serving=78,
        protein_grams=6.2,
        fibre_grams=0,
    )
    return food


@pytest.fixture
def food2():
    food = dict(
        id=2,
        name="oatmeal",
        serving_size="100 grams",
        kcal_per_serving=336,
        protein_grams=13.2,
        fibre_grams=10.1,
    )
    return food


@pytest.fixture(autouse=True)
def create_food_entries(client, user1, user2, food1, food2):
    payload = dict(id=1, user=user1, food=food1, number_servings=1.5)
    client.post("/", json=payload)
    payload = dict(id=2, user=user2, food=food2, number_servings=2.2)
    client.post("/", json=payload)


def test_get_foods_user1(client):
    resp = client.get("/1")
    data = resp.json()
    assert len(data) == 1
    entry = data[0]
    assert entry["id"] == 1
    assert entry["user"]["username"] == "user1"
    assert entry["food"]["name"] == "egg"
    assert entry["number_servings"] == 1.5
    assert FoodEntry(**entry).total_calories == 117.0


def test_get_foods_user2(client, user2):
    new_food = dict(
        id=3,
        name="almendras",
        serving_size="20 grams",
        kcal_per_serving=104,
        protein_grams=2.3,
        fibre_grams=1.1,
    )
    payload = dict(id=3, user=user2, food=new_food, number_servings=2)
    client.post("/", json=payload)
    resp = client.get("/2")
    data = resp.json()
    assert len(data) == 2
    assert data[0]["food"]["name"] == "oatmeal"
    assert data[1]["food"]["name"] == "almendras"
    assert data[0]["user"]["id"] == 2
    assert data[1]["user"]["id"] == 2
    assert data[0]["number_servings"] == 2.2
    assert data[1]["number_servings"] == 2.0
    # need to create Pydantic model to test property
    assert FoodEntry(**data[0]).total_calories == 739.2
    assert FoodEntry(**data[1]).total_calories == 208.0
    # clean up for next tests (price of having global dict)
    client.delete("/3")


def test_update_food_entry(client):
    entry = client.get("/1").json()[0]
    assert entry["number_servings"] == 1.5
    new_entry = entry.copy()
    new_entry["number_servings"] = 3
    client.put(f"/{entry['id']}", json=new_entry)
    entry = client.get("/1").json()[0]
    assert entry["number_servings"] == 3.0


def test_update_nonexisting_food_entry_returns_404(client):
    entry = client.get("/2").json()[0]
    resp = client.put("/3", json=entry)
    assert resp.status_code == 404
    assert resp.json() == {"detail": "Food entry not found"}


def test_delete_food_entry(client):
    resp = client.delete("/2")
    assert resp.json() == {"ok": True}
    # user1's item still there
    assert len(client.get("/1").json()) == 1
    # user2's item deleted
    assert len(client.get("/2").json()) == 0


def test_delete_nonexisting_food_entry_returns_404(client):
    resp = client.delete("/3")
    assert resp.status_code == 404
    assert resp.json() == {"detail": "Food entry not found"}