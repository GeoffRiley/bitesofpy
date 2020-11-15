import sqlite3

import pytest
from db_intro import DB, SQLiteType, SchemaError

NINJAS = [
    ("taspotts", 906),
    ("Tomade", 896),
    ("tasoak", 894),
    ("clamytoe", 890),
]

DB_SCHEMA = [("ninja", SQLiteType.TEXT), ("bitecoins", SQLiteType.INTEGER)]


@pytest.fixture
def db():
    with DB() as db:
        db.create("ninjas", DB_SCHEMA, "ninja")
        db.insert("ninjas", NINJAS)

        yield db


def test_empty_db():
    db = DB()
    assert db.location == ":memory:"
    assert db.cursor is None
    assert db.connection is None
    assert db.table_schemas == {}


@pytest.mark.parametrize(
    "table, schema, pk",
    [
        ("city", [("name", SQLiteType.TEXT), ("population", SQLiteType.REAL)], "name"),
        ("ninjas", DB_SCHEMA, "ninja"),
    ],
)
def test_create(table, schema, pk):
    with DB() as db:
        assert db.num_transactions == 0
        db.create(table, schema, pk)
        query = (
            f"SELECT name FROM sqlite_master WHERE type= 'table' AND name='{table}';"
        )
        output = db.cursor.execute(query).fetchall()
        assert len(output) == 1
        assert db.num_transactions == 0


def test_no_table_twice(db):
    with pytest.raises(sqlite3.OperationalError) as e:
        db.create("ninjas", DB_SCHEMA, "ninja")
    assert str(e.value) == "table ninjas already exists"


def test_wrong_pk():
    with pytest.raises(SchemaError) as e:
        with DB() as db:
            db.create("ninjas", DB_SCHEMA, "ID")

    assert str(e.value) == "The provided primary key must be part of the schema."


def test_insert(db):
    assert db.num_transactions == 4
    query = f"SELECT * FROM ninjas;"
    output = db.cursor.execute(query).fetchall()
    assert output == NINJAS


def test_insert_twice(db):
    with pytest.raises(sqlite3.IntegrityError) as e:
        db.insert("ninjas", NINJAS)

    assert str(e.value) in ("UNIQUE constraint failed: ninjas.ninja",
                            "column ninja is not unique")


@pytest.mark.parametrize(
    "table, bad_values, expected",
    [
        ("ninjas", [("Bob",)], 2),
        ("ninjas", [("Bob", 1000, 1)], 2),
        ("ninjas", [tuple()], 2),
        ("ninjas", [("Bob", 1000), ("pmayd",)], 2),
    ],
)
def test_incorrect_number_of_values_for_insert(db, table, bad_values, expected):
    with pytest.raises(SchemaError) as e:
        db.insert(table, bad_values)
    assert str(e.value) == f"Table {table} expects items with {expected} values."


@pytest.mark.parametrize(
    "table, bad_values, col, expected",
    [
        ("ninjas", [("Bob", "1000")], "bitecoins", int),
        ("ninjas", [(1000, "Bob")], "ninja", str),
        ("ninjas", [("Bob", 1000), ("pmayd", "128")], "bitecoins", int),
    ],
)
def test_wrong_value_type_for_insert(db, table, bad_values, col, expected):
    with pytest.raises(SchemaError) as e:
        db.insert(table, bad_values)

    assert str(e.value) == f"Column {col} expects values of type {expected.__name__}."


@pytest.mark.parametrize(
    "table, col, expected",
    [
        ("ninjas", None, NINJAS),
        ("ninjas", ["ninja"], sorted([(e[0],) for e in NINJAS])),
        ("ninjas", ["bitecoins"], [(e[1],) for e in NINJAS]),
    ],
)
def test_select(db, table, col, expected):
    rows = db.select(table, col)
    assert rows == expected


@pytest.mark.parametrize(
    "table, target, expected",
    [
        ("ninjas", ("ninja", "clamytoe"), [e for e in NINJAS if e[0] == "clamytoe"]),
        ("ninjas", ("bitecoins", 906), [e for e in NINJAS if e[1] == 906]),
    ],
)
def test_select_db_target(db, table, target, expected):
    row = db.select(table, target=target)
    assert row == expected


@pytest.mark.parametrize(
    "table, target, expected",
    [
        ("ninjas", ("bitecoins", ">", 900), [e for e in NINJAS if e[1] > 900]),
        ("ninjas", ("ninja", "LIKE", "%pot%"), [e for e in NINJAS if "pot" in e[0]]),
        ("ninjas", ("ninja", "<>", "Tomade"), [e for e in NINJAS if e[0] != "Tomade"]),
    ],
)
def test_select_operator(db, table, target, expected):
    rows = db.select(table, target=target)
    assert rows == expected


@pytest.mark.parametrize(
    "table, new_value, target, expected",
    [
        ("ninjas", ("bitecoins", 1000), ("ninja", "clamytoe"), [("clamytoe", 1000)]),
        ("ninjas", ("ninja", "tomade"), ("ninja", "Tomade"), [("tomade", 896)]),
    ],
)
def test_update_db(db, table, new_value, target, expected):
    db.update("ninjas", new_value, target)
    assert db.num_transactions == 5

    rows = db.select(table, target=new_value)
    assert rows == expected


@pytest.mark.parametrize(
    "table, target", [("ninjas", ("ninja", "clamytoe")), ("ninjas", ("bitecoins", 906))]
)
def test_delete_db(db, table, target):
    db.delete(table, target)
    rows = db.select(table, target=target)
    assert rows == []
