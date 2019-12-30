import pytest

from workouts import print_workout_days


@pytest.mark.parametrize('match, result', [
    ('cardio', 'Wed'),
    ('UPPER', 'Mon, Thu'),
    ('Body', 'Mon, Tue, Thu, Fri'),
    ('march', 'No matching workout')
])
def test_print_workout_days(capsys, match, result):
    print_workout_days(match)
    captured = capsys.readouterr()
    assert captured.out.strip() == result
