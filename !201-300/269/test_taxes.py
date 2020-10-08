import pytest

from taxes import Bracket, Taxed, Taxes

bracket_2020 = [
    Bracket(9_875, 0.1),
    Bracket(40_125, 0.12),
    Bracket(85_525, 0.22),
    Bracket(163_300, 0.24),
    Bracket(207_350, 0.32),
    Bracket(518_400, 0.35),
    Bracket(518_401, 0.37),
]


@pytest.fixture(scope="module")
def taxes_2019():
    income = 40_000
    return Taxes(income)


@pytest.fixture(scope="module")
def taxes_2020_low():
    income = 8_000
    return Taxes(income, bracket_2020)


@pytest.fixture(scope="module")
def taxes_2020_over():
    income = 1_000_000
    return Taxes(income, bracket_2020)


def test_values(taxes_2019):
    assert taxes_2019.income == 40_000
    assert taxes_2019.total == 4_658.50
    assert taxes_2019.tax_rate == 11.65
    assert isinstance(taxes_2019.bracket, list)
    assert isinstance(taxes_2019.bracket[0], Bracket)


def test_taxes(taxes_2019):
    assert len(taxes_2019.tax_amounts) == 3
    assert isinstance(taxes_2019.tax_amounts[0], Taxed)
    assert taxes_2019.tax_amounts[2].tax == 115.50


def test_summary(taxes_2019):
    output = str(taxes_2019).splitlines()
    assert len(output) == 5
    assert "Summary Report" in output[0]


def test_low_income(taxes_2020_low):
    assert taxes_2020_low.taxes == 800.00


def test_report(taxes_2020_over, capfd):
    taxes_2020_over.report()
    output = capfd.readouterr()[0].strip().splitlines()
    assert len(output) == 17
    assert "Summary Report" in output[0]
    assert "Taxes Breakdown" in output[6]
    assert "=" in output[1]
    assert len(output[1]) == 34
    assert "-" in output[-2]
    assert "14,096.00" in output[-5]
    assert "0.24" in output[-6]
