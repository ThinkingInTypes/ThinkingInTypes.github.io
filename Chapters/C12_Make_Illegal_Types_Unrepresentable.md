# Make Illegal Types Unrepresentable

A common strategy for preventing problems is to validate function arguments.
This spreads validation code across functions, producing maintenance problems.
This chapter moves validation into custom types that make invalid arguments impossible.
In addition, data is checked when you create an instance, rather than when data is passed to a function.
This approach:

1. Discovers problems sooner.
2. Clarifies the meaning of code.
3. Shares custom type benefits across all functions that use those types.
4. Eliminates duplicate validation checks and their associated maintenance.
5. Makes changes easier by localizing validation to a single point.
6. Eliminates the need for techniques such as Design By Contract (DBC).
7. Enables more focused testing with finer granularity.
8. Helps produce Domain-Driven Design.

## "Stringly Typed"

Years ago I came across some research looking at the way generic components like `List`, `Set` and `Map` were used in Java.
Only a tiny percentage of the code reviewed used anything _except_ strings as type parameters.
This study suggested that the vast majority of systems were using strings as their primary data type.

Because you can put any characters in any format into a string, such "stringly typed" systems
(an ironic play on "strongly typed") may be the worst of all possible worlds.
Unless it's text, classifying something as a string doesn't tell you anything.
When a function receives a string meant to represent a type, that function can assume precisely nothing about it.
Every such function must start from scratch and analyze that string to see if it conforms to what that function needs.

Changing the meaning of a stringly-typed item is a daunting job.
You must hunt through your code base and ensure that your change is reflected in the validations in every single function.
Because the logic is distributed, it's highly likely you will miss some.

Consider representing phone numbers as strings.
Here are some formats you might encounter:

```python
# string_phone_numbers.py
# Some problematic formats
phone_numbers: list[str] = [
    "5551234",  # No formatting – unclear area code
    "555-1234",  # US format, but without area code
    "(555) 123-4567",  # US format with punctuation
    "555.123.4567",  # Inconsistent punctuation
    "+1-555-123-4567",  # International format
    "+44 20 7946 0958",  # UK format – space-separated
    "5551234567",  # No formatting at all
    "555 1234",  # Ambiguous – local format?
    "555-12ab",  # Invalid characters
    "CallMeMaybe",  # Completely invalid
    "01234",  # Leading zero – looks like a zip code
    "",  # Empty string
    " 5551234 ",  # Whitespace issues
]
```

Any function that takes a phone number as a string must first validate that argument.
Here's a common but awkward approach:

```python
# phone_number_functions.py
import re


def f1(phone: str):
    valid = re.compile(
        r"^\+?(\d{1,3})?[\s\-.()]*([\d\s\-.()]+)$"
    )
    if not valid.match(phone):
        print(f"Error {phone = }")
        return
    ...


def f2(phone_num: str):
    check = re.compile(
        r"^\+?(\d{1,3})?[\s\-.()]*([\d\s\-.()]+)$"
    )
    assert check.match(phone_num), f"Invalid {phone_num}"
    ...


def f3(phonenumber: str):
    phone_number = re.compile(
        r"^\+?(\d{1,3})?[\s\-.()]*([\d\s\-.()]+)$"
    )
    if not phone_number.match(phonenumber):
        return f"Bad {phonenumber = }"
    ...
```

Each function has its own custom code and reports errors differently.
There might be many such functions spread throughout the system.
If there's a bug or any change in the way phone numbers are validated, all validation code must be found and corrected,
and any tests must also be updated.

Does anyone set out to write code like this?
Probably not--it starts out seeming like "the simplest thing" and just continues to accumulate, one logical step at a time.
Although _you_ might not write code like this, systems like this exist for phone numbers and for many other data items represented as strings.

## Design by Contract

The argument-validation problem was observed by Bertrand Meyer and introduced as a core concept in his Eiffel programming language,
described in the book _Object-Oriented Software Construction_ (1988).
_Design By Contract_ (DbC) tried to reduce errors by treating the interaction between software components as a formal agreement:

- **_Preconditions_**:
  What must be true before a function/method runs.
- **_Postconditions_**:
  What must be true after the function completes.
- **_Invariants_**:
  What must always be true about the object state.

