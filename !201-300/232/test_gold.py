from gold import gold_prices, years_gold_value_decreased


def test_gold_prices_full_data_set():
    actual = years_gold_value_decreased()
    expected = (2013, 2009)
    assert actual == expected


def test_gold_prices_1950_1999():
    data = '\n'.join(gold_prices.strip().splitlines()[:10])
    actual = years_gold_value_decreased(data)
    expected = (1981, 1979)
    assert actual == expected


def test_gold_prices_till_1980_1989():
    data = '\n'.join(gold_prices.strip().splitlines()[-8:-6])
    actual = years_gold_value_decreased(data)
    expected = (1981, 1987)
    assert actual == expected
