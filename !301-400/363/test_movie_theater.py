import pytest

from movie_theater import invoice_refactored


def test_invoice_without_discount():
    assert invoice_refactored("Pulp Fiction", 1) == 10


def test_invoice_with_discount():
    assert invoice_refactored("Pulp Fiction", 6) == 50


def test_invoice_imax_movie():
    assert invoice_refactored("Tomorrow Never Dies", 3) == 36


def test_invoice_0_tickets():
    with pytest.raises(ValueError):
        invoice_refactored("Pulp Fiction", 0)


def test_invoice_unknown_movie():
    with pytest.raises(LookupError):
        invoice_refactored("Unknown Movie", 5)