Eiffel provided explicit keywords to make Design by Contract a first-class citizen in the language:

| Keyword     | Purpose                                    |
|-------------|--------------------------------------------|
| `require`   | Preconditions                              |
| `ensure`    | Postconditions                             |
| `invariant` | Class-wide conditions                      |
| `old`       | Refers to previous state in postconditions |

The intent was that each function used these to ensure the correctness of the inputs and outputs of that function,
and the state of the object.
In particular, `require` typically checks the argument values for correctness.
For preconditions in Python, we can create a `requires` decorator to check argument values:

```python
# require.py
from dataclasses import dataclass
from typing import Callable
from functools import wraps


@dataclass(frozen=True)
class Condition:
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

A `Condition` combines each `check` with a description of the failure condition.
`check` is a `Callable` (usually a function) that takes the same arguments as the decorated function and returns a
`bool` indicating whether the condition is satisfied.

`requires` is a _decorator factory_; it returns a decorator that can be applied to any function.
It accepts any number of `Condition` instances.
The inner function `decorator` is the decorator that wraps the target function `func`.
`wrapper` is the new function that will replace `func`.
`@wraps(func)` preserves metadata like the function name and docstring.

To use it, create one or more `Condition` objects, then use those to decorate functions with `requires`:

```python
# basic_requires.py
from book_utils import Catch
from require import requires, Condition

positivity = Condition(
    check=lambda x: x > 0, message="x must be positive"
)


@requires(positivity)
def sqrt(x) -> float:
    return x**0.5


print(sqrt(4))
## 2.0
with Catch():
    sqrt(-2)
## Error: x must be positive
```

`requires` produces an improved Design by Contract tool for validating function arguments.
Consider managing a bank account:

```python
# bank_account.py
from dataclasses import dataclass
from decimal import Decimal

from book_utils import Catch
from require import requires, Condition

positive_amount = Condition(
    check=lambda self, amount: amount >= Decimal("0"),
    message="Amount cannot be negative",
)

sufficient_balance = Condition(
    check=lambda self, amount: self.balance >= amount,
    message="Insufficient balance",
)


@dataclass
class BankAccount:
    balance: Decimal

    @requires(positive_amount)
    def deposit(self, amount: Decimal) -> str:
        self.balance += amount
        return f"Deposit {amount}, balance: {self.balance}"

    @requires(positive_amount, sufficient_balance)
    def withdraw(self, amount: Decimal) -> str:
        self.balance -= amount
        return f"Withdraw {amount}, balance: {self.balance}"


account = BankAccount(Decimal(100))
print(account.deposit(Decimal(50)))
## Deposit 50, balance: 150
print(account.withdraw(Decimal(30)))
## Withdraw 30, balance: 120
with Catch():
    account.withdraw(Decimal(200))
## Error: Insufficient balance
with Catch():
    account.deposit(Decimal(-10))
## Error: Amount cannot be negative
```

Here, the `Condition`s are applied to methods, so their `lambda`s both include `self`.
In `withdraw` you see multiple `Condition`s applied within one `requires` decorator.

If they validate their arguments, traditional Python functions tend to duplicate that validation code at the beginning of each function body.
Design by Contract is an improvement over this.
The `@requires` clearly shows that the arguments are constrained, and `Condition`s reduce duplicated code.

Design by Contract helps, but it has limitations:

1. A programmer can forget to use `requires`,
   or choose to perform argument checks by hand if Design by Contract doesn't make sense to them.
2. Validations are spread throughout your system.
   Using `Condition` reduces logic duplication, but making changes still risks missing updates on functions.
3. It can be tricky; note the use of `self` in `positive_amount` and `sufficient_balance` so those can be applied to methods.
   This might require new understanding for the user of `requires`.

## Centralizing Validation into Custom Types

A more straightforward approach than DbC is to encode validations into custom types.
This way, incorrect objects of those types cannot successfully be created.
Custom types tend to be easier to understand and use than precondition checks.
If a type constraint changes, that change immediately propagates to all usages of that type.
In addition, the types are usually _domain driven_, that is, they represent a concept from the problem domain.

For the bank example, we start by creating an `Amount`, which is a `Decimal` value with some fundamental constraints.
If an `Amount` object exists, you know it cannot contain a negative value or more than two decimal places:

```python
# amount.py
from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal
from typing import Self


@dataclass(frozen=True)
class Amount:
    value: Decimal

    @classmethod
    def of(cls, value: int | float | str | Decimal) -> Self:
        if isinstance(value, float):
            text = repr(value)
            if "e" in text.lower():
                raise ValueError(f"{value!r}: out of range")
            parts = text.split(".", 1)
            if len(parts) == 2 and len(parts[1]) > 2:
                raise ValueError(f"{value!r}: >2 decimal places")
            dec = Decimal(text)
        else:
            dec = (
                value
                if isinstance(value, Decimal)
                else Decimal(str(value))
            )

        return cls(dec)

    def __post_init__(self) -> None:
        if self.value < Decimal("0"):
            raise ValueError(f"Negative Amount({self.value})")

        if int(self.value.as_tuple().exponent) > 2:
            raise ValueError(
                f"Amount({self.value}): >2 decimal places"
            )

    def __add__(self, other: Amount) -> Amount:
        return Amount.of(self.value + other.value)

    def __sub__(self, other: Amount) -> Amount:
        return Amount.of(self.value - other.value)
```

The `of()` method is intended to be the single point of creation of an `Amount`, however you can still create an `Amount` directly from a `Decimal`.
Even then, `__post_init__` will be called and will ensure that `value` is positive and has no more than two decimal places.

Note that `__add__` and `__sub__` return new `Amount` objects without checking whether they are non-negative.
The `Amount` initialization takes care of that.

Because `Amount` objects are immutable, you don't have to worry that they'll be changed to an illegal state after they're created.

If you provide an incorrect `value` to `Amount`, the `Decimal` constructor throws an exception:

```python
# demo_amount.py
from decimal import Decimal

from amount import Amount
from book_utils import Catch

print(Amount.of(123))  # int
## Amount(value=Decimal('123'))
print(Amount.of("123"))  # str
## Amount(value=Decimal('123'))
print(Amount.of(1.23))  # float
## Amount(value=Decimal('1.23'))
print(Amount.of(Decimal("1.23")))
## Amount(value=Decimal('1.23'))
with Catch():
    Amount.of(-123)
## Error: Negative Amount(-123)
with Catch():
    Amount.of(1.111)
## Error: 1.111: >2 decimal places
with Catch():
    Amount.of("not-a-number")
## Error: [<class 'decimal.ConversionSyntax'>]
# Can construct from Decimal:
print(Amount(Decimal("12.34")))
## Amount(value=Decimal('12.34'))
with Catch():
    Amount(Decimal("-12.34"))
## Error: Negative Amount(-12.34)
with Catch():
    Amount(Decimal("1.111"))
```

Now we define a bank-account `Balance` that contains an `Amount`, but doesn't need special construction behavior:

```python
# balance.py
from __future__ import annotations
from dataclasses import dataclass
from amount import Amount


@dataclass(frozen=True)
class Balance:
    amount: Amount

    def deposit(self, amount: Amount) -> Balance:
        return Balance(self.amount + amount)

    def withdraw(self, amount: Amount) -> Balance:
        return Balance(self.amount - amount)
```

Note that `Balance` produces new immutable objects when you `deposit` and `withdraw`.
Because it uses `Amount`, it needs no special validation checks.

In the new, improved `BankAccount`,
the need for argument validation disappears because it is automatically enforced by the types:

```python
# typed_bank_account.py
from dataclasses import dataclass

from amount import Amount
from balance import Balance
from book_utils import Catch


@dataclass
class BankAccount:
    balance: Balance

    def deposit(self, amount: Amount) -> str:
        self.balance = self.balance.deposit(amount)
        return (
            f"Deposit {amount.value}, "
            f"Balance: {self.balance.amount.value}"
        )

    def withdraw(self, amount: Amount) -> str:
        self.balance = self.balance.withdraw(amount)
        return (
            f"Withdraw {amount.value}, "
            f"Balance: {self.balance.amount.value}"
        )


account = BankAccount(Balance(Amount.of(100)))
print(account.deposit(Amount.of(50)))
## Deposit 50, Balance: 150
print(account.withdraw(Amount.of(30)))
## Withdraw 30, Balance: 120
with Catch():
    account.withdraw(Amount.of(200))
