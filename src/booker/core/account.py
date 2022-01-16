from datetime import datetime
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

    def _je(
        self, sign: Sign, amount: Decimal, date: datetime | None = None
    ) -> JournalEntry:
        date = datetime.utcnow() if date is None else date
        je = JournalEntry(sign=sign, amnt=amount, date=date)
        self.entries.append(je)
        return je

    def dr(self, amount: Decimal, date: datetime | None = None) -> JournalEntry:
        return self._je(sign=Sign.D, amount=amount, date=date)

    def cr(self, amount: Decimal, date: datetime | None = None) -> JournalEntry:
        return self._je(sign=Sign.C, amount=amount, date=date)

    def balance(self):
        if self.entries:
            return sum(self.entries[1:], start=self.entries[0])
        return JournalEntry(sign=Sign.D, amnt=Decimal("0"), date=datetime.utcnow())
