from dataclasses import dataclass, field
from datetime import date
from enum import Enum


@dataclass(kw_only=True, frozen=True)
class Entry:
    """Journal entry.

    Args:
        ref: Reference ID for 1+ Entry objects.
        date: Date of Entry.
        Value: Value of Entry in pence.

    """

    ref: str
    date: date
    value: int


@dataclass(kw_only=True)
class Account:
    """Account.

    Args:
        code: Unique Account code.
        name: Human-friendly Account name.
        entries: Entry objects associated with the Account.

    """

    code: str
    name: str
    entries: set[Entry] = field(default_factory=set)

    def _entry(self, ref: str, date: date, value: int) -> Entry:
        return Entry(ref=ref, date=date, value=value)

    def balance(self) -> int:
        """Sum of the Entry objects associated with the Account.

        Returns:
            int

        """
        return sum(e.value for e in self.entries)

    def debit(self, ref: str, date: date, value: int) -> Entry:
        """Debit the Account.

        Creates a new Entry object and assoicates it with the Account.

        Args:
            ref: Reference ID for 1+ Entries.
            date: Date of Entry.
            value: Value of Entry in pence.

        Returns:
            Entry

        """

        e = Entry(ref=ref, date=date, value=value)
        self.entries.add(e)
        return e

    def credit(self, ref: str, date: date, value: int) -> Entry:
        """Credit the Account.

        Creates a new Entry object and assoicates it with the Account.

        Args:
            ref: Reference ID for 1+ Entries.
            date: Date of Entry.
            value: Value of Entry in pence.

        Returns:
            Entry

        """

        e = Entry(ref=ref, date=date, value=value * -1)
        self.entries.add(e)
        return e
