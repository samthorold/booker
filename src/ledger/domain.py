from dataclasses import dataclass
from datetime import date


@dataclass(frozen=True)
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
    date: date
    value: int


class LedgerError(Exception):
    """Ledger domain base Exception."""


class PostingError(LedgerError):
    """PostingError base Exception."""


class TransactionDoesNotBalance(PostingError):
    """The entries do not balance."""


class NoSuchAccount(LedgerError):
    """No such account code in the ledger.

    As opposed to, say, an account with zero balance.
    """


class Ledger:
    """Ledger.

    Args:
        entries: Entry objects associated with the Ledger.

    """

    def __init__(self, entries: set[Entry] | None = None) -> None:
        self.entries: set[Entry] = set() if entries is None else entries

    def post(self, entries: set[Entry]) -> set[Entry]:
        """Post entries to the ledger.

        Args:
            entries: Entry objects to post

        Raises:
            TransactionDoesNotBalance: The entries do not balance.

        Returns:
            The entries passed in.

        """

        if sum(e.value for e in entries) != 0:
            raise PostingError("Entries do not balance")

        self.entries = self.entries | entries

        return entries

    def balance(self, account: str) -> int:
        """Get the balance for an account code.

        Args:
            account: Account code.

        Raises:
            NoSuchAccount: No corresponding account code in the ledger.

        Returns:
            Sum of the entries for the corresponding account.

        """
        entries = set(e for e in self.entries if e.account == account)
        if not entries:
            raise NoSuchAccount
        return sum(e.value for e in entries)
