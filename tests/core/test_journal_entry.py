from decimal import Decimal

from booker.core.journal_entry import JournalEntry, Sign


def test_add_journal_entry():
    je1 = JournalEntry(sign=Sign.D, amnt=Decimal("100"))
    je2 = JournalEntry(sign=Sign.D, amnt=Decimal("100"))
    assert je1 + je2 == JournalEntry(sign=Sign.D, amnt=Decimal("200"))

    je1 = JournalEntry(sign=Sign.D, amnt=Decimal("100"))
    je2 = JournalEntry(sign=Sign.C, amnt=Decimal("90"))
    assert je1 + je2 == JournalEntry(sign=Sign.D, amnt=Decimal("10"))

    je1 = JournalEntry(sign=Sign.D, amnt=Decimal("90"))
    je2 = JournalEntry(sign=Sign.C, amnt=Decimal("100"))
    assert je1 + je2 == JournalEntry(sign=Sign.C, amnt=Decimal("10"))

