import uuid

import pytest
import requests

from ledger import config


@pytest.mark.usefixtures("postgres_db")
@pytest.mark.usefixtures("restart_api")
def test_add_and_list_ledgers():
    name = uuid.uuid4().hex
    data = {"name": name}

    url = config.get_api_url()

    r = requests.post(f"{url}/ledgers", json=data)
    assert r.status_code == 201, r.json()
    assert r.json()["name"] == name

    r = requests.get(f"{url}/ledgers")
    assert r.status_code == 200, r.json()
    assert name in r.json()["ledgers"]


@pytest.mark.usefixtures("postgres_db")
@pytest.mark.usefixtures("restart_api")
def test_cannot_duplicate_ledger_names():
    name = uuid.uuid4().hex
    data = {"name": name}

    url = config.get_api_url()

    r = requests.post(f"{url}/ledgers", json=data)
    assert r.status_code == 201, r.json()
    assert r.json()["name"] == name

    r = requests.post(f"{url}/ledgers", json=data)
    assert r.status_code == 400, r.json()


@pytest.mark.usefixtures("postgres_db")
@pytest.mark.usefixtures("restart_api")
def test_create_multiple_ledgers():
    names = [uuid.uuid4().hex for _ in range(2)]

    url = config.get_api_url()

    for name in names:
        data = {"name": name}
        _ = requests.post(f"{url}/ledgers", json=data)

    r = requests.get(f"{url}/ledgers")
    assert r.status_code == 200, r.json()
    data = r.json()
    assert all(name in data["ledgers"] for name in names)
