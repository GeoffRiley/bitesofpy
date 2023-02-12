import pytest

from goal_tracker import goal_tracker


@pytest.mark.parametrize(
    "desc, annual_target, current_score, score_date, expected",
    [
        (
                "steps",
                5000000,
                164394,
                (2023, 1, 12),
                "Congratulations! You are on track with your steps goal. The target for 2023-01-12 is 164,383 steps "
                "and you are 11 ahead.",
        ),
        (
                "healthy snacks",
                722,
                119,
                (2000, 2, 29),
                "Congratulations! You are on track with your healthy snacks goal. The target for 2000-02-29 is 118 healthy "
                "snacks and you are 1 ahead.",
        ),
        (
                "days of code",
                365,
                77,
                (2021, 3, 18),
                "Congratulations! You are on track with your days of code goal. The target for 2021-03-18 is 77 days of code "
                "and you are 0 ahead.",
        ),
        (
                "pages read",
                36500,
                27298,
                (2023, 9, 30),
                "You have some catching up to do! The target for 2023-09-30 is 27,300 pages read and you are 2 behind.",
        ),
        (
                "minutes walked",
                (30 * 365),
                2500,
                (2021, 3, 30),
                "You have some catching up to do! The target for 2021-03-30 is 2,670 minutes walked and you are 170 behind.",
        ),
        (
                "pybites completed",
                5000,
                0,
                (2021, 1, 3),
                "You have some catching up to do! The target for 2021-01-03 is 41 pybites completed and you are 41 behind.",
        ),
        (
                "leaps",
                365,
                31,
                (2000, 2, 1),
                "Congratulations! You are on track with your leaps goal. The target for 2000-02-01 is 31 leaps and you are "
                "0 ahead.",
        ),
        (
                "jumps",
                365,
                31,
                (2023, 2, 1),
                "You have some catching up to do! The target for 2023-02-01 is 32 jumps and you are 1 behind.",
        ),
    ],
)
def test_bite_goal_tracker(desc, annual_target, current_score, score_date, expected):
    assert goal_tracker(desc, annual_target, current_score, score_date) == expected
