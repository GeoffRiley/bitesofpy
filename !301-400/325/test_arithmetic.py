from arithmetic import calc_sums, VALUES

EXPECTED = (
    ("0.1", "0.2", "0.30"),
    ("0.2", "0.3", "0.50"),
    ("0.3", "0.005", "0.31"),
    ("0.005", "0.005", "0.01"),
    ("0.005", "2.67", "2.68"),
)


def test_calc_sums():
    i = 0
    for i, line in enumerate(calc_sums(VALUES)):
        n1, n2, sum_ = EXPECTED[i]
        assert (
                line == f"The sum of {n1} and {n2}, rounded to two decimal places, is {sum_}."
        )

    # Confirm all output was generated
    assert i == len(EXPECTED) - 1, "Not all output was generated!"
