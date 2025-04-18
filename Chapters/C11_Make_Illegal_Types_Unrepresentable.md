# Make Illegal Types Unrepresentable

A common strategy for preventing problems is to check values after arguments are passed to functions.
This spreads validation code across functions, producing maintenance problems.
This chapter moves validation into custom types that make invalid data impossible.
In addition, data is checked when you create an instance, rather than when data is passed to a function.
With this approach, you:

1. Discover problems sooner.
2. Clarify the meaning of your code.
3. Share custom type benefits across all functions that use those types.
4. Eliminate duplicate validation checks and their associated maintenance.
5. Make changes easier by localizing validation to a single point.
6. Eliminate the need for techniques such as Design By Contract (DBC).
7. Enable more focused testing with finer granularity.
8. Naturally move towards Domain-Driven Design.

## "Stringly Typed"

Years ago I came across some research looking at the way generic components like `List`, `Set` and `Map` were used in Java.
Only a tiny percentage of the code reviewed used anything _except_ strings as type parameters.
This study suggested that the vast majority of systems were using strings as their primary data type.

Because you can put any characters in any format into a string, such "stringly typed" systems (an ironic play on "strongly typed") may be the worst of all possible worlds.
Unless it's actually text, classifying something as a string doesn't tell you anything.
When a function receives a string meant to represent a type, that function can assume precisely nothing about it.
Every such function must start from scratch and analyze that string to see if it conforms to what that function needs.

Changing the meaning of a stringly-typed item is a daunting job.
You must look through every function that uses it and ensure that your change is reflected in the validations in every single function.
Because the logic is distributed, it's highly likely you will miss some.

Consider representing phone numbers as strings.
Here are just a few of the different formats you might encounter:

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

Any function that takes a phone number represented as a string must first validate that number.
Here's one of the worst approaches imaginable:

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
If there's a bug or any change in the way phone numbers are validated, all validation code must be hunted down and corrected, and any tests must also be updated.

Does anyone set out to write code like this?
Probably not--it starts out seeming like "the simplest thing" and just continues to accumulate, one logical step at a time.
Although _you_ might not write code like this, systems like this exist for phone numbers and for many other data items represented as strings.
We'll learn how custom types dramatically simplify validation and guarantee correctness throughout your system.

## Design by Contract

The argument-validation problem was observed by Bertrand Meyer and introduced as a core concept in his Eiffel programming language, described in the book _Object-Oriented Software Construction_ (1988).
_Design By Contract_ (DbC) tried to reduce errors by treating the interaction between software components as a formal agreement:

- **_Preconditions_**:
  What must be true before a function/method runs.
- **_Postconditions_**:
  What must be true after the function completes.
- **_Invariants_**:
  What must always be true about the object state.

Eiffel provided explicit keywords to make DbC a first-class citizen in the language:

| Keyword     | Purpose                                    |
|-------------|--------------------------------------------|
| `require`   | Preconditions                              |
| `ensure`    | Postconditions                             |
| `invariant` | Class-wide conditions                      |
| `old`       | Refers to previous state in postconditions |

The intent was that each function used these to ensure the correctness of the inputs and outputs of that function, and the state of the object.
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

A `Condition` combines each `check` with a description of the failure condition.
`check` is a `Callable` (usually a function) that takes the same arguments as the decorated function and returns a `bool` indicating whether the condition is satisfied.

`requires` is a _decorator factory_; it returns a decorator that can be applied to any function.
It accepts any number of `Condition` instances.

This inner function `decorator` is the actual decorator; it wraps the target function `func`.

`wrapper` is the new function that will replace `func`.
`@wraps(func)` preserves metadata like the function name and docstring.

To use it, create one or more `Condition` objects and decorate functions with them using `requires`:

```python
# basic_requires.py
from book_utils import Catch
from require import requires, Condition

positivity = Condition(
    check=lambda x: x > 0, message="x must be positive"
)


@requires(positivity)
def sqrt(x) -> float:
    return x ** 0.5


print(sqrt(4))
## 2.0
with Catch():
    sqrt(-2)
## Error: x must be positive
```

`requires` produces an improved design-by-contract tool for validating function arguments.
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

    @requires(positive_amount, sufficient_balance)
    def withdraw(self, amount: Decimal) -> str:
        self.balance -= amount
        return f"Withdrew {amount}, balance: {self.balance}"

    @requires(positive_amount)
    def deposit(self, amount: Decimal) -> str:
        self.balance += amount
        return (
            f"Deposited {amount}, balance: {self.balance}"
        )


account = BankAccount(Decimal(100))
print(account.deposit(Decimal(50)))
## Deposited 50, balance: 150
print(account.withdraw(Decimal(30)))
## Withdrew 30, balance: 120
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

DbC helps, but it has limitations:

1. A programmer can forget to use `requires`, or choose to perform argument checks by hand if DbC doesn't make sense to them.
2. Validations are spread throughout your system.
   Using `Condition` reduces logic duplication, but making changes still risks missing updates on functions.

## Centralizing Validation into Custom Types

Instead of DbC, we can encode validations into custom types.
This way, incorrect objects of those types cannot successfully be created.
In addition, the types are usually _domain driven_, that is, they represent a concept from the problem domain.

For the bank example, we start by creating an `Amount`, which is a `Decimal` value with the fundamental property that it cannot be negative.
If an `Amount` object exists, you know it cannot contain a negative value:

```python
# amount.py
from dataclasses import dataclass
from decimal import Decimal


@dataclass(frozen=True)
class Amount:
    value: Decimal

    def __init__(self, value: int | float | str | Decimal):
        d_value = Decimal(str(value))
        if d_value < Decimal("0"):
            raise ValueError(
                f"Amount({d_value}) cannot be negative"
            )
        object.__setattr__(self, "value", d_value)

    def __add__(self, other: "Amount") -> "Amount":
        return Amount(self.value + other.value)

    def __sub__(self, other: "Amount") -> "Amount":
        return Amount(self.value - other.value)
```

Although `Amount` is a frozen `dataclass`, it is still possible to write an `__init__` method.
Doing so replaces the constructor generated by `dataclass`.
Here, the `__init__` allows `Amount` to accept multiple types of input.
It turns `value` by converting it to a `str`.
This is passed to `Decimal` and the result is checked to ensure it is non-negative.

`__init__` modifies itself using `object.__setattr__`, but other than that we want it safely immutable.
Modifying a frozen `dataclass` using `object.__setattr__` is best only done during construction.
You'll more commonly call `object.__setattr__` in `__post_init__`, but if you find yourself using it in other methods, reconsider whether your type is really frozen.
Requiring `object.__setattr__` to modify a frozen `dataclass` means you have a way to search for modifications.

Note that `__add__` and `__sub__` return new `Amount` objects without checking whether they are non-negative
The `Amount` initialization takes care of that.

If you provide an incorrect `value` to `Amount`, the `Decimal` constructor throws an exception:

```python
# bad_amount.py
from amount import Amount
from book_utils import Catch

print(Amount(123))
## Amount(value=Decimal('123'))
print(Amount("123"))
## Amount(value=Decimal('123'))
print(Amount(1.23))
## Amount(value=Decimal('1.23'))
with Catch():
    Amount("not-a-number")
## Error: [<class 'decimal.ConversionSyntax'>]
```

Now we define a bank-account `Balance` that contains an `Amount`, but doesn't need special construction behavior.
Thus, we can produce an immutable using `NamedTuple`:

```python
# balance.py
from typing import NamedTuple
from amount import Amount


class Balance(NamedTuple):
    amount: Amount

    def deposit(self, deposit_amount: Amount) -> "Balance":
        return Balance(self.amount + deposit_amount)

    def withdraw(
            self, withdrawal_amount: Amount
    ) -> "Balance":
        return Balance(self.amount - withdrawal_amount)
```

Note that `Balance` produces new immutable objects when you `deposit` and `withdraw`.
Because it uses `Amount`, it needs no special validation checks.

