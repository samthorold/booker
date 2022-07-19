from datetime import date as date_cls

import pytest

from ledger import domain
from ledger.uow import SqlAlchemyUnitOfWork


def insert_ledger_and_entries(session, name, ref, date, accounts, values):
    session.execute(
        "INSERT INTO ledgers (name, version)" " VALUES (:name, :version)",
        dict(name=name, version=1),
    )
    for account, value in zip(accounts, values):
        session.execute(
            "INSERT INTO entries (ref, account, date, value, ledger_id)"
            " VALUES (:ref, :account, :date, :value, :ledger_id)",
            dict(ref=ref, account=account, date=date, value=value, ledger_id=1),
        )


YESTERDAY = date_cls(2021, 12, 31)
TODAY = date_cls(2022, 1, 1)
TOMORROW = date_cls(2022, 1, 2)


# really a test of the orm
def test_insert_ledger_and_entries(session):
    insert_ledger_and_entries(
        session,
        "sales",
        "ref",
        TODAY,
        ("sales", "cash"),
        (-100, 100),
    )


def test_insert_ledger_with_repo(session_factory):
    name = "sales"
    uow = SqlAlchemyUnitOfWork(session_factory)
    with uow:
        uow.ledgers.add(domain.Ledger(name))
        uow.commit()
    new_session = session_factory()
    rows = list(new_session.execute('SELECT name FROM "ledgers"'))
    assert rows == [(name,)]


def test_get_ledger_and_entries(session_factory):

    name = "sales"

    session = session_factory()
    insert_ledger_and_entries(
        session,
        name,
        "ref",
        TODAY,
        ("sales", "cash"),
        (-100, 100),
    )
    session.commit()

    uow = SqlAlchemyUnitOfWork(session_factory)
    with uow:
        sales_ledger = uow.ledgers.get(name)
        assert sales_ledger.name == name
        assert len(sales_ledger.entries) == 2, sales_ledger.entries

        all_sales_ledgers = uow.ledgers.list()
        assert len(all_sales_ledgers) == 1


def test_account_balance(session_factory):

    name = "sales"

    session = session_factory()
    insert_ledger_and_entries(
        session,
        name,
        "ref",
        TODAY,
        ("sales", "cash"),
        (-100, 100),
    )
    session.commit()

    uow = SqlAlchemyUnitOfWork(session_factory)
    with uow:
        sales_ledger = uow.ledgers.get(name)
        assert sales_ledger.name == name
        assert sales_ledger.balance("sales", TODAY) == -100
        assert sales_ledger.balance("cash", TODAY) == 100


def test_rolls_back_uncommitted_work_by_default(session_factory):
    uow = SqlAlchemyUnitOfWork(session_factory)
    with uow:
        insert_ledger_and_entries(
            uow.session,
            "sales",
            "ref",
            TODAY,
            ("sales", "cash"),
            (-100, 100),
        )

    new_session = session_factory()
    rows = list(new_session.execute('SELECT * FROM "ledgers"'))
    assert rows == []
    rows = list(new_session.execute('SELECT * FROM "entries"'))
    assert rows == []


def test_commit(session_factory):
    uow = SqlAlchemyUnitOfWork(session_factory)
    with uow:
        insert_ledger_and_entries(
            uow.session,
            "sales",
            "ref",
            TODAY,
            ("sales", "cash"),
            (-100, 100),
        )
        uow.commit()

    new_session = session_factory()
    rows = list(new_session.execute('SELECT * FROM "ledgers"'))
    assert len(rows) == 1
    rows = list(new_session.execute('SELECT * FROM "entries"'))
    assert len(rows) == 2


def test_rolls_back_on_error(session_factory):
    class MyException(Exception):
        pass

    uow = SqlAlchemyUnitOfWork(session_factory)
    with pytest.raises(MyException):
        with uow:
            insert_ledger_and_entries(
                uow.session,
                "sales",
                "ref",
                TODAY,
                ("sales", "cash"),
                (-100, 100),
            )
            raise MyException()

    new_session = session_factory()
    rows = list(new_session.execute('SELECT * FROM "ledgers"'))
    assert rows == []
    rows = list(new_session.execute('SELECT * FROM "entries"'))
    assert rows == []
