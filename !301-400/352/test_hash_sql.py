from random import shuffle

import pytest

from hash_sql import hash_query


@pytest.fixture
def complex_query():
    return """select Candidate, Election_year, sum(Total_$), count(*)
    from combined_party_data
    where Election_year = 2016
    group by Candidate, Election_year
    having count(*) > 80
    order by count(*) DESC;
    """


def test_hash_query_ignore_semicolon(complex_query: str):
    assert hash_query(complex_query) == hash_query(complex_query[:-1])


def test_hash_query_ignore_case_sensitive(complex_query: str):
    assert hash_query(complex_query) == hash_query(complex_query.upper())
    assert hash_query(complex_query) == hash_query(complex_query.title())
    assert hash_query(complex_query) == hash_query(complex_query.lower())
    assert hash_query(complex_query) == hash_query(complex_query.casefold())


def test_hash_query_ignore_backticks(complex_query: str):
    assert hash_query(complex_query) == hash_query(
        complex_query.replace("combined_party_data", "\"combined_party_data\"")
    )


def test_hash_query_ignore_order(complex_query: str):
    shuffled_query = complex_query.split()
    shuffle(shuffled_query)
    shuffled_query = " ".join(shuffled_query)
    assert hash_query(complex_query) == hash_query(shuffled_query)


@pytest.mark.parametrize("old, new", [
    ("=", "<"),
    ("=", ">"),
    ("=", "!="),
    ("=", "=="),
    ("Candidate", "Candidates"),
    ("80", "100"),
    ("group by", "groupby"),
    ("order by", "orderby"),
    ("DESC", "ASC"),
    ("sum(Total_$)", "Total_$"),
    ("combined_party_data", "combined_party"),
    ("2016", "2022")
])
def test_hash_query_detect_changes(complex_query: str, old: str, new: str):
    assert hash_query(complex_query) != hash_query(complex_query.replace(old, new))


def test_hash_query_stable_cache(complex_query: str):
    hash_ = hash_query(complex_query)
    assert hash_query(complex_query) == hash_


@pytest.mark.parametrize("length", [(1), (2), (5), (10), (11), (27), (50), (100)])
def test_hash_query_length_param(complex_query: str, length: int):
    assert len(hash_query(complex_query, length=length)) == length


def test_hash_query_invalid_length(complex_query: str):
    with pytest.raises(ValueError):
        hash_query(complex_query, length=-1)

    with pytest.raises(TypeError):
        hash_query(complex_query, length=1.1)
