# Domain

## Ubiquitous Language

### Bookkeeping

Bookkeeping is all about creating an accurate paper trial.

??? note "Accounting methods"

    Two accounting methods, cash and accrual.
    The difference is when sales and purchases are recorded.
    Cash-based accounting records sales and purchases when cash exchanges hands.
    Accrual-based accounting recourds sales and purchases when they happen.
    All but the smallest businesses use accrual-based accounting.

A business has three financial concepts that must be kept in balance;
assets, capital, and liabilities.
Assets = capital + liabilities.

Every `transaction` requires at least one `debit` and one `credit`.
This is double-entry bookkeeping.

The `chart of accounts` sets out all a business' `account`s and the types of
`transaction`s that go into each one.

"The books" or "the accounts" are a collection of `ledger`s.

A `ledger` records groups of `debit`s and `credit`s. For example,

- Sales `ledger`: customer accounts
- Purchase `ledger`: supplier accounts
- General `ledger`: ultimately, all business activities
- Bank `ledger`: bank account inflows and outflows

The information recorded in bookkeeping is ultimately used to create financial
statements.

The statement of financial position shows a snapshot in time of the value of
assets, capital, and liabilties.

The statements of financial performance shows a window of time of the value of
income and expenses.

Bookkeeping follows the accounting cycle over a period of time.

```mermaid
graph TB
  A[Transactions] --> B[Reconciliations]
  B --> C[Trial Balance]
  C --> D[Adjusted Journal Entries]
  D --> E[Financial Statements]
  E --> F[Closing Entries]
  F --> A
```

To "close" the accounts means to zero out all the income and expense accounts.

Different types of account have different "normal" balances.

| Account | Normal balance|
| --- | --- |
| Asset | Debit |
| Capital | Credit |
| Liability | Credit |
| Income | Credit |
| Expense | Debit |

A debit normal balance means debiting that account increases the value.

The `chart of accounts` records which types of `transaction`s should affect
which `account`s.
It is probably in a specific order and includes a description for each account.

`Account`s can be added during the period but not removed.

Chart of accounts columns;

- Number
- Name
- Type (Asset, Capital, Liability, Income, Expense)
- Description of the types of `transaction`s to be recorded in that `account`

Historically, splitting the act of entering debits and credits onto
separate ledgers kept things simpler.
Debits and credits relating to sales were all recorded in one place then
the total sales for the period was entered in the general ledger.

`Control account reconciliations` help to check the various ledgers are in
agreement.

For example, the debtors control account totals all the sales and customer
receipts for a period.
This may be compared to the aged debtors report.

Not all debits and credits are the result of explicit transactions such as a
sale.
For example, assets depreciate in value and prepaid expenses such as insurance
are used up with time.

### Periodic tasks

Certain tasks need completing on a daily, weekly, or monthly basis.
Besides the annual financial statement preparation.

Businesses use checklists to keep track of which tasks have been completed
for the period.

### Preparing financial statements


### Tax


### Reporting

For decision-making...

For external parties...

### Budgeting


## Bounded Contexts

The same words may have different meanings inside each context or system.

### Ledger system

Records accounts and their debits and credits.

Actions include

- Creating accounts
    - provided the account number / code is unique
- Deleting accounts
    - provided the account has a zero balance
- Posting debits and credits to ledger(s)
    - provided the transaction has a zero balance

Really, two contexts...

The chart of accounts system and the ledger system.

For the chart of accounts

    Account
        code
        name
        description
        balance to permit deleting the account
        (last closed)

For the ledger

    Entry
        ref
        account code
        date
        value

!!! tip

    For the purposes of the ledger system,
    the account number is taken as read.
    Some other system manages account management.

Ensures individual transactions balance and
debit/crediting an account is idempotent.

### Reporting system

Records groups of accounts.

Returns aggregate information - not concerned with debits and credits.

Includes control accounts and financial statements.

### Budgeting / Forecasting system

...

## Context Map



## Tactical - Entities, Values, and Aggregates

```mermaid
classDiagram
  Account "1" --o "0..n" Entry
  class Account{
    +str code
    +str name
    +set~Entry~ entries
    +balance() int
    +credit(ref, date, value) Entry
    +debit(ref, date, value) Entry
  }
  class Entry{
    +str ref
    +date date
    +Int value
  }
```

???+ note "Debits, credit, and decimals"

    Debit and credit amounts are represented as positve and negative values
    respectively, while money amounts are in pence to avoid floating point
    number issues.
