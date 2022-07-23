from typing import Iterable, Protocol

from sqlalchemy.orm.session import Session

from ledger.domain import Ledger


class Repository(Protocol):
    """Repository protocol"""

    session: Session

    def add(self, ledger: Ledger) -> None:
        ...

    def get(self, name: str) -> Ledger:
        ...

    def list(self) -> Iterable[Ledger]:
        ...


class SQLAlchemyRepository:
    """SQLAlchemyRepository"""

    def __init__(self, session: Session):
        self.session = session

    def add(self, ledger: Ledger) -> None:
        self.session.add(ledger)

    def get(self, name: str) -> Ledger:
        return self.session.query(Ledger).filter_by(name=name).one()

    def list(self) -> Iterable[Ledger]:
        return self.session.query(Ledger).all()
