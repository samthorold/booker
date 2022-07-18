from sqlalchemy import Table, Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship, registry

from ledger import domain


mapper_registry = registry()


ledgers = Table(
    "ledgers",
    mapper_registry.metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("name", String(255), unique=True, nullable=False),
)


entries = Table(
    "entries",
    mapper_registry.metadata,
    Column("ref", String(255), primary_key=True),
    Column("account", String(255), primary_key=True),
    Column("date", Date, primary_key=True),
    Column("value", Integer, primary_key=True),
    Column("ledger_id", ForeignKey("ledgers.id")),
)


def start_mappers():
    entries_mapper = mapper_registry.map_imperatively(domain.Entry, entries)
    mapper_registry.map_imperatively(
        domain.Ledger,
        ledgers,
        properties={
            "entries": relationship(
                entries_mapper,
                backref="ledger",
                collection_class=set,
            )
        },
    )
