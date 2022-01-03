from attrs import define

@define
class Account:
    """Account.

    Attributes:
        code: Unique code.
        name: Human-friendly name.

    Examples:
    >>> a = Account(code="1", name="Assets")
    >>> a.code
    '1'
    >>> a.name
    'Assets'

    """
    code: str
    name: str