In the new, improved `BankAccount`, the need for validation disappears because it is automatically enforced by the types:

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
        return f"Deposited {amount.value}, balance: {self.balance.amount.value}"

    def withdraw(self, amount: Amount) -> str:
        self.balance = self.balance.withdraw(amount)
        return f"Withdrew {amount.value}, balance: {self.balance.amount.value}"


account = BankAccount(Balance(Amount(100)))
print(account.deposit(Amount(50)))
## Deposited 50, balance: 150
print(account.withdraw(Amount(30)))
## Withdrew 30, balance: 120
with Catch():
    account.withdraw(Amount(200))
## Error: Amount(-80) cannot be negative
with Catch():
    account.deposit(Amount(-10))
## Error: Amount(-10) cannot be negative
```

This code is significantly more straightforward to understand and change.
If we need to modify the underlying representation of `Amount` we only do it in one place.
For example, suppose we discover Python's implementation of `Decimal` is too slow.
We can modify `Amount` to use, for example, a Rust implementation of decimal numbers.
We _only_ need to change the code for `Amount` because the rest of the code uses `Amount`.

Any new code we write that uses our custom types transparently benefits from all the type validations built into those types.
If we add more validations to `Amount` or `Balance`, they automatically propagate to each site where those types are used.

## A `PhoneNumber` Type

Let's apply this approach to the stringly-typed phone number problem shown at the beginning of the chapter.

```python
# phone_number.py
from dataclasses import dataclass
from typing import Self
import re


@dataclass(frozen=True)
class PhoneNumber:
    """
    A validated and normalized phone number.
    """

    country_code: str
    number: str  # Digits only, no formatting

    phone_number_re = re.compile(
        r"^\+?(\d{1,3})?[\s\-.()]*([\d\s\-.()]+)$"
    )

    @classmethod
    def parse(cls, raw: str) -> Self:
        cleaned = raw.strip()
        match = cls.phone_number_re.match(cleaned)
        if not match:
            raise ValueError(
                f"Invalid phone number: {raw!r}"
            )

        cc, num = match.groups()
        digits = re.sub(r"\D", "", num)
        if not digits:
            raise ValueError(f"No digits found in: {raw!r}")

        country_code = cc if cc else "1"  # default to US
        return cls(country_code=country_code, number=digits)

    def format_number(self) -> str:
        if len(self.number) == 10:
            return f"({self.number[:3]}) {self.number[3:6]}-{self.number[6:]}"
        return self.number  # Fallback: just the digits

    def __str__(self) -> str:
        formatted = self.format_number()
        return f"+{self.country_code} {formatted}"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, PhoneNumber):
            return NotImplemented
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
        pn = PhoneNumber.parse(raw)
        print(f"{raw!r} -> {pn}")
## '5551234' -> +555 1234
## '555-1234' -> +555 1234
## '(555) 123-4567' -> +1 (555) 123-4567
## '555.123.4567' -> +555 1234567
## '+1-555-123-4567' -> +1 (555) 123-4567
## '+44 20 7946 0958' -> +44 (207) 946-0958
## '5551234567' -> +555 1234567
## '555 1234' -> +555 1234
## Error: Invalid phone number: '555-12ab'
## Error: Invalid phone number: 'CallMeMaybe'
## '01234' -> +012 34
## Error: Invalid phone number: ''
## ' 5551234 ' -> +555 1234
```

Every function that works with phone numbers only uses the `PhoneNumber` type.
If you need to modify the behavior of a `PhoneNumber`, you do it in only one place.
If you need to improve the performance of `PhoneNumber` creation and use, you do it in only one place,
for example, by converting the `PhoneNumber` type into a Rust module.

## The Programmable Meter

I recently visited my friend Matt, who is a physics professor (we were undergraduate physics students together).
He has a stellar reputation as a teacher, and I realized I had never watched him teach, so I decided to see him in action.
This was an electronics lab, and the students were using programmable measurement tools.
The interface language these tools used was Python.
To send commands to the programmable meter, the meter developers had used the stringly-typed route
(The docs had a reference to Turbo C, so the meter was created long before Python's annotated types).
The students ended up puzzling over getting the format of the strings correct, rather than doing the lab.

## How Cyclopts uses Types

