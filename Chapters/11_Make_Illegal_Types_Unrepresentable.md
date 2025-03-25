# Make Illegal Types Unrepresentable

A common strategy for preventing problems is to check values after arguments are passed to functions.
This spreads validation code across functions, producing maintenance problems.
This chapter moves validation into custom types that make invalid data impossible.
In addition, data is checked when you create an instance, rather than when data is passed to a function.
With this approach, you:

1. Discover problems sooner.
1. Clarify the meaning of your code.
1. Share custom type benefits across all functions that use those types.
1. Eliminate duplicate validation checks and their associated maintenance.
1. Make changes easier by localizing validation to a single point.
1. Eliminate the need for techniques such as Design By Contract (DBC).
1. Enable more focused testing with finer granularity.

## "Stringly Typed"

Years ago I came across some research looking at the way generic components like `List`, `Set` and `Map` were being used in Java.
Only a tiny percentage of the code reviewed used anything *except* strings as type parameters.
This study suggested that the vast majority of systems were using strings as their primary data type.

Because you can put any characters in any format into a string, such "stringly typed" systems (an ironic play on "strongly typed") may be the worst of all possible worlds.
Unless it's actually text, classifying something as a string says virtually nothing about it.
When a function receives a string that is meant to represent a type, that function can assume precisely nothing about it.
Every such function must start from scratch and analyze that string to see if it conforms to what that function needs.

If you ever change the meaning of that stringly-typed item, you have a daunting job ahead of you: to look through every function that uses it and ensure that your change is reflected in the validations in every single function.

[[Stringly typed example, possibly telephone numbers]]

## Design by Contract

The argument-validation problem was observed by Bertrand Meyer and introduced as a core concept in his Eiffel programming language, described in the book *Object-Oriented Software Construction* (1988).
*Design By Contract* (DbC) tried to reduce errors by treating the interaction between software components as a formal agreement:

- Preconditions: What must be true before a function/method runs.
- Postconditions: What must be true after the function completes.
- Invariants: What must always be true about the object state.

Eiffel provided explicit keywords to make DbC a first-class citizen in the language:

| Keyword     | Purpose                |
|-------------|------------------------|
| `require`   | Preconditions          |
| `ensure`    | Postconditions         |
| `invariant` | Class-wide conditions  |
| `old`       | Refers to previous state in postconditions |

The idea was that each function you wrote would use these to ensure the correctness of the inputs and outputs of that function.
In particular, `require` typically checks the argument values for correctness.
For preconditions in Python, we can create a `requires` decorator to check argument values:

```python
# require.py
from typing import Callable, NamedTuple
from functools import wraps


class Condition(NamedTuple):
    check: Callable[..., bool]
    message: str


def requires(*conditions: Condition):
    def decorator(func: Callable):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for condition in conditions:
                if not condition.check(*args, **kwargs):
                    raise ValueError(condition.message)
            return func(*args, **kwargs)
        return wrapper
    return decorator
```

Now we can apply `require` to validate function arguments:

```python
# bank_account.py
from dataclasses import dataclass
from decimal import Decimal
from require import requires, Condition

POSITIVE_AMOUNT = Condition(
    check=lambda self, amount: amount > Decimal("0"),
    message="Amount must be positive"
)

SUFFICIENT_BALANCE = Condition(
    check=lambda self, amount: self.balance >= amount,
    message="Insufficient balance"
)

@dataclass
class BankAccount:
    balance: Decimal

    @requires(POSITIVE_AMOUNT, SUFFICIENT_BALANCE)
    def withdraw(self, amount: Decimal) -> None:
        self.balance -= amount
        print(f"Withdrew {amount}, new balance: {self.balance}")

    @requires(POSITIVE_AMOUNT)
    def deposit(self, amount: Decimal) -> None:
        self.balance += amount
        print(f"Deposited {amount}, new balance: {self.balance}")


account = BankAccount(Decimal("100"))
account.deposit(Decimal("50"))
## Deposited 50, new balance: 150
account.withdraw(Decimal("30"))
## Withdrew 30, new balance: 120

try:
    account.withdraw(Decimal("200"))
except Exception as e:
    print(f"Error: {e}")
## Error: Insufficient balance

try:
    account.deposit(Decimal("-10"))
except Exception as e:
    print(f"Error: {e}")
## Error: Amount must be positive
```

This is an improvement over placing the testing code at the beginning of each function, as Eiffel does and as traditional Python functions do--assuming they test their arguments.
The `@require` clearly shows that constraints have been placed on the arguments.
`Condition` reduces duplicated code.

DbC definitely helps, but it has limitations:

1. A programmer can forget to use `requires`, or simply choose to perform argument checks by hand if DbC doesn't make sense to them.
1. The tests are spread throughout your system. Using `Condition` centralizes the test logic but making changes still risks missing updates on functions.

## Centralizing Validation into Custom Types

Instead of DbC, we can encode our validations into custom types.
This way, incorrect objects of those types cannot successfully be created:

```python
# typed_bank_account.py
from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True)
class Amount:
    value: Decimal

    def __init__(self, value: int | float | str | Decimal) -> None:
        decimal_value = Decimal(str(value))
        if decimal_value < Decimal("0"):
            raise ValueError(f"Amount cannot be negative, got {decimal_value}")
        object.__setattr__(self, "value", decimal_value)

    def __add__(self, other: "Amount") -> "Amount":
        return Amount(self.value + other.value)

    def __sub__(self, other: "Amount") -> "Amount":
        return Amount(self.value - other.value)


@dataclass(frozen=True)
class Balance:
    amount: Amount

    def deposit(self, deposit_amount: Amount) -> "Balance":
        return Balance(self.amount + deposit_amount)

    def withdraw(self, withdrawal_amount: Amount) -> "Balance":
        return Balance(self.amount - withdrawal_amount)


@dataclass
class BankAccount:
    balance: Balance

    def deposit(self, amount: Amount) -> None:
        self.balance = self.balance.deposit(amount)
        print(f"Deposited {amount.value}, balance: {self.balance.amount.value}")

    def withdraw(self, amount: Amount) -> None:
        self.balance = self.balance.withdraw(amount)
        print(f"Withdrew {amount.value}, balance: {self.balance.amount.value}")


account = BankAccount(Balance(Amount(100)))
account.deposit(Amount(50))
## Deposited 50, balance: 150
account.withdraw(Amount(30))
## Withdrew 30, balance: 120

try:
    account.withdraw(Amount(200))  # Too much
except ValueError as e:
    print(f"Error: {e}")
## Error: Amount cannot be negative, got -80

try:
    account.deposit(Amount(-10))  # Invalid amount
except ValueError as e:
    print(f"Error: {e}")
## Error: Amount cannot be negative, got -10
```
