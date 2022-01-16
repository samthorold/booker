from datetime import datetime as dt
from decimal import Decimal

from booker.core.journal_entry import JournalEntry, Sign


DATE = dt.fromisoformat("2022-01-01")


def test_add_journal_entry():
    je1 = JournalEntry(sign=Sign.D, amnt=Decimal("100"), date=DATE)
    je2 = JournalEntry(sign=Sign.D, amnt=Decimal("100"), date=DATE)
    assert je1 + je2 == JournalEntry(sign=Sign.D, amnt=Decimal("200"), date=DATE)

    je1 = JournalEntry(sign=Sign.D, amnt=Decimal("100"), date=DATE)
    je2 = JournalEntry(sign=Sign.C, amnt=Decimal("90"), date=DATE)
    assert je1 + je2 == JournalEntry(sign=Sign.D, amnt=Decimal("10"), date=DATE)

    je1 = JournalEntry(sign=Sign.D, amnt=Decimal("90"), date=DATE)
    je2 = JournalEntry(sign=Sign.C, amnt=Decimal("100"), date=DATE)
    assert je1 + je2 == JournalEntry(sign=Sign.C, amnt=Decimal("10"), date=DATE)
