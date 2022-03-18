from datetime import datetime

import pytest
from bs4 import BeautifulSoup
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
    user = dict(id=1, username="Julian", password=LAME_PASSWORD)
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


@pytest.fixture
def food_entry1(user, food1):
    payload = dict(id=1, user=user, food=food1, number_servings=1.5)
    yield payload
    del food_log[1]


@pytest.fixture
def food_entry2(user, food2):
    payload = dict(id=2, user=user, food=food2, number_servings=2)
    yield payload
    del food_log[2]


@pytest.fixture(autouse=True)
def create_food_entries(client, food_entry1, food_entry2):
    client.post("/", json=food_entry1)
    client.post("/", json=food_entry2)


def test_show_foods_for_user(client):
    resp = client.get("/Julian")
    assert resp.status_code == 200
    try:
        soup = BeautifulSoup(resp.text, "html.parser")
    except Exception as exc:
        pytest.fail(f"Could not make soup object for testing, exception: {exc}")

    assert soup.title.text == "Food log for Julian"

    assert len(soup.findAll("tr")) == 2
    tds = soup.findAll("td")
    assert len(tds) == 8

    # datetimes change and freezegun did not work so best we can do is assert type
    dt1, dt2 = tds.pop(1).text, tds.pop(4).text
    for dt in (dt1, dt2):
        isinstance(datetime.strptime(dt, "%Y-%m-%d %H:%M:%S.%f"), datetime)

    # remaining cells are plain text
    text_cells = [td.text for td in tds]
    assert text_cells == [
        "egg",
        "1.5 x piece",
        "117.0",
        "oatmeal",
        "2.0 x 100 grams",
        "672.0",
    ]