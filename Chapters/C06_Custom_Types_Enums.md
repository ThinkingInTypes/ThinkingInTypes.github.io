# Custom Types: Enums

> When you find yourself creating a lookup table, dictionary, or registry, consider whether an `Enum` provides a better, type-safe solution.

// Can you import an Enum namespace so you don't have to qualify the names? (yes, but discouraged)

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
print(state.value)     
print(state.name)      

# Equality and identity:
assert Status.OK == Status.OK
assert Status.OK is Status.OK

# Iteration:
for s in Status:
    print(s.name, s.value)

# Invalid member access:
with Catch():
    Status(4)

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

This example applies all the tools we've introduced so far: data classes, Enums, and type safety principles.
It models calendar dates in such a way that:

- Every Date object is guaranteed valid at construction
- Illegal states cannot be represented
- All constraints are embedded directly into the type system

Each month has a number (1–12) and the number of days it contains:

```python
# type_safe_date.py
from dataclasses import dataclass
from enum import Enum

@dataclass(frozen=True)
class MonthValue:
    number: int
    days: int    # Number of days in the month

    def __post_init__(self) -> None:
        if not 1 <= self.number <= 12:
            raise ValueError(f"Invalid month number: {self.number}")
        if not 1 <= self.days <= 31:
            raise ValueError(f"Invalid days in month: {self.days}")

    def valid_day(self, day: int) -> None:
        if not 1 <= day <= self.days:
            raise ValueError(f"Invalid day {day} for month {self.number}")

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
    def number(cls, month_number: int) -> Month:
        for m in cls:
            if m.value.number == month_number:
                return m
        raise ValueError(f"No such month: {month_number}")

@dataclass(frozen=True)
class Date:
    year: int
    month: Month
    day: int

    def __post_init__(self) -> None:
        if self.year <= 0:
            raise ValueError(f"Invalid year: {self.year}")
        self.month.value.valid_day(self.day)

    def __str__(self) -> str:
        return f"{self.year}-{self.month.value.number:02}-{self.day:02}"
```

The `MonthValue` class enforces data validity by ensuring no invalid month definitions can exist.
The `Month` `Enum` serves as a registry of legal months.

Years, months, and days are combined into a single type-safe structure, `Date`.
Every `Date` object is validated at creation time.
You can only create legal dates--illegal states are unrepresentable:

```python
# type_safe_date_demo.py
from type_safe_date import Month, Date

d1 = Date(2025, Month.JANUARY, 31)
print(d1)  # 2025-01-31

d2 = Date(2025, Month.FEBRUARY, 28)
print(d2)  # 2025-02-28
# Invalid day for February
try:
    Date(2025, Month.FEBRUARY, 30)
except ValueError as e:
    print(e)  # Invalid day 30 for month 2

# Invalid year
try:
    Date(0, Month.JANUARY, 1)
except ValueError as e:
    print(e)  # Invalid year: 0

# Lookup by month number
month = Month.number(4)
d3 = Date(2025, month, 30)
print(d3)  # 2025-04-30
```

All invariants live in one place: the data model.
Construction enforces correctness.
The type checker ensures we cannot accidentally confuse months, days, or years.
Errors are caught at the boundary when invalid data is provided.

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