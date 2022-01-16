from datetime import datetime as dt
from decimal import Decimal

from booker.core.account import Account
from booker.core.journal_entry import JournalEntry, Sign


def test_acount_balance():
    acct = Account(code="1", name="a", entries=[])
    _ = acct.dr("100.00")
    _ = acct.dr("100.00")
    _ = acct.cr("5")

    got = acct.balance()
    want = JournalEntry(sign=Sign.D, amnt=Decimal("195"), date=dt.utcnow())

    assert got.sign == want.sign and got.amnt == want.amnt
