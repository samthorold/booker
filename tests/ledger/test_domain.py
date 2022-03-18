from datetime import date as date_cls

import pytest

from ledger.domain import ClosingError, Entry, Ledger, NoSuchAccount, PostingError


YESTERDAY = date_cls(2021, 12, 31)
TODAY = date_cls(2022, 1, 1)
TOMORROW = date_cls(2022, 1, 2)

ENTRY = Entry(ref="001", account="001", date=TODAY, value=100)


def create_transaction(ref, values, accounts=None, date=TODAY) -> set[Entry]:
    accounts = ("001", "002") if accounts is None else accounts
    if len(accounts) != len(values):
        raise ValueError(
            f"accounts {accounts} and values {values} must be the same length"
        )
    return set(
        [Entry(ref, account, date, value) for account, value in zip(accounts, values)]
    )


def test_entry_is_immutable():
    # dataclasses.FrozonInstanceError is subclass of AttributeError
    with pytest.raises(AttributeError):
        ENTRY.ref = "002"

    with pytest.raises(AttributeError):
        ENTRY.account = "002"


def test_entry_hashable():
    hash(ENTRY)


def test_init_ledger_with_no_entries():
    Ledger("Gen")


def test_init_ledger_with_entries():
    l = Ledger("Gen", set([ENTRY]))
    assert len(l.entries) == 1


def test_post_balanced_entries():
    l = Ledger("Gen")
    entries = create_transaction("001", (100, -100))
    es = l.post(entries)
    assert len(l.entries) == len(es)


def test_post_unbalanced_entries():
    l = Ledger("Gen")
    entries = create_transaction("001", (100, -101))
    with pytest.raises(PostingError):
        _ = l.post(entries)


def test_ledger_can_get_account_balance():
    l = Ledger("Gen", create_transaction("001", (100, -100), date=YESTERDAY))
    assert l.balance("001", TODAY) == 100
    assert l.balance("002", TODAY) == -100

    _ = l.post(create_transaction("002", (100, -100), date=TODAY))
    assert l.balance("001", TODAY) == 200
    assert l.balance("002", TODAY) == -200

    _ = l.post(create_transaction("003", (100, -100), date=TOMORROW))
    assert l.balance("001", TODAY) == 200
    assert l.balance("002", TODAY) == -200
    assert l.balance("001", TOMORROW) == 300
    assert l.balance("002", TOMORROW) == -300


def test_ledger_balance_no_account():
    with pytest.raises(NoSuchAccount):
        Ledger("gen").balance("5", TODAY)


def test_ledger_post_idempotent():
    entries = create_transaction("001", (100, -100))
    l = Ledger("Gen", entries)
    assert l.balance("001", TODAY) == 100
    assert l.balance("002", TODAY) == -100
    entries = create_transaction("001", (100, -100))
    _ = l.post(entries)
    assert l.balance("001", TODAY) == 100
    assert l.balance("002", TODAY) == -100


def test_ledger_close_to_reused_reference():
    general = Ledger("General")
    sales = Ledger("Sales")
    _ = sales.post(create_transaction("001", (100, -100), ("001", "002"), TODAY))
    _ = sales.post(create_transaction("002", (-100, 100), ("001", "002"), TODAY))
    _ = sales.post(create_transaction("003", (100, -100), ("001", "002"), TODAY))
    with pytest.raises(ClosingError):
        _ = sales.close_to("002", general, TODAY)

    general = Ledger("General")
    _ = general.post(create_transaction("001", (100, -100), ("001", "002"), TODAY))
    sales = Ledger("Sales")
    _ = sales.post(create_transaction("001", (100, -100), ("001", "002"), TODAY))
    _ = sales.post(create_transaction("002", (-100, 100), ("001", "002"), TODAY))
    _ = sales.post(create_transaction("003", (100, -100), ("001", "002"), TODAY))
    with pytest.raises(ClosingError):
        _ = sales.close_to("001", general, TODAY)


def test_ledger_close_to():
    general = Ledger("General")
    sales = Ledger("Sales")
    assert not sales.close_to("close sales", general, TODAY)

    _ = sales.post(create_transaction("001", (100, -100), ("001", "002"), YESTERDAY))
    _ = sales.post(create_transaction("002", (100, -100), ("001", "002"), TODAY))
    _ = sales.post(create_transaction("003", (100, -100), ("003", "004"), YESTERDAY))
    _ = sales.post(create_transaction("004", (-100, 100), ("003", "004"), TODAY))
    _ = sales.post(create_transaction("005", (100, -100), ("001", "002"), TOMORROW))

    closing_entries = sales.close_to("close sales", general, TODAY)

    # only as many closing entries as accounts with non-zero balance
    assert len(closing_entries) == 2
    assert all(sales.balance(a, TODAY) == 0 for a in ("001", "002"))
    assert sales.balance("001", TOMORROW) == 100
    assert sales.balance("002", TOMORROW) == -100
    assert general.balance("001", TODAY) == 200
    assert general.balance("002", TODAY) == -200
    assert general.balance("001", TOMORROW) == 200
    assert general.balance("002", TOMORROW) == -200

    closing_entries = sales.close_to("close sales", general, TODAY)

    # should be noop
    assert not closing_entries
    assert all(sales.balance(a, TODAY) == 0 for a in ("001", "002"))
    assert sales.balance("001", TOMORROW) == 100
    assert sales.balance("002", TOMORROW) == -100
    assert general.balance("001", TODAY) == 200
    assert general.balance("002", TODAY) == -200
    assert general.balance("001", TOMORROW) == 200
    assert general.balance("002", TOMORROW) == -200
