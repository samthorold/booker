from datetime import date as date_cls

from ledger import domain
from ledger import uow as unit_of_work


class InvalidSku(Exception):
    pass


def add_ledger(name: str, uow: unit_of_work.UnitOfWork):
    with uow:
        uow.ledgers.add(domain.Ledger(name))
        uow.commit()
    return name


def ledgers(uow: unit_of_work.UnitOfWork):
    with uow:
        ledgers = uow.ledgers.list()
    return [ledger.name for ledger in ledgers]


def post(
    name: str,
    data: dict,
    uow: unit_of_work.UnitOfWork,
) -> set[domain.Entry]:
    with uow:
        ledger = uow.ledgers.get(name)
        entries = set(domain.Entry.from_dict(entry) for entry in data)
        posted_entries = ledger.post(entries)
        uow.commit()
    return posted_entries


def close(
    ref: str,
    child: str,
    parent: str,
    date_tpl: tuple[int, int, int],
    uow: unit_of_work.UnitOfWork,
) -> set[domain.Entry]:
    date = date_cls(*date_tpl)
    with uow:
        child_ledger = uow.ledgers.get(child)
        parent_ledger = uow.ledgers.get(parent)
        posted_entries = child_ledger.close_to(ref, parent_ledger, date)
        uow.commit()
    return posted_entries
