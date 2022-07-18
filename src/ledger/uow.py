from typing import Protocol

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session

from ledger import config, repository


class UnitOfWork(Protocol):
    ledgers: repository.Repository

    def __enter__(self) -> "UnitOfWork":
        return self

    def __exit__(self, *args):
        self.rollback()

    def commit(self):
        ...

    def rollback(self):
        ...


DEFAULT_SESSION_FACTORY = sessionmaker(
    bind=create_engine(
        config.get_postgres_uri(),
        isolation_level="REPEATABLE READ",
    )
)

class SqlAlchemyUnitOfWork:
    def __init__(self, session_factory=DEFAULT_SESSION_FACTORY):
        self.session_factory = session_factory

    def __enter__(self):
        self.session = self.session_factory()  # type: Session
        self.ledgers = repository.SQLAlchemyRepository(self.session)
        return self

    def __exit__(self, *args):
        self.session.rollback()
        self.session.close()

    def commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()
