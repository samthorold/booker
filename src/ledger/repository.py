from typing import Iterable, Protocol

from ledger.domain import Ledger


class Repository(Protocol):
    def add(self, ledger: Ledger) -> None:
        ...

    def get(self, name: str) -> Ledger:
        ...

    def list(self) -> Iterable[Ledger]:
        ...


class SQLAlchemyRepository:
    def __init__(self, session):
        self.session = session

    def add(self, ledger: Ledger) -> None:
        self.session.add(ledger)

    def get(self, name: str) -> Ledger:
        return self.session.query(Ledger).filter_by(name=name).first()

    def list(self) -> Iterable[Ledger]:
        return self.session.query(Ledger).all()
