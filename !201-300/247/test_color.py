from unittest.mock import patch

import color
import pytest


@pytest.fixture(scope="module")
def gen():
    return color.gen_hex_color()


@pytest.mark.parametrize('test_values, result', [
    ([1, 2, 3], '#010203'),
    ([0, 1, 2], '#000102'),
    ([255, 254, 253], '#FFFEFD'),
    ([-1, -2, -3], '#-1-2-3'),
    ([254, 255, 256], '#FEFF100'),
    ([1, 2, 3, 4], pytest.raises(ValueError))
])
@patch('color.sample')
def test_gen_hex_color(mock_sample, gen, test_values, result):
    mock_sample.return_value = test_values
    if isinstance(result, str):
        assert next(gen) == result
    else:
        with result:
            assert next(gen)
    mock_sample.assert_called_with(range(0, 256), 3)
