import pytest
import requests

from ledger import config


@pytest.mark.e2e
@pytest.mark.usefixtures("postgres_db")
@pytest.mark.usefixtures("restart_api")
def test_create_ledger_and_get_list():
    name = "sales"
    data = {"name": name}

    url = config.get_api_url()

    r = requests.post(f"{url}/ledgers", json=data)

    assert r.status_code == 201
    assert r.json()["name"] == name

    r = requests.get(f"{url}/ledgers")
    assert r.status_code == 200
    assert name in r.json()["ledgers"]


@pytest.mark.e2e
@pytest.mark.usefixtures("postgres_db")
@pytest.mark.usefixtures("restart_api")
def test_create_multiple_ledgers():
    names = ["sales", "general"]

    url = config.get_api_url()

    for name in names:
        data = {"name": name}
        _ = requests.post(f"{url}/ledgers", json=data)

    r = requests.get(f"{url}/ledgers")
    assert r.status_code == 200
    data = r.json()
    assert all(name in data["ledgers"] for name in names)
