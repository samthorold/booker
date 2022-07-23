from __future__ import annotations
from typing import Protocol

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session

from ledger import config, repository


class UnitOfWork(Protocol):
    """Unit of Work protocol."""

    ledgers: repository.Repository

    def __enter__(self) -> UnitOfWork:
        ...

    def __exit__(self, *args):
        ...

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
    """SQLAlchemy Unit of Work."""

    def __init__(self, session_factory=DEFAULT_SESSION_FACTORY):
        self.session_factory = session_factory

    def __enter__(self):
        self.session: Session = self.session_factory()
        self.ledgers: repository.Repository = repository.SQLAlchemyRepository(
            self.session
        )
        return self

    def __exit__(self, *args):
        self.rollback()
        self.session.close()

    def commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()
