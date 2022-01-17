from booker.core.chart_of_accounts import ChartOfAccounts


def test_create_account():
    coa = ChartOfAccounts()
    a = coa.create_account(code="1", type="ASSET", name="a", description="Long para")

    assert len(coa) == 1
    assert a in coa

    assert a.code == "1"
    assert a.name == "a"

    assert coa[a.code] == a
