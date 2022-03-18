import pytest
from fastapi.testclient import TestClient

from app import FoodEntry, app

LAME_PASSWORD = "1234"  # noqa S105


@pytest.fixture(scope="session")
def client():
    client = TestClient(app)
    return client


@pytest.fixture(scope="session")
def user1():
    user = dict(id=1, username="tim", password=LAME_PASSWORD)
    return user


@pytest.fixture(scope="session")
def user2():
    user = dict(id=2, username="sara", password=LAME_PASSWORD)
    return user


@pytest.fixture(autouse=True, scope="session")
def insert_user(client, user1, user2):
    """Insert users in user DB"""
    for usr in (user1, user2):
        client.post("/create_user", json=usr)


@pytest.fixture(scope="session")
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


@pytest.fixture(scope="session")
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


def test_get_food_entry_without_auth(client, user1, food1):
    resp = client.get("/")
    assert resp.status_code == 401
    assert resp.json() == {"detail": "Not authenticated"}


def test_create_food_entry_without_auth(client, user1, food1):
    payload = dict(id=1, user=user1, food=food1, number_servings=1.5)
    resp = client.post("/", json=payload)
    assert resp.status_code == 401
    assert resp.json() == {"detail": "Not authenticated"}


def _get_token(client, username):
    payload = {"username": username, "password": LAME_PASSWORD}
    resp = client.post("/token", data=payload)
    return resp


def test_get_token_success(client, user1):
    resp = _get_token(client, user1["username"])
    assert resp.status_code == 200
    data = resp.json()
    assert "access_token" in data
    assert len(data["access_token"]) == 121
    assert data["token_type"] == "bearer"


def test_get_token_wrong_username(client):
    payload = {"username": "fake", "password": LAME_PASSWORD}
    resp = client.post("/token", data=payload)
    assert resp.status_code == 401
    assert resp.json() == {"detail": "Incorrect username or password"}


def test_get_token_wrong_password(client):
    payload = {"username": "tim", "password": "bad"}
    resp = client.post("/token", data=payload)
    assert resp.status_code == 401
    assert resp.json() == {"detail": "Incorrect username or password"}


def test_create_with_auth(client, user1, food1):
    resp = _get_token(client, user1["username"])
    data = resp.json()
    token = data["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    payload = dict(id=1, user=user1, food=food1, number_servings=1.5)
    resp = client.post("/", json=payload, headers=headers)
    assert resp.status_code == 201
    data = resp.json()
    assert data["id"] == 1
    assert data["user"]["id"] == 1
    assert data["food"]["name"] == "egg"
    assert data["number_servings"] == 1.5


def test_create_with_wrong_token(client, user1, food1):
    headers = {"Authorization": "Bearer fake_token"}
    payload = dict(id=1, user=user1, food=food1, number_servings=1.5)
    resp = client.post("/", json=payload, headers=headers)
    assert resp.status_code == 401
    assert resp.json() == {"detail": "Could not validate credentials"}


def test_can_only_create_own_foods(client, user1, user2, food1):
    resp = _get_token(client, user1["username"])
    data = resp.json()
    token = data["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    payload = dict(id=1, user=user2, food=food1, number_servings=1.5)
    resp = client.post("/", json=payload, headers=headers)
    assert resp.status_code == 400
    assert resp.json() == {"detail": "Can only add food for current user"}


def _create_food_as_user(client, payload, username):
    resp = _get_token(client, username)
    data = resp.json()
    token = data["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    resp = client.post("/", json=payload, headers=headers)
    assert resp.status_code == 201
    return headers


def test_get_only_returns_own_foods(client, user1, user2, food1, food2):
    payload = dict(id=1, user=user1, food=food1, number_servings=1.5)
    _create_food_as_user(client, payload, user1["username"])
    payload = dict(id=2, user=user2, food=food2, number_servings=2)
    headers = _create_food_as_user(client, payload, user2["username"])
    resp = client.get("/", headers=headers)
    # only seeing user2 foods
    assert resp.status_code == 200
    data = resp.json()
    assert len(data) == 1
    item = data[0]
    assert item["id"] == 2
    assert item["user"]["id"] == 2
    assert item["food"]["name"] == "oatmeal"
    assert item["number_servings"] == 2.0


def test_update_needs_login(client, user1, food1):
    payload = dict(id=1, user=user1, food=food1, number_servings=1.5)
    _create_food_as_user(client, payload, user1["username"])
    payload = dict(id=1, user=user1, food=food1, number_servings=2)
    resp = client.put("/1", json=payload)
    assert resp.status_code == 401
    assert resp.json() == {"detail": "Not authenticated"}


def test_update_wrong_food(client, user1, food1):
    payload = dict(id=1, user=user1, food=food1, number_servings=1.5)
    headers = _create_food_as_user(client, payload, user1["username"])
    payload = dict(id=1, user=user1, food=food1, number_servings=2)
    resp = client.put("/3", json=payload, headers=headers)
    assert resp.status_code == 404


def test_update_food_not_owner_by_user(client, user1, user2, food1, food2):
    payload = dict(id=1, user=user1, food=food1, number_servings=1.5)
    _create_food_as_user(client, payload, user1["username"])
    payload = dict(id=2, user=user2, food=food2, number_servings=2)
    headers = _create_food_as_user(client, payload, user2["username"])
    # cannot update user1 food as user2
    resp = client.put("/1", json=payload, headers=headers)
    assert resp.status_code == 400
    assert resp.json() == {"detail": "Food entry not owned by you"}


def test_update_food_owned_by_self(client, user1, user2, food1, food2):
    payload = dict(id=1, user=user1, food=food1, number_servings=1.5)
    headers = _create_food_as_user(client, payload, user1["username"])
    payload = dict(id=1, user=user1, food=food1, number_servings=2)
    resp = client.put("/1", json=payload, headers=headers)
    assert resp.status_code == 200
    data = resp.json()
    assert data["number_servings"] == 2.0


def test_delete_needs_login(client, user1, food1):
    payload = dict(id=1, user=user1, food=food1, number_servings=1.5)
    _create_food_as_user(client, payload, user1["username"])
    resp = client.delete("/1")
    assert resp.status_code == 401
    assert resp.json() == {"detail": "Not authenticated"}


def test_delete_wrong_food(client, user1, food1):
    payload = dict(id=1, user=user1, food=food1, number_servings=1.5)
    headers = _create_food_as_user(client, payload, user1["username"])
    resp = client.delete("/3", json=payload, headers=headers)
    assert resp.status_code == 404


def test_delete_food_not_owner_by_user(client, user1, user2, food1, food2):
    payload = dict(id=1, user=user1, food=food1, number_servings=1.5)
    _create_food_as_user(client, payload, user1["username"])
    payload = dict(id=2, user=user2, food=food2, number_servings=2)
    headers = _create_food_as_user(client, payload, user2["username"])
    # cannot delete user1 food as user2
    resp = client.delete("/1", headers=headers)
    assert resp.status_code == 400
    assert resp.json() == {"detail": "Food entry not owned by you"}


def test_delete_food_owned_by_self(client, user1, user2, food1, food2):
    payload = dict(id=1, user=user1, food=food1, number_servings=1.5)
    headers = _create_food_as_user(client, payload, user1["username"])
    resp = client.delete("/1", headers=headers)
    assert resp.status_code == 200
    assert resp.json() == {"ok": True}