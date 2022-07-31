from flask import Flask

import json

from ledger import orm, routes


def create_app():
    app = Flask(__name__)
    app.register_blueprint(routes.v1, url_prefix="/v1")
    orm.start_mappers()
    return app

