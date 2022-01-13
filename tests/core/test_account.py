from decimal import Decimal

from booker.core.account import Account
from booker.core.journal_entry import Sign


def test_journal_entry():
    acct = Account(code="1", name="a", entries=[])
    etry = acct.journal_entry(sign=Sign.D, amount="100.00")

    assert etry.sign == Sign.D
    assert etry.amnt == Decimal("100")

