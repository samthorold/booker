from datetime import date as date_cls

from ledger.uow import SqlAlchemyUnitOfWork


def insert_ledger_and_entries(session, name, ref, date, accounts, values):
    session.execute(
        "INSERT INTO ledgers (name, version)"
        " VALUES (:name, :version)",
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


def test_insert_ledger_and_entries(session):
    insert_ledger_and_entries(
        session,
        "sales",
        "ref",
        TODAY,
        ("sales", "cash"),
        (-100, 100),
    )


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