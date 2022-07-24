from __future__ import annotations
from dataclasses import asdict, dataclass
from datetime import date as date_cls  # date a common name
from typing import Optional, Any


# https://github.com/cosmicpython/code/issues/17
@dataclass(unsafe_hash=True)
class Entry:
    """Ledger entry.

    Args:
        ref: Reference ID for 1+ Entry objects.
        account: Account code.
        date: Date of Entry.
        value: Value of Entry in pence.

    """

    ref: str
    account: str
    date: date_cls
    value: int

    @classmethod
    def from_dict(cls, d: dict[str, str | int]) -> Entry:
        ref = str(d["ref"])
        account = str(d["account"])
        date = date_cls.fromisoformat(str(d["date"]))
        value = int(d["value"])
        return Entry(
            ref=ref,
            account=account,
            date=date,
            value=value,
        )

    def __repr__(self):
        return f"<Entry({self.ref}, {self.account}, {self.date}, {self.value})>"

    def to_dict(self) -> dict[str, Any]:
        d = asdict(self)
        d["date"] = d["date"].isoformat()
        return d


class LedgerError(Exception):
    """Ledger domain base Exception."""


class PostingError(LedgerError):
    """PostingError base Exception."""


class NoSuchAccount(LedgerError):
    """No such account code in the ledger.

    As opposed to, say, an account with zero balance.
    """


class ClosingError(LedgerError):
    """ClosingError base Exception."""


class TransactionDoesNotBalance(PostingError):
    """The entries do not balance."""


class Ledger:
    """Aggregate for the Ledger domain.

    The version attribute is to prevent multiple processes writing to the same
    ledger simultaneously.

    Args:
        name: Name of the Ledger e.g. "General"
        entries: Entry objects associated with the Ledger.
        version: Helps to prevent concurrent writes.

    """

    # Tempting to put get classmethods here but they go on the unit of work.

    def __init__(
        self, name: str, entries: Optional[set[Entry]] = None, version: int = 0
    ) -> None:
        self.name = name
        self.entries: set[Entry] = set() if entries is None else entries
        self.version = version

    def __repr__(self):
        return f"<Ledger({self.name})>"

    def post(self, entries: set[Entry]) -> set[Entry]:
        """Post entries to the ledger.

        Args:
            entries: Entry objects to post

        Raises:
            TransactionDoesNotBalance: The entries do not balance.

        Returns:
            Entries added to the ledger.

        """

        if sum(e.value for e in entries) != 0:
            raise PostingError("Entries do not balance")

        # dangerous to not make a new object? e.g. set(...)
        original_entries = self.entries

        self.entries = original_entries | entries

        self.version += 1

        return self.entries - original_entries

    def balance(self, account: str, date: date_cls) -> int:
        """Get the balance for an account code.

        Args:
            account: Account code.

        Raises:
            NoSuchAccount: No corresponding account code in the ledger.

        Returns:
            Sum of the entries for the corresponding account.

        """
        entries = set(
            e for e in self.entries if e.account == account and e.date <= date
        )
        if not entries:
            raise NoSuchAccount(
                f"No entries for account '{account}'"
                f"prior to {date.strftime('%Y-%m-%d')}"
            )
        return sum(e.value for e in entries)

    def close_to(self, ref: str, ledger: Ledger, date: date_cls) -> set[Entry]:
        """Zero-out all accounts with non-zero balances and post corresponding
        entries to the given ledger.

        Args:
            ledger: Ledger to post closing entries to.
            date: Latest date to include entries from (inclusive).

        Raises:
            ClosingError: Issue closing the ledger.

        Returns:
            The closing enries.

        """

        # potentially a lot of entries but is only for a single ledger so may
        # not get too crazy
        accounts = set(e.account for e in self.entries)
        zeroing_out_entries = set(
            Entry(ref, a, date, bal * -1)
            for a in accounts
            if (bal := self.balance(a, date))
        )
        posted_zeroing_out_entries = self.post(zeroing_out_entries)

        if len(posted_zeroing_out_entries) != len(zeroing_out_entries):
            raise ClosingError(f"Is the reference, {ref}, correct?")

        closing_entries = set(
            Entry(ref, e.account, date, e.value * -1) for e in zeroing_out_entries
        )

        # if there is an exception here,
        # need to reverse out the posted_zeroing_out_entries
        # haven't found a way to test it though
        posted_closing_entries = ledger.post(closing_entries)

        if len(posted_closing_entries) != len(closing_entries):
            self.entries = self.entries - posted_zeroing_out_entries
            raise ClosingError(f"Is the reference, {ref}, correct?")

        return posted_closing_entries
