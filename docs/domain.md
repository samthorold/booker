# Domain

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
