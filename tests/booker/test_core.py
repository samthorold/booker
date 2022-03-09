from datetime import date

import pytest

from booker.core import Account, Entry, Sign


def test_entry_is_immutable():
    e = Entry(
        ref="001",
        date=date(2022, 1, 1),
        sign=Sign.DEBIT,
        amount=100,
    )

    # dataclasses.FrozonInstanceError is subclass of AttributeError
    with pytest.raises(AttributeError):
        e.amount = 200


def test_entry_hashable():
    e = Entry(
        ref="001",
        date=date(2022, 1, 1),
        sign=Sign.DEBIT,
        amount=100,
    )
    hash(e)


def test_no_entry_type_conversion():
    e = Entry(
        ref="001",
        date=date(2022, 1, 1),
        sign=1,
        amount=100,
    )

    assert isinstance(e.sign, int), type(e.sign)


def test_init_account_with_no_entries():
    _ = Account(code="1", name="a")
