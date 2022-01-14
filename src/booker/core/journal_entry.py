from decimal import Decimal
from enum import Enum, auto

from attrs import define


class Sign(Enum):
    D = "D"
    C = "C"


@define
class JournalEntry:
    sign: Sign
    amnt: Decimal

    def __add__(self, other: "JournalEntry"):
        l = self.amnt * (1 if self.sign == Sign.D else -1)
        r = other.amnt * (1 if other.sign == Sign.D else -1)
        amnt = l + r
        sign = Sign.D if amnt > 0 else Sign.C
        return JournalEntry(sign=sign, amnt=abs(amnt))
 
