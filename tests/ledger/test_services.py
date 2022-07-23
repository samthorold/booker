import pytest

from ledger import services
from ledger.uow import SqlAlchemyUnitOfWork


def test_add_and_list_ledgers(session_factory):
    name = "sales"
    uow = SqlAlchemyUnitOfWork(session_factory)
    with uow:
        _ = services.add_ledger(name, uow=uow)
        uow.commit()

    uow = SqlAlchemyUnitOfWork(session_factory)
    with uow:
        ledgers = services.ledgers(uow=uow)
        assert name in ledgers["ledgers"]


def test_cannot_add_duplicate_ledgers(session_factory):
    name = "sales"
    uow = SqlAlchemyUnitOfWork(session_factory)
    with uow:
        _ = services.add_ledger(name, uow=uow)
        uow.commit()

    uow = SqlAlchemyUnitOfWork(session_factory)

    with pytest.raises(services.DuplicateLedger):
        with uow:
            _ = services.add_ledger(name, uow=uow)
            uow.commit()

    uow = SqlAlchemyUnitOfWork(session_factory)
    with uow:
        ledgers = services.ledgers(uow=uow)
        assert name in ledgers["ledgers"]


def test_post_and_balance(session_factory):
    name = "sales"
    uow = SqlAlchemyUnitOfWork(session_factory)
    with uow:
        _ = services.add_ledger(name, uow=uow)
        uow.commit()

    ref = "ref"
    entries = [
        {"ref": ref, "account": "cash", "date": "2022-01-01", "value": 10},
        {"ref": ref, "account": "rev", "date": "2022-01-01", "value": -10},
    ]

    uow = SqlAlchemyUnitOfWork(session_factory)
    with uow:
        _ = services.post(
            name=name,
            entries=entries,
            uow=uow,
        )
        uow.commit()

    uow = SqlAlchemyUnitOfWork(session_factory)
    with uow:
        got = services.balance(name, "cash", "2099-01-01", uow)
        assert got["balance"] == 10
        got = services.balance(name, "rev", "2099-01-01", uow)
        assert got["balance"] == -10


def test_close(session_factory):
    uow = SqlAlchemyUnitOfWork(session_factory)
    with uow:
        _ = services.add_ledger("sales", uow=uow)
        _ = services.add_ledger("general", uow=uow)
        uow.commit()

    ref = "ref"
    entries = [
        {"ref": ref, "account": "cash", "date": "2022-01-01", "value": 10},
        {"ref": ref, "account": "rev", "date": "2022-01-01", "value": -10},
    ]

    uow = SqlAlchemyUnitOfWork(session_factory)
    with uow:
        _ = services.post(
            name="sales",
            entries=entries,
            uow=uow,
        )
        uow.commit()

    uow = SqlAlchemyUnitOfWork(session_factory)
    with uow:
        got = services.balance("sales", "cash", "2099-01-01", uow)
        assert got["balance"] == 10
        got = services.balance("sales", "rev", "2099-01-01", uow)
        assert got["balance"] == -10

    uow = SqlAlchemyUnitOfWork(session_factory)
    with uow:
        services.close(
            ref="close",
            child="sales",
            parent="general",
            date="2022-01-31",
            uow=uow,
        )

    uow = SqlAlchemyUnitOfWork(session_factory)
    with uow:
        got = services.balance("general", "cash", "2099-01-01", uow)
        assert got["balance"] == 10
        got = services.balance("general", "rev", "2099-01-01", uow)
        assert got["balance"] == -10
