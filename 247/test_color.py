from unittest.mock import patch

import pytest

import color


@pytest.fixture(scope="module")
def gen():
    return color.gen_hex_color()


@pytest.mark.parametrize('test_values, result', [
    ([1, 2, 3], '#010203'),
    ([0, 0, 0], '#000000'),
    ([255,255,255], '#FFFFFF'),
    ([-1,-1,-1], '#-1-1-1'),
    ([256,256,256], '#100100100')
])
@patch('color.sample')
def test_gen_hex_color(mock_sample, gen, test_values, result):
    mock_sample.return_value = test_values
    assert next(gen) == result
