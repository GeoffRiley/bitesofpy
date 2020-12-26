import logging

import pytest

from logger import sum_even_numbers


def test_sum_numbers_function_works(caplog):
    assert sum_even_numbers([2, 9, 4, 11, 6]) == 12


def test_sum_numbers_logging(caplog):
    caplog.set_level(logging.INFO, logger="app")
    sum_even_numbers(list(range(1, 11)))
    assert len(caplog.records) == 1
    record = caplog.records[0]
    assert record.module == 'logger'
    assert record.name == 'app'
    assert record.levelname == 'INFO'
    expected = 'Input: [1, 2, 3, 4, 5, 6, 7, 8, 9, 10] -> output: 30'
    assert record.message == expected


def test_sum_numbers_throws_exception(caplog):
    caplog.set_level(logging.INFO, logger="app")
    with pytest.raises(TypeError):
        sum_even_numbers([1, 'a', 2, 3])
    assert len(caplog.records) == 1
    record = caplog.records[0]
    assert record.levelname == 'ERROR'
    expected = "Bad inputs: [1, 'a', 2, 3]"
    assert record.message == expected
    assert record.exc_text.startswith('Traceback')
    assert record.exc_text.endswith(
        ('TypeError: not all arguments converted during '
         'string formatting'))
