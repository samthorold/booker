from flask import Flask, request

from ledger import domain, orm, services, uow

app = Flask(__name__)
orm.start_mappers()


@app.route("/ledgers", methods=["GET", "POST"])
def ledger():
    if request.method == "POST":
        name = services.add_ledger(
            uow=uow.SqlAlchemyUnitOfWork(),
            **request.json,
        )
        return {"name": name}, 201
    return services.ledgers(uow.SqlAlchemyUnitOfWork())


@app.route("/post", methods=["POST"])
def post():
    try:
        return services.post(
            request.json["name"],
            request.json["entries"],
            uow.SqlAlchemyUnitOfWork(),
        ), 201
    except domain.LedgerError as e:
        return {"message": str(e)}, 400


@app.route("/close", methods=["POST"])
def close():
    try:
        posted_entries = services.close(
            request.json["ref"],
            request.json["child"],
            request.json["parent"],
            request.json["date"],
            uow.SqlAlchemyUnitOfWork(),
        )
    except domain.LedgerError as e:
        return {"message": str(e)}, 400

    return [e.to_dict() for e in posted_entries], 201
