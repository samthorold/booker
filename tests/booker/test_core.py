from datetime import date

import pytest

from booker.core import Account, Entry


ENTRY = Entry(ref="001", date=date(2022, 1, 1), value=100)


def test_entry_is_immutable():
    # dataclasses.FrozonInstanceError is subclass of AttributeError
    with pytest.raises(AttributeError):
        ENTRY.ref = "002"


def test_entry_hashable():
    hash(ENTRY)


def test_init_account_with_no_entries():
    _ = Account(code="1", name="a")


def test_account_dr_cr():
    a = Account(code="1", name="a")
    e = a.debit("001", date(2022, 1, 1), 100)
    assert isinstance(e, Entry)
    assert e.value == 100
    e = a.credit("001", date(2022, 1, 1), 100)
    assert isinstance(e, Entry)
    assert e.value == -100


def test_account_balance():
    a = Account(code="1", name="a")
    _ = a.debit("001", date(2022, 1, 1), 100)
    _ = a.credit("001", date(2022, 1, 1), 200)

    assert a.balance() == -100
