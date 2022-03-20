from sqlalchemy import Table, MetaData, Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import mapper, relationship

from ledger import domain


metadata = MetaData()


ledgers = Table(
    "ledgers",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("name", String(255), unique=True, nullable=False),
)


entries = Table(
    "entries",
    metadata,
    Column("ref", String(255), primary_key=True),
    Column("account", String(255), primary_key=True),
    Column("date", Date, primary_key=True),
    Column("value", Integer, primary_key=True),
    Column("ledger_id", ForeignKey("ledgers.id")),
)


def start_mappers():
    entries_mapper = mapper(domain.Entry, entries)
    return mapper(
        domain.Ledger,
        ledgers,
        properties={
            "entries": relationship(
                entries_mapper,
                collection_class=set,
            )
        },
    )
