from datetime import datetime
from decimal import Decimal
from enum import Enum

from attrs import define, Factory

from booker.core.journal_entry import JournalEntry, Sign


class AccountType(Enum):
    ASSET = "ASSET"
    LIABILITY = "LIABILITY"
    CAPITAL = "CAPITAL"
    INCOME = "INCOME"
    EXPENSE = "EXPENSE"


@define(kw_only=True)
class Account:
    """Account.

    Attributes:
        code: Unique code.
        type: Account type; asset, liabilitity, capital, income, or expense
        name: Human-friendly name.
        description: Description of entries to be associated with the account.
        entries: JournalEntry objects associated with this Account.

    """

    code: str
    type: AccountType
    name: str
    description: str
    entries: list[JournalEntry] = Factory(list)

    def _je(
        self, sign: Sign, amount: str | Decimal, date: str | datetime | None = None
    ) -> JournalEntry:
        date = datetime.utcnow() if date is None else date
        je = JournalEntry(sign=sign, amnt=amount, date=date)
        self.entries.append(je)
        return je

    def dr(
        self, amount: str | Decimal, date: str | datetime | None = None
    ) -> JournalEntry:
        return self._je(sign=Sign.D, amount=amount, date=date)

    def cr(
        self, amount: str | Decimal, date: str | datetime | None = None
    ) -> JournalEntry:
        return self._je(sign=Sign.C, amount=amount, date=date)

    def balance(self):
        if self.entries:
            return sum(self.entries[1:], start=self.entries[0])
        return JournalEntry(sign=Sign.D, amnt=Decimal("0"), date=datetime.utcnow())
