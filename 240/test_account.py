import pytest
from account import Account


# write your pytest functions below, they need to start with test_
@pytest.fixture
def einstein():
    return Account('Einstein', 100)


@pytest.fixture
def socrates():
    return Account('Socrates', 0)


def add_transactions(acct, values):
    for v in values:
        acct.add_transaction(v)


def test_account_create(einstein):
    assert isinstance(einstein, Account)
    assert einstein.balance == 100
    assert str(einstein) == 'Account of Einstein with starting amount: 100'
    assert repr(einstein) == "Account('Einstein', 100)"


def test_account_transaction(einstein):
    assert einstein.balance == 100
    einstein.add_transaction(50)
    assert einstein.balance == 150
    einstein.add_transaction(-75)
    assert einstein.balance == 75
    assert len(einstein) == 2


def test_account_bad_transaction(socrates):
    assert socrates.balance == 0
    with pytest.raises(ValueError):
        socrates.add_transaction(3.14)
    assert socrates.balance == 0


def test_account_comparisons(einstein, socrates):
    assert einstein > socrates
    add_transactions(socrates, [10, 20, 30])
    assert socrates.balance == 60
    assert socrates[1] == 20


def test_account_merge_acounts(einstein, socrates):
    assert einstein.balance == 100 and socrates.balance == 0
    add_transactions(einstein, [50, -75])
    add_transactions(socrates, [10, 20, 30])
    assert einstein.balance == 75 and socrates.balance == 60
    pythagoras = einstein + socrates
    assert pythagoras.balance == 135
    assert str(pythagoras) == 'Account of Einstein&Socrates with starting amount: 100'
    assert len(pythagoras) == 5
    assert pythagoras[1] == -75
