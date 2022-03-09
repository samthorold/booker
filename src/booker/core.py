from dataclasses import dataclass, field
from datetime import date
from enum import Enum


class Sign(Enum):
    DEBIT = 1
    CREDIT = -1


@dataclass(kw_only=True, frozen=True)
class Entry:
    ref: str
    date: date
    sign: Sign
    amount: int  # pence


@dataclass(kw_only=True)
class Account:
    code: str
    name: str
    entries: set[Entry] = field(default_factory=set)
