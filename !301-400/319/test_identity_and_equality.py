import pytest

from identity_and_equality import (
    Car,
    is_same_car_color_and_model,
    is_same_instance_of_car,
)


# `NewList` for tests
class NewList(list):
    pass


# A bunch of lists to test
l1 = [["gas", "electro", "hybrid"], "200 PS", "radio"]
l2 = l1
l3 = l1.copy()
l4 = l1[0]
l5 = [l4, "digital radio"]
l6 = [l1[0], "digital radio"]
l7 = NewList(l1)
l8 = ["unleaded"]

# A bunch of `Car`s
my_car = Car("Toyota Corolla", "black")
other_car1 = my_car
other_car2 = Car("Toyota Corolla", "black")
other_car3 = Car("Toyota Corolla", "red")
other_car4 = Car("Porsche Cayenne", "black")


# Test staticmethod Car.age
@pytest.mark.parametrize(
    "days, expected",
    [
        (7, "A week old"),  # week
        (365, "A year old"),  # year
        (2, "Neither a week, nor a year old"),  # Other number
    ],
)
def test_car_age(days, expected):
    assert Car.age(days) == expected


# Test staticmethod Car.age
@pytest.mark.parametrize(
    "list1, list2, expected",
    [
        ([], [], True),  # Empty
        (l1, l2, True),  # same instance
        (l1, l1[:], True),  # full copy
        (l1, l3, True),  # full copy
        (l5, l6, True),  # Two identical short lists
        (l5[0], l6[0], True),  # First element of short lists (same instances)
        (l1, l7, True),  # One list, one NewList, same contents
        (l1, l8, False),  # Two completely different lists
    ],
)
def test_the_same_configuration(list1, list2, expected):
    assert Car.has_same_configuration(list1, list2) == expected


@pytest.mark.parametrize(
    "car1, car2, expected",
    [
        (my_car, my_car, True),  # Identical cars (same instance)
        (my_car, other_car1, True),  # Identical cars (same instance)
        (my_car, other_car2, True),  # Car of the same model and color
        (other_car2, other_car3, False),  # Completely different cars
    ],
)
def test_is_same_car_color_and_model(car1, car2, expected):
    assert is_same_car_color_and_model(car1, car2) == expected


@pytest.mark.parametrize(
    "car1, car2, expected",
    [
        (my_car, my_car, True),  # Same instance
        (my_car, other_car1, True),  # Same Car, different instance
        (other_car1, other_car2, False),  # Completely different cars
    ],
)
def test_is_the_same_instance_of_car(car1, car2, expected):
    assert is_same_instance_of_car(car1, car2) == expected