## Error: Negative Amount(-80)
with Catch():
    account.deposit(Amount.of(-10))
## Error: Negative Amount(-10)
```

This code is significantly more straightforward to understand and change.
If we need to modify the underlying representation of `Amount` we only do it in one place.
For example, suppose we discover Python's implementation of `Decimal` is too slow.
We can modify `Amount` to use, for example, a Rust implementation of decimal numbers.
We _only_ need to change the code for `Amount`; all code that uses `Amount` automatically adopts the new behavior.

All code we write that uses our custom types benefits from all the type validations for those custom types.
If we add more validations to `Amount` or `Balance`, they automatically propagate to each site where those types are used.

## A `PhoneNumber` Type

Let's apply this approach to the stringly-typed phone number problem shown at the beginning of the chapter.

```python
# phone_number.py
# Validated and normalized phone number
from __future__ import annotations
from dataclasses import dataclass
from typing import Self
import re

_PHONE_RE = re.compile(
    r"^\+?(\d{1,3})?[\s\-.()]*([\d\s\-.()]+)$"
)


@dataclass(frozen=True)
class PhoneNumber:
    country_code: str
    number: str  # Digits only, no formatting

    @classmethod
    def of(cls, raw: str) -> Self:
        # Parse and validate a raw phone number string.
        match = _PHONE_RE.match(raw.strip())
        if not match:
            raise ValueError(f"Invalid phone number: {raw!r}")
        cc, num = match.groups()
        digits = re.sub(r"\D", "", num)
        if not digits:
            raise ValueError(f"No digits in: {raw!r}")
        country_code = cc or "1"  # default to US
        return cls(country_code, digits)

    def __post_init__(self) -> None:
        # Validate country code: 1-3 digits
        if not re.fullmatch(r"\d{1,3}", self.country_code):
            raise ValueError(
                f"Invalid country code: {self.country_code!r}"
            )
        # Validate number: digits only
        if not re.fullmatch(r"\d+", self.number):
            raise ValueError(
                f"Invalid number digits: {self.number!r}"
            )

    def format_number(self) -> str:
        if len(self.number) == 10:
            area, prefix, line = (
                self.number[:3],
                self.number[3:6],
                self.number[6:],
            )
            return f"({area}) {prefix}-{line}"
        return self.number

    def __str__(self) -> str:
        return f"+{self.country_code} {self.format_number()}"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, PhoneNumber):
            return NotImplemented  # Instead of False
        return (
            self.country_code == other.country_code
            and self.number == other.number
        )
```

We can test this against the list in `string_phone_numbers.py`:

```python
# phone_numbers_as_types.py
from phone_number import PhoneNumber
from string_phone_numbers import phone_numbers
from book_utils import Catch

for raw in phone_numbers:
    with Catch():
        print(PhoneNumber.of(raw))
## +555 1234
## +555 1234
## +1 (555) 123-4567
## +555 1234567
## +1 (555) 123-4567
## +44 (207) 946-0958
## +555 1234567
## +555 1234
## Error: Invalid phone number: '555-12ab'
## Error: Invalid phone number: 'CallMeMaybe'
## +012 34
## Error: Invalid phone number: ''
## +555 1234
print(PhoneNumber("886", "7775551212"))
## +886 (777) 555-1212
```

Every function that works with phone numbers only uses the `PhoneNumber` type.
If you need to modify the behavior of a `PhoneNumber`, you do it in only one place.
If you need to improve the performance of `PhoneNumber` creation and use, you do it in only one place.

## The Programmable Meter

I recently visited my friend Matt, who is a physics professor (we were undergraduate physics students together).
He has a stellar reputation as a teacher, and I realized I had never watched him teach,
so I decided to see him in action.
This was an electronics lab, and the students were using programmable measurement tools.
The interface language these tools used was Python.
To send commands to the programmable meter, the meter developers had used the "stringly-typed" route
(The docs had a reference to Turbo C, so the meter was created long before Python's annotated types).
The students ended up puzzling over getting the format of the strings correct rather than doing the lab.

## How Cyclopts uses Types

Create a simplified example from [python_example_validator.py](https://github.com/BruceEckel/pybooktools/blob/main/src/pybooktools/util/python_example_validator.py).