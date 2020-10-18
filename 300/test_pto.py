import pto
import pytest
from pto import four_day_weekends


def test_four_day_weekends_default(capfd):
    four_day_weekends()
    output = capfd.readouterr()[0].splitlines()
    assert len(output) == 23
    assert "18 Four-Day Weekends" in output[0]
    assert "(25 days)" in output[2]
    assert "(11 days)" in output[3]
    assert "*" in output[10]
    assert output[-2] == "2020-12-11 - 2020-12-14"


def test_four_day_weekends_workdays(capfd):
    four_day_weekends(show_workdays=True)
    output = capfd.readouterr()[0].splitlines()
    assert len(output) == 24
    assert "Remaining Work Days: 184 (23 days)" in output[0]
    assert output[-1] == "2020-12-31"


def test_four_day_weekends_invalid_call():
    with pytest.raises(ValueError) as e:
        four_day_weekends(True)
    assert str(e.value) == pto.ERROR_MSG


def test_four_day_weekends_invalid_call_custom_error_message():
    new_msg = "You're calling it wrong dude!"
    pto.ERROR_MSG = new_msg
    with pytest.raises(ValueError) as e:
        four_day_weekends(True)
    assert str(e.value) == new_msg


def test_four_day_weekends_october(capfd):
    four_day_weekends(start_month=10)
    output = capfd.readouterr()[0].splitlines()
    assert len(output) == 16
    assert "(3 days)" in output[3]
    assert output[10] == "2020-11-13 - 2020-11-16"


def test_four_day_weekends_october_work_days(capfd):
    four_day_weekends(start_month=10, show_workdays=True)
    output = capfd.readouterr()[0].splitlines()
    assert len(output) == 15
    assert "(14 days)" in output[0]
    assert output[10] == "2020-12-10"


def test_four_day_weekends_less_pto(capfd):
    four_day_weekends(start_month=10, paid_time_off=120)
    output = capfd.readouterr()[0].splitlines()
    assert len(output) == 16
    assert "11" in output[0]
    assert "120" in output[2]
    assert "-56" in output[3]
    assert "*" in output[8]


def test_four_day_weekends_no_event_horizon(capfd):
    four_day_weekends(start_month=10, paid_time_off=284)
    output = capfd.readouterr()[0].splitlines()
    for line in output:
        assert "*" not in line


def test_four_day_weekends_pto_160(capfd):
    four_day_weekends(paid_time_off=160)
    output = capfd.readouterr()[0].splitlines()
    assert "*" in output[13]


def test_four_day_weekends_pto_odd(capfd):
    four_day_weekends(start_month=11, paid_time_off=55)
    output = capfd.readouterr()[0].splitlines()
    assert "*" in output[7]
