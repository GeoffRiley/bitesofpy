import pytest
from fastapi.testclient import TestClient

from app import app, food_log, pwd_context

LAME_PASSWORD = "1234"  # noqa S105


# also from https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/
def _verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


@pytest.fixture
def client():
    client = TestClient(app)
    return client


@pytest.fixture
def user():
    user = dict(id=1, username="user", password=LAME_PASSWORD)
    return user


@pytest.fixture
def food():
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
def food_entry1(user, food):
    payload = dict(id=1, user=user, food=food, number_servings=1.5)
    yield payload
    del food_log[1]


@pytest.fixture
def food_entry2(user, food):
    payload = dict(id=2, user=user, food=food, number_servings=27.5)
    yield payload
    del food_log[2]


@pytest.fixture(autouse=True)
def create_food_entries(client, food_entry1):
    client.post("/", json=food_entry1)


def test_cannot_insert_same_food_entry_id_twice(client, food_entry1):
    resp = client.post("/", json=food_entry1)
    assert resp.status_code == 400
    error = "Food entry already logged, use an update request"
    expected = {"detail": error}
    assert resp.json() == expected


def test_cannot_overeat(client, food_entry2):
    # 29 x 78 kcal > 2.250 default daily calories
    resp = client.post("/", json=food_entry2)
    assert resp.status_code == 201
    # oops this will hit 2262.0 kcal > 2250 limit
    food_entry3 = food_entry2.copy()
    food_entry3["id"] = 3
    food_entry3["number_servings"] = 1
    resp = client.post("/", json=food_entry3)
    assert resp.status_code == 400
    error = "Cannot add more food than daily caloric allowance = 2250 kcal / day"
    expected = {"detail": error}
    assert resp.json() == expected
