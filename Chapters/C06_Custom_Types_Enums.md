# Custom Types: Enums

> When you find yourself creating a lookup table, dictionary, or registry, consider whether an `Enum` provides a better, type-safe solution.

Often, part of your domain consists of a fixed set of choices:

- A product has a limited number of states: AVAILABLE, SOLD_OUT, DISCONTINUED.
- An HTTP response has well-defined status codes.
- An order can be in only one of several phases: PENDING, PAID, SHIPPED, DELIVERED.

We could model these using strings, integers, or constants, but this is error-prone:

- No enforcement of valid values.
- No protection against typos or accidental misuse.
- No integration with the type system.

Enums exist specifically to address these problems.
They provide a way to create named, distinct, and immutable sets of values, each of which is represented as a distinct type-safe object.

Enums introduce a new kind of type safety.
When you use an Enum:

- You limit possible values to exactly those you define.
- The type checker can verify that only valid members are used.
- Your code becomes more self-documenting.
- Many kinds of invalid states become unrepresentable.

Enums directly support one of the most important principles in this book:
> Make illegal states unrepresentable.

Enums aren't just for simple values.
While most programmers initially encounter Enums as collections of named integers, Python’s Enum system is far more powerful:

- Enum members can hold any kind of object--not just numbers or strings.
- You can attach behavior directly to Enum members.
- Enums can serve as registries, configuration models, and even state machines.

Enums can be parameterized to fully participate in the type system, giving you even stronger guarantees of correctness.

As with data classes, Enums allow you to bring your problem domain directly into your code, reducing bugs and improving clarity.

## Basic Enums

The simplest Enum is a set of named constants:

```python
# status.py
from enum import Enum
from book_utils import Catch


class Status(Enum):
    OK = 1
    ERROR = 2
    RETRY = 3


# Accessing members:
state = Status.OK
print(state)
## Status.OK
print(state.value)
## 1
print(state.name)
## OK

# Equality and identity:
assert Status.OK == Status.OK
assert Status.OK is Status.OK

# Iteration:
for s in Status:
    print(s.name, s.value)
## OK 1
## ERROR 2
## RETRY 3

# Invalid member access:
with Catch():
    Status(4)
## Error: 4 is not a valid Status

# Enum members are immutable:
with Catch():
    Status.OK.value = 42  # type: ignore
```

Instead of assigning raw integers or strings, we use the Enum members.
Each member has both a name (OK) and a value (1).
The members are type-safe objects.
We cannot accidentally assign an invalid state.

Enum members provide safe comparisons by both value and identity.

Assign an invalid value produces a runtime error.

Each Enum member knows its own name.
This makes Enums naturally self-documenting, useful for logging, debugging, and display.

Because you can iterate over all members, Enums are convenient for menus, dropdowns, or validating input.

The string form of an Enum member is its qualified name.
This helps clarify logs and debugging output.

Once defined, Enum members cannot be altered.
This immutability makes Enums reliable building blocks.

### Members Can Have Custom Values

Enum values can be other types:

```python
# colors.py
from enum import Enum


class Color(Enum):
    RED = "red"
    GREEN = "green"
    BLUE = "blue"
```

Many Python libraries (including modern web frameworks) use str-based Enums for dot-completion and clearer external representation.

## ...

## Constraining Value Types

```python
# enum_int.py
from enum import IntEnum


class Status(IntEnum):
    OK = 1
    ERROR = 2
    RETRY = 3
```

```python
# enum_str.py
from enum import StrEnum


class Status(StrEnum):
    OK = "yes!"
    ERROR = "no."
    RETRY = "again!"
```

### Parametric Enums

Starting with Python 3.14, the language introduces support for parametric Enums using Enum[T]. This allows specifying the value type directly in the class header:

```text
from enum import Enum

class Status(Enum[int]):
    OK = 1
    ERROR = 2
```

At the time of writing, this feature is supported by type checkers such as Pyright and Mypy.
However, full runtime support in CPython is still rolling out.
For maximum compatibility, we recommend using IntEnum and StrEnum for type-safe enums until full support stabilizes.

## ...

## Type Safe Dates

This example uses data classes, Enums, and type safety principles.
It models calendar dates in such a way that:

- Every Date object is guaranteed valid at construction
- Illegal states cannot be represented
- All constraints are embedded directly into the type system

The `Month(Enum)` will hold `MonthValue`s, each of which holds its month's number (1–12) and the number of days it contains:

