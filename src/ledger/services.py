from datetime import date as date_cls
from typing import Any

from ledger import domain
from ledger import uow as unit_of_work


def add_ledger(name: str, uow: unit_of_work.UnitOfWork) -> dict[str, str]:
    with uow:
        ledger = domain.Ledger(name=name)
        uow.ledgers.add(ledger)
        uow.commit()
    return {"name": name}


def ledgers(uow: unit_of_work.UnitOfWork):
    with uow:
        ledgers = [l.name for l in uow.ledgers.list()]
    return {"ledgers": ledgers}


def post(
    name: str,
    entries: list[dict[str, Any]],
    uow: unit_of_work.UnitOfWork,
) -> dict[str, str | list[dict[str, Any]]]:
    with uow:
        ledger = uow.ledgers.get(name)
        entry_objs = set(domain.Entry.from_dict(entry) for entry in entries)
        posted_entries = [e.to_dict() for e in ledger.post(entry_objs)]
        uow.commit()
    return {
        "name": name,
        "posted_entries": posted_entries,
    }


def balance(
    name: str,
    account: str,
    date: str,
    uow: unit_of_work.UnitOfWork,
) -> dict[str, int | str]:
    with uow:
        ledger = uow.ledgers.get(name)
        date_ = date_cls.fromisoformat(date)
        bal = ledger.balance(account=account, date=date_)
    return {
        "name": name,
        "account": account,
        "date": date,
        "balance": bal,
    }


def close(
    ref: str,
    child: str,
    parent: str,
    date: str,
    uow: unit_of_work.UnitOfWork,
) -> dict[str, str | list[dict[str, Any]]]:
    with uow:
        child_ledger = uow.ledgers.get(child)
        parent_ledger = uow.ledgers.get(parent)
        date_ = date_cls.fromisoformat(date)
        posted_entries = [
            e.to_dict() for e in child_ledger.close_to(ref, parent_ledger, date_)
        ]
        uow.commit()
    return {
        "ref": ref,
        "child": child,
        "parent": parent,
        "date": date,
        "posted_entries": posted_entries,
    }
