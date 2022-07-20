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
        assert name in ledgers


def test_post_and_balance(session_factory):
    name = "sales"
    uow = SqlAlchemyUnitOfWork(session_factory)
    with uow:
        _ = services.add_ledger(name, uow=uow)
        uow.commit()

    ref = "ref"
    data = [
        {"ref": ref, "account": "cash", "date": "2022-01-01", "value": 10},
        {"ref": ref, "account": "rev", "date": "2022-01-01", "value": -10},
    ]

    uow = SqlAlchemyUnitOfWork(session_factory)
    with uow:
        _ = services.post(
            name=name,
            data=data,
            uow=uow,
        )
        uow.commit()

    uow = SqlAlchemyUnitOfWork(session_factory)
    with uow:
        assert services.balance(name, "cash", "2099-01-01", uow) == 10
        assert services.balance(name, "rev", "2099-01-01", uow) == -10


def test_close(session_factory):
    uow = SqlAlchemyUnitOfWork(session_factory)
    with uow:
        _ = services.add_ledger("sales", uow=uow)
        _ = services.add_ledger("general", uow=uow)
        uow.commit()

    ref = "ref"
    data = [
        {"ref": ref, "account": "cash", "date": "2022-01-01", "value": 10},
        {"ref": ref, "account": "rev", "date": "2022-01-01", "value": -10},
    ]

    uow = SqlAlchemyUnitOfWork(session_factory)
    with uow:
        _ = services.post(
            name="sales",
            data=data,
            uow=uow,
        )
        uow.commit()

    uow = SqlAlchemyUnitOfWork(session_factory)
    with uow:
        assert services.balance("sales", "cash", "2099-01-01", uow) == 10
        assert services.balance("sales", "rev", "2099-01-01", uow) == -10

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
        assert services.balance("general", "cash", "2099-01-01", uow) == 10
        assert services.balance("general", "rev", "2099-01-01", uow) == -10
