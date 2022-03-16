from datetime import date

import pytest

from ledger.domain import Entry, Ledger, PostingError


TODAY = date(2022, 1, 1)

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
    Ledger()


def test_init_ledger_with_entries():
    l = Ledger(set([ENTRY]))
    assert len(l.entries) == 1


def test_post_balanced_entries():
    l = Ledger()
    entries = create_transaction("001", (100, -100))
    es = l.post(entries)
    assert len(l.entries) == len(es)


def test_post_unbalanced_entries():
    l = Ledger()
    entries = create_transaction("001", (100, -101))
    with pytest.raises(PostingError):
        _ = l.post(entries)


def test_ledger_can_get_account_balance():
    entries = create_transaction("001", (100, -100))
    l = Ledger(entries)
    assert l.balance("001") == 100
    assert l.balance("002") == -100
    entries = create_transaction("002", (100, -100))
    _ = l.post(entries)
    assert l.balance("001") == 200
    assert l.balance("002") == -200


def test_ledger_post_idempotent():
    entries = create_transaction("001", (100, -100))
    l = Ledger(entries)
    assert l.balance("001") == 100
    assert l.balance("002") == -100
    entries = create_transaction("001", (100, -100))
    _ = l.post(entries)
    assert l.balance("001") == 100
    assert l.balance("002") == -100
