from unittest.mock import patch

import pytest
from guess import GuessGame, InvalidNumber

SECRET_NUMBER = 7


@pytest.fixture(scope='module')
def the_game():
    return GuessGame(SECRET_NUMBER)


def test_game_basics(the_game):
    assert the_game.attempt == 0
    assert the_game.secret_number == SECRET_NUMBER
    assert the_game.max_guesses == 5


@pytest.mark.parametrize('guess, result', [
    ('not a bally old number squire', 'Not a number'),
    (-1, 'Negative number'),
    (16, 'Number too high')
])
def test_validate_fails(the_game, guess, result):
    with pytest.raises(InvalidNumber) as exc:
        the_game._validate(guess)
    assert result in str(exc.value)


@pytest.mark.parametrize('guess, result', [
    (None, "int() argument must be a string, a bytes-like object or a number, not 'NoneType'"),
    ([1], "int() argument must be a string, a bytes-like object or a number, not 'list'"),
    ((1,), "int() argument must be a string, a bytes-like object or a number, not 'tuple'")
])
def test_validate_dreadfuls(the_game, guess, result):
    with pytest.raises(TypeError) as exc:
        the_game._validate(guess)
    assert result in str(exc.value)


@pytest.mark.parametrize('guess, result', [
    (0, 0),
    ('7', 7),
    (2.5, 2),
    (15, 15)
])
def test_validate_passes(the_game, guess, result):
    assert the_game._validate(guess) == result


@patch("builtins.input", side_effect=[12, 10, 8, 4, 6])
def test_guess_correct_full(input_mock, capsys):
    the_game = GuessGame(5)
    the_game()
    actual = capsys.readouterr()[0].strip()
    expected = '\n'.join([
        'Guess a number: ',
        'Too high',
        'Guess a number: ',
        'Too high',
        'Guess a number: ',
        'Too high',
        'Guess a number: ',
        'Too low',
        'Guess a number: ',
        'Too high',
        'Sorry, the number was 5'
    ])
    assert actual == expected


@patch("builtins.input", side_effect=[7, 3, 5])
def test_guess_correct(input_mock, capsys):
    the_game = GuessGame(5, max_guesses=3)
    the_game()
    actual = capsys.readouterr()[0].strip()
    expected = '\n'.join([
        'Guess a number: ',
        'Too high',
        'Guess a number: ',
        'Too low',
        'Guess a number: ',
        'You guessed it!'
    ])
    assert actual == expected
    assert the_game.attempt == 3


@patch("builtins.input", side_effect=[7, 3, 6])
def test_guess_out_of_turns(input_mock, capsys):
    the_game = GuessGame(5, max_guesses=3)
    the_game()
    actual = capsys.readouterr()[0].strip()
    expected = '\n'.join([
        'Guess a number: ',
        'Too high',
        'Guess a number: ',
        'Too low',
        'Guess a number: ',
        'Too high',
        'Sorry, the number was 5'
    ])
    assert actual == expected
    assert the_game.attempt == 3


@patch("builtins.input", side_effect=[7, 'frog', 5])
def test_guess_bad_guess(input_mock, capsys):
    the_game = GuessGame(5, max_guesses=3)
    the_game()
    actual = capsys.readouterr()[0].strip()
    expected = '\n'.join([
        'Guess a number: ',
        'Too high',
        'Guess a number: ',
        'Enter a number, try again',
        'Guess a number: ',
        'You guessed it!'
    ])
    assert actual == expected
    assert the_game.attempt == 2


@patch("builtins.input", side_effect=[7, 'frog', 4])
def test_guess_bad_guess_out_of_turns(input_mock, capsys):
    the_game = GuessGame(5, max_guesses=2)
    the_game()
    actual = capsys.readouterr()[0].strip()
    expected = '\n'.join([
        'Guess a number: ',
        'Too high',
        'Guess a number: ',
        'Enter a number, try again',
        'Guess a number: ',
        'Too low',
        'Sorry, the number was 5'
    ])
    assert actual == expected
    assert the_game.attempt == 2
