from decimal import Decimal

from attrs import define, Factory

from booker.core.journal_entry import JournalEntry, Sign


@define(kw_only=True)
class Account:
    """Account.

    Attributes:
        code: Unique code.
        name: Human-friendly name.

    Examples:
    >>> a = Account(code="1", name="Assets")
    >>> a.code
    '1'
    >>> a.name
    'Assets'

    """

    code: str
    name: str
    entries: list[JournalEntry] = Factory(list)

    def journal_entry(self, sign: Sign | str, amount: Decimal | str) -> JournalEntry:
        je = JournalEntry(sign=Sign(sign), amnt=Decimal(amount))
        self.entries.append(je)
        return je

    def balance(self):
        if self.entries:
            return sum(self.entries[1:], start=self.entries[0])
        return JournalEntry(sign=Sign.D, amnt=Decimal("0"))

