import pytest
from pydantic.error_wrappers import ValidationError

from models import Food


def test_create_food_object():
    food = Food(
        id=1,
        name="egg",
        serving_size="piece",
        kcal_per_serving=78,
        protein_grams=6.3,
        fibre_grams=0,
    )
    assert type(food) == Food
    assert food.id == 1
    assert food.name == "egg"
    assert food.serving_size == "piece"
    assert food.kcal_per_serving == 78
    assert food.protein_grams == 6.3
    assert food.fibre_grams == 0


def test_create_food_without_fibre():
    # no fibre in constructor
    food = Food(
        id=1, name="egg", serving_size="piece", kcal_per_serving=78, protein_grams=6.3
    )
    # hence it's set to default 0
    assert food.fibre_grams == 0


def test_create_food_required_attrs():
    with pytest.raises(ValidationError):
        # missing attrs like serving_size, kcal_per_serving, etc.
        Food(id=1, name="egg")


def test_create_food_wrong_serving_type():
    with pytest.raises(ValidationError):
        # note that name=2 is ok with pydantic, it gets casted
        Food(
            id=1,
            name="egg",
            serving_size="piece",
            kcal_per_serving="2ab",
            protein_grams=6.3,
            fibre_grams=1.2,
        )


def test_create_food_casting_no_exception():
    # "78" is ok, so is an int for protein's float type
    assert Food(
        id=1,
        name="egg",
        serving_size="piece",
        kcal_per_serving="78",
        protein_grams=6,
        fibre_grams=1.2,
    )
