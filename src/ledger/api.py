# pyright: reportOptionalSubscript=false

# flask.request.json return type is optional and pyright gets upset
# when indexing e.g. request.json["name"]

from flask import Flask, request

from ledger import domain, orm, services, uow

app = Flask(__name__)
orm.start_mappers()


@app.route("/ledgers", methods=["GET", "POST"])
def ledger():
    if request.method == "POST":
        name = services.add_ledger(request.json["name"], uow.SqlAlchemyUnitOfWork())
        return name, 201
    return services.ledgers(uow.SqlAlchemyUnitOfWork())


@app.route("/post", methods=["POST"])
def post():
    try:
        posted_entries = services.post(
            request.json["name"],
            request.json["entries"],
            uow.SqlAlchemyUnitOfWork(),
        )
    except domain.LedgerError as e:
        return {"message": str(e)}, 400

    return [e.to_dict() for e in posted_entries], 201


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
