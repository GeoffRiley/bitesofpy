import os

import pytest
from movies import MovieDb

DB = os.path.join(os.getenv("TMP", "/tmp"), 'movies.db')
# https://www.imdb.com/list/ls055592025/
DATA = [
    ("The Godfather", 1972, 9.2),
    ("The Shawshank Redemption", 1994, 9.3),
    ("Schindler's List", 1993, 8.9),
    ("Raging Bull", 1980, 8.2),
    ("Casablanca", 1942, 8.5),
    ("Citizen Kane", 1941, 8.3),
    ("Gone with the Wind", 1939, 8.1),
    ("The Wizard of Oz", 1939, 8),
    ("One Flew Over the Cuckoo's Nest", 1975, 8.7),
    ("Lawrence of Arabia", 1962, 8.3),
]
TABLE = 'movies'


@pytest.fixture(scope='module')
def db():
    # instantiate MovieDb class using above constants
    # do proper setup / teardown using MovieDb methods
    # https://docs.pytest.org/en/latest/fixture.html (hint: yield)
    movies = MovieDb(DB, DATA, TABLE)
    movies.init()

    yield movies

    movies.drop_table()


# write tests for all MovieDb's query / add / delete
def test_query(db):
    assert len(db.query(title='godfather')) == 1
    assert len(db.query(title='the')) == 5
    assert db.query(title='Arabia')[0][2] == 1962
    assert db.query(year=1942)[0][1] == 'Casablanca'
    assert len(db.query(score_gt=9.2)) == 1


def test_add(db):
    assert db.add('Soylent Green', 1973, 7.1) == 11


def test_delete(db):
    assert len(db.query(title='soylent')) == 1
    db.delete(11)
    assert len(db.query(title='soylent')) == 0
