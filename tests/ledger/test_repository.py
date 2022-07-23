from ledger.repository import Repository, SQLAlchemyRepository


def test_types(session):
    repo: Repository = SQLAlchemyRepository(session)
