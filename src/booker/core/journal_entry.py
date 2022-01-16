from datetime import datetime
from decimal import Decimal
from enum import Enum

from attrs import define, field


class Sign(Enum):
    """

    Examples
    >>> list(Sign)
    [<Sign.D: 1>, <Sign.C: -1>]
    """

    D = 1
    C = -1


def convert_sign(obj: str | Sign) -> Sign:
    """

    Exmaples
    >>> convert_sign("D")
    <Sign.D: 1>
    >>> convert_sign(-1)
    <Sign.C: -1>
    >>> convert_sign("James Milner")
    Traceback (most recent call last):
    ...
    ValueError: ...
    """
    if isinstance(obj, str):
        if obj.lower().startswith("d"):
            return Sign.D
        if obj.lower().startswith("c"):
            return Sign.C
        raise ValueError(f"Cannot convert {obj} to Sign")
    try:
        return Sign(obj)
    except Exception as e:
        raise ValueError(f"Cannot convert {obj} to sign") from e


def convert_datetime(obj: str | datetime) -> datetime:
    """

    Examples
    >>> from datetime import datetime as dt
    >>> convert_datetime(dt(2022, 1, 1))
    datetime.datetime(2022, 1, 1, 0, 0)
    >>> convert_datetime("2022-01-01")
    datetime.datetime(2022, 1, 1, 0, 0)
    >>> convert_datetime("2022")
    Traceback (most recent call last):
    ...
    ValueError: ...
    """
    if isinstance(obj, str):
        try:
            return datetime.fromisoformat(obj)
        except Exception as e:
            raise ValueError(
                f"Cannot convert {obj} to datetime (must be ISO format)"
            ) from e
    if isinstance(obj, datetime):
        return obj
    raise ValueError(f"{obj} must be str or datetime object")


def convert_decimal(obj: str | int | float | Decimal) -> Decimal:
    """

    Examples
    >>> from decimal import Decimal
    >>> convert_decimal("100")
    Decimal('100')
    >>> convert_decimal("100") == convert_decimal(100)
    True
    >>> convert_decimal("100") == convert_decimal(100.0)
    True
    >>> convert_decimal(Decimal("100")) == convert_decimal(100.0)
    True
    """
    try:
        return Decimal(obj)
    except Exception as e:
        raise ValueError(f"Cannot convert {obj} to Decimal") from e


@define
class JournalEntry:
    """

    Examples
    >>> JournalEntry(sign="D", amnt=100, date="2022-01-01")
    JournalEntry(sign=<Sign.D: 1>, amnt=Decimal('100'), date=datetime.datetime(2022, 1, 1, 0, 0))
    """

    sign: Sign = field(converter=convert_sign)
    amnt: Decimal = field(converter=convert_decimal)
    date: datetime = field(converter=convert_datetime)

    def __add__(self, other: "JournalEntry"):
        amnt = self.amnt * self.sign.value + other.amnt * other.sign.value
        sign = Sign.D if amnt > 0 else Sign.C
        date = self.date if self.date > other.date else other.date
        return JournalEntry(sign=sign, amnt=abs(amnt), date=date)
