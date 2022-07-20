import pytest
import requests

from ledger import config


@pytest.mark.postgres
@pytest.mark.usefixtures("postgres_db")
@pytest.mark.usefixtures("restart_api")
def test_create_ledger():
    name = "sales"
    data = {"name": name}

    url = config.get_api_url()
    r = requests.post(f"{url}/ledgers", json=data)

    assert r.status_code == 201
    assert r.json()["name"] == name
