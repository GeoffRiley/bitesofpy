import pytest

from to_columns import print_names_to_columns


@pytest.fixture
def names():
    return "Bob Julian Tim Sara Eva Ana Jake Maria".split()


def test_default(capfd, names):
    print_names_to_columns(names)
    actual = capfd.readouterr()[0].strip()
    expected = ("| Bob       | Julian    \n"
                "| Tim       | Sara      \n"
                "| Eva       | Ana       \n"
                "| Jake      | Maria")
    assert actual == expected


def test_three_columns(capfd, names):
    print_names_to_columns(names, cols=3)
    actual = capfd.readouterr()[0].strip()
    expected = ("| Bob       | Julian    | Tim       \n"
                "| Sara      | Eva       | Ana       \n"
                "| Jake      | Maria")
    assert actual == expected


def test_four_columns(capfd, names):
    print_names_to_columns(names, cols=4)
    actual = capfd.readouterr()[0].strip()
    expected = ("| Bob       | Julian    | Tim       | Sara      \n"
                "| Eva       | Ana       | Jake      | Maria")
    assert actual == expected
