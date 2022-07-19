from datetime import date as date_cls
from typing import Any

from ledger import domain
from ledger import uow as unit_of_work


def add_ledger(name: str, uow: unit_of_work.UnitOfWork):
    with uow:
        ledger = domain.Ledger(name=name)
        uow.ledgers.add(ledger)
        uow.commit()
    return name


def ledgers(uow: unit_of_work.UnitOfWork):
    with uow:
        ledgers = [l.name for l in uow.ledgers.list()]
    return ledgers


def post(
    name: str,
    data: list[dict[str, Any]],
    uow: unit_of_work.UnitOfWork,
) -> tuple[dict[str, Any], ...]:
    with uow:
        ledger = uow.ledgers.get(name)
        entries = set(domain.Entry.from_dict(entry) for entry in data)
        posted_entries = tuple(e.to_dict() for e in ledger.post(entries))
        uow.commit()
    return posted_entries


def balance(
    name: str,
    account: str,
    date: str,
    uow: unit_of_work.UnitOfWork,
) -> int:
    with uow:
        ledger = uow.ledgers.get(name)
        date = date_cls.fromisoformat(date)
        bal = ledger.balance(account=account, date=date)
    return bal


def close(
    ref: str,
    child: str,
    parent: str,
    date: str,
    uow: unit_of_work.UnitOfWork,
) -> tuple[dict[str, Any], ...]:
    with uow:
        child_ledger = uow.ledgers.get(child)
        parent_ledger = uow.ledgers.get(parent)
        date_ = date_cls.fromisoformat(date)
        posted_entries = tuple(
            e.to_dict() for e in
            child_ledger.close_to(ref, parent_ledger, date_)
        )
        uow.commit()
    return posted_entries
