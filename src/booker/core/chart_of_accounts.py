from attrs import define, Factory

from booker.core.account import Account, AccountType


@define(kw_only=True)
class ChartOfAccounts:
    accounts: dict[str, Account] = Factory(dict)

    def __len__(self):
        return len(self.accounts)

    def __iter__(self):
        return iter(self.accounts.values())

    def __getitem__(self, k):
        return self.accounts[k]

    def create_account(
        self, *, code: str, type: AccountType, name: str, description: str
    ) -> Account:
        a = Account(code=code, type=type, name=name, description=description)
        self.accounts[a.code] = a
        return a
