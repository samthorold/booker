from flask import Flask, request

import json

from ledger import domain, orm, services, uow

app = Flask(__name__)
orm.start_mappers()


@app.route("/ledgers", methods=["GET", "POST"])
def ledger():
    if request.method == "POST":
        assert request.json
        data = request.json
        name = data.pop("name")
        try:
            return (
                services.add_ledger(
                    uow=uow.SqlAlchemyUnitOfWork(),
                    name=name,
                    **data,
                ),
                201,
            )
        except domain.LedgerError as e:
            return {"message": str(e)}, 400
    return services.ledgers(uow=uow.SqlAlchemyUnitOfWork())


@app.route("/post", methods=["POST"])
def post():
    assert request.json
    data = request.json
    name = data.pop("name")
    entries = data.pop("entries")
    try:
        return (
            services.post(
                name=name,
                entries=entries,
                uow=uow.SqlAlchemyUnitOfWork(),
            ),
            201,
        )
    except domain.LedgerError as e:
        return {"message": str(e)}, 400


@app.route("/balance", methods=["GET"])
def balance():
    assert request.json
    data = request.json

    name = data.pop("name")
    account = data.pop("account")
    date = data.pop("date")
    try:
        return services.balance(
            name=name,
            account=account,
            date=date,
            uow=uow.SqlAlchemyUnitOfWork(),
        )
    except domain.LedgerError as e:
        return {"message": str(e)}, 400


@app.route("/close", methods=["POST"])
def close():
    assert request.json
    data = request.json
    ref = data.pop("ref")
    child = data.pop("child")
    parent = data.pop("parent")
    date = data.pop("date")
    try:
        return (
            services.close(
                ref=ref,
                child=child,
                parent=parent,
                date=date,
                uow=uow.SqlAlchemyUnitOfWork(),
            ),
            201,
        )
    except domain.LedgerError as e:
        return {"message": str(e)}, 400
