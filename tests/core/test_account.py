from decimal import Decimal

from booker.core.account import Account
from booker.core.journal_entry import JournalEntry, Sign


def test_journal_entry():
    acct = Account(code="1", name="a", entries=[])
    etry = acct.journal_entry(sign="D", amount="100.00")

    assert etry.sign == Sign.D
    assert etry.amnt == Decimal("100")


def test_acount_balance():
    acct = Account(code="1", name="a", entries=[])
    _ = acct.journal_entry("D", amount="100.00")
    _ = acct.journal_entry("D", amount="100.00")
    _ = acct.journal_entry("C", amount="5")

    assert acct.balance() == JournalEntry(Sign.D, Decimal("195"))

