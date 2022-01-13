from decimal import Decimal
from enum import Enum, auto

from attrs import define


class Sign(Enum):
    D = auto()
    C = auto()


@define
class JournalEntry:
    sign: Sign
    amnt: Decimal

