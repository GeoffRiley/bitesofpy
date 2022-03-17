from datetime import datetime, timedelta

import pytest
from pydantic.error_wrappers import ValidationError

from models import Food, FoodEntry, User, pwd_context

LAME_PASSWORD = "1234"  # noqa S105


# also from https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/
def _verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


@pytest.fixture
def user():
    user = User(id=1, username="user1", password=LAME_PASSWORD)
    return user


@pytest.fixture
def food():
    food = Food(
        id=1,
        name="egg",
        serving_size="piece",
        kcal_per_serving=78,
        protein_grams=6.3,
        fibre_grams=0,
    )
    return food


def test_create_user_object(user):
    assert type(user) == User
    assert user.id == 1
    assert user.username == "user1"
    assert _verify_password(LAME_PASSWORD, user.password) is True


def test_create_incomplete_user_object():
    error = "username\n.*field required"
    with pytest.raises(ValidationError, match=error):
        User(id=1, password="abc")


def test_create_user_object_wrong_type():
    error = "User\nid\n  value is not a valid integer"
    with pytest.raises(ValidationError, match=error):
        User(id="1abc", username="user1", password="abc")


def test_create_food_log_object(user, food):
    food_entry = FoodEntry(id=1, user=user, food=food, number_servings=1.5)
    now = datetime.now()
    assert abs(food_entry.date_added - now) < timedelta(seconds=10)
    assert food_entry.user == user
    assert food_entry.food == food
    assert food_entry.number_servings == 1.5
    assert food_entry.total_calories == 1.5 * 78


def test_create_food_missing_data(user, food):
    error = "user\n.*field required"
    with pytest.raises(ValidationError, match=error):
        FoodEntry(id=1, food=food, number_servings=1.5)