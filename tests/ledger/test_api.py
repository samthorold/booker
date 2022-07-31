import uuid

import pytest
import requests

from ledger import config


@pytest.mark.e2e
@pytest.mark.usefixtures("postgres_db")
@pytest.mark.usefixtures("restart_api")
def test_add_and_list_ledgers():
    name = uuid.uuid4().hex
    data = {"name": name}

    url = config.get_api_url()

    r = requests.post(f"{url}/v1/ledgers", json=data)
    assert r.status_code == 201, r.json()
    assert r.json()["name"] == name

    r = requests.get(f"{url}/v1/ledgers")
    assert r.status_code == 200, r.json()
    assert name in r.json()["ledgers"]


@pytest.mark.e2e
@pytest.mark.usefixtures("postgres_db")
@pytest.mark.usefixtures("restart_api")
def test_cannot_add_duplicate_ledgers():
    name = uuid.uuid4().hex
    data = {"name": name}

    url = config.get_api_url()

    r = requests.post(f"{url}/v1/ledgers", json=data)
    assert r.status_code == 201, r.json()
    assert r.json()["name"] == name

    r = requests.post(f"{url}/v1/ledgers", json=data)
    assert r.status_code == 400, r.json()


@pytest.mark.e2e
@pytest.mark.usefixtures("postgres_db")
@pytest.mark.usefixtures("restart_api")
def test_create_multiple_ledgers():
    names = [uuid.uuid4().hex for _ in range(2)]

    url = config.get_api_url()

    for name in names:
        data = {"name": name}
        _ = requests.post(f"{url}/v1/ledgers", json=data)

    r = requests.get(f"{url}/v1/ledgers")
    assert r.status_code == 200, r.json()
    data = r.json()
    assert all(name in data["ledgers"] for name in names)


@pytest.mark.e2e
@pytest.mark.usefixtures("postgres_db")
@pytest.mark.usefixtures("restart_api")
def test_post_and_balance():
    name = uuid.uuid4().hex

    url = config.get_api_url()

    data = {"name": name}
    _ = requests.post(f"{url}/v1/ledgers", json=data)

    ref = "ref"
    entries = [
        {"ref": ref, "account": "cash", "date": "2022-01-01", "value": 10},
        {"ref": ref, "account": "rev", "date": "2022-01-01", "value": -10},
    ]
    data = {"name": name, "entries": entries}
    r = requests.post(f"{url}/v1/post", json=data)
    assert r.status_code == 201, r.json()
    data = r.json()
    assert len(data["posted_entries"]) == 2, data

    data = {
        "name": name,
        "account": "cash",
        "date": "2022-01-01",
    }
    r = requests.get(f"{url}/v1/balance", json=data)
    assert r.status_code == 200, r.json()
    assert r.json()["balance"] == 10, r.json()


@pytest.mark.e2e
@pytest.mark.usefixtures("postgres_db")
@pytest.mark.usefixtures("restart_api")
def test_close():
    child = uuid.uuid4().hex
    parent = uuid.uuid4().hex

    url = config.get_api_url()

    for name in [child, parent]:
        data = {"name": name}
        _ = requests.post(f"{url}/v1/ledgers", json=data)

    ref = uuid.uuid4().hex
    entries = [
        {"ref": ref, "account": "cash", "date": "2022-01-01", "value": 10},
        {"ref": ref, "account": "rev", "date": "2022-01-01", "value": -10},
    ]
    data = {"name": child, "entries": entries}
    _ = requests.post(f"{url}/v1/post", json=data)

    data = {
        "ref": uuid.uuid4().hex,
        "child": child,
        "parent": parent,
        "date": "2022-01-01",
    }
    r = requests.post(f"{url}/v1/close", json=data)
    print(r.json())
    assert r.status_code == 201, r.json()
    assert len(r.json()["posted_entries"]) == 2

    data = {
        "name": parent,
        "account": "cash",
        "date": "2022-01-01",
    }
    r = requests.get(f"{url}/v1/balance", json=data)
    assert r.status_code == 200, r.json()
    assert r.json()["balance"] == 10, r.json()

    data = {
        "name": child,
        "account": "cash",
        "date": "2022-01-01",
    }
    r = requests.get(f"{url}/v1/balance", json=data)
    assert r.json()["balance"] == 0, r.json()
