

def insert_ledger_and_entries(session, name, ref, date, accounts, values):
    session.execute(
        "INSERT INTO ledgers (name, version)"
        " VALUES (:name, :version)",
        dict(name=name, version=1),
    )
    for account, value in zip(accounts, values):
        session.execute(
            "INSERT INTO entries (ref, account, date, value)"
            " VALUES (:ref, :account, :date, :value)",
            dict(ref=ref, account=account, date=date, value=value),
        )


def test_insert_ledger_and_entries(session):
    insert_ledger_and_entries(
        session,
        "sales",
        "ref",
        "2022-06-01",
        ("sales", "cash"),
        (-100, 100),
    )
