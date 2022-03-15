from datetime import date

import pytest

from ledger.domain import Entry, Ledger, PostingError


ENTRY = Entry(ref="001", account="001", date=date(2022, 1, 1), value=100)

BALANCED_ENTRIES = set(
    [
        Entry(ref="001", account="001", date=date(2022, 1, 1), value=100),
        Entry(ref="001", account="002", date=date(2022, 1, 1), value=-100),
    ]
)

UNBALANCED_ENTRIES = set(
    [
        Entry(ref="001", account="001", date=date(2022, 1, 1), value=100),
        Entry(ref="001", account="002", date=date(2022, 1, 1), value=-101),
    ]
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
    l = Ledger(entries=set([ENTRY]))
    assert len(l.entries) == 1


def test_post_balanced_entries():
    l = Ledger()

    es = l.post(BALANCED_ENTRIES)

    assert len(l.entries) == len(es)


def test_post_unbalanced_entries():
    l = Ledger()

    with pytest.raises(PostingError):
        _ = l.post(UNBALANCED_ENTRIES)