```python
# month_value.py
from dataclasses import dataclass
from enum import Enum
from typing import Self


@dataclass(frozen=True)
class MonthValue:
    number: int
    days: int  # Number of days in the month

    def __post_init__(self) -> None:
        if not 1 <= self.number <= 12:
            raise ValueError(
                f"Invalid month number: {self.number}"
            )
        if not 1 <= self.days <= 31:
            raise ValueError(
                f"Invalid days in month: {self.days}"
            )

    def valid_day(self, day: int) -> None:
        if not 1 <= day <= self.days:
            raise ValueError(
                f"Invalid day {day} for month {self.number}"
            )
```

The `MonthValue` class enforces data validity by ensuring no invalid month definitions can exist.

The `Month` `Enum` serves as a registry of legal months:

```python
# month.py
from enum import Enum
from typing import Self
from month_value import MonthValue


class Month(Enum):  # Enum[MonthValue]
    JANUARY = MonthValue(1, 31)
    FEBRUARY = MonthValue(2, 28)
    MARCH = MonthValue(3, 31)
    APRIL = MonthValue(4, 30)
    MAY = MonthValue(5, 31)
    JUNE = MonthValue(6, 30)
    JULY = MonthValue(7, 31)
    AUGUST = MonthValue(8, 31)
    SEPTEMBER = MonthValue(9, 30)
    OCTOBER = MonthValue(10, 31)
    NOVEMBER = MonthValue(11, 30)
    DECEMBER = MonthValue(12, 31)

    def __str__(self) -> str:
        return self.name

    @classmethod
    def number(cls, month_number: int) -> Self:
        for m in cls:
            if m.value.number == month_number:
                return m
        raise ValueError(f"No such month: {month_number}")
```

```python
# year.py
from dataclasses import dataclass


@dataclass(frozen=True)
class Year:
    value: int

    def __post_init__(self) -> None:
        if self.value <= 0:
            raise ValueError(f"Invalid year: {self.value}")
```

```python
# day.py
from typing import Self
from dataclasses import dataclass
from month import Month


@dataclass(frozen=True)
class Day:
    value: int

    def __post_init__(self) -> None:
        if self.value <= 0:
            raise ValueError(f"Invalid day: {self.value}")

    @classmethod
    def of(cls, month: Month, day: int) -> Self:
        month.value.valid_day(day)
        return cls(day)
```

```python
# type_safe_date.py
from dataclasses import dataclass
from year import Year
from month import Month
from day import Day


@dataclass(frozen=True)
class Date:
    year: Year
    month: Month
    day: Day

    def __post_init__(self) -> None:
        # Validate day against month:
        object.__setattr__(
            self, "day", Day.of(self.month, self.day.value)
        )

    def __str__(self) -> str:
        return f"{self.year.value}-{self.month.value.number:02}-{self.day.value:02}"
```

Years, months, and days are combined into a single type-safe structure, `Date`.
Every `Date` object is validated at creation time.
You can only create legal dates--illegal states are unrepresentable:

```python
# type_safe_date_demo.py
from book_utils import Catch
from type_safe_date import Month, Day, Year, Date

print(Date(Year(2025), Month.FEBRUARY, Day(28)))
## 2025-02-28

# Look up by month number
print(Date(Year(2025), Month.number(4), Day(30)))
## 2025-04-30

with Catch():
    Day.of(Month.FEBRUARY, 30)
## Error: Invalid day 30 for month 2

with Catch():
    Year(0)
## Error: Invalid year: 0
```

All invariants live in one place: the data model.
Construction enforces correctness.
The type checker ensures we cannot accidentally confuse months, days, or years.
Errors are caught at the boundary when invalid data is provided.

As an exercise, incorporate leap-year checking.

## Recommended practices

### Don't Import Enum Members into your Namespace

By design, Enums serve as namespaces, preserving both type safety and namespace clarity.

It's possible to remove the qualification:

```python
# direct_value_names.py
from enum import Enum


class Status(Enum):
    OK = 1
    ERROR = 2


OK = Status.OK
ERROR = Status.ERROR

# Programmatically:
globals().update(Status.__members__)

s: Status = OK
s = ERROR
```

This works.
But it pollutes your global namespace.
You lose the explicit association between member and Enum.
It becomes unclear what Enum OK belongs to.
Type checkers can no longer infer the Enum type automatically.
Readability suffers.

## Enums Improve Reliability

Enums provide:

- Centralized definition
- Type safety
- Namespacing (Status.OK instead of OK)
- Iterable membership
- Prevention of invalid values

Enums aren't simply "constants with names"--they are types that make your program's intent explicit.