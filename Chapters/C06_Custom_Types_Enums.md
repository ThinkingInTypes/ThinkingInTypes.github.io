# Custom Types: Enums

> When you find yourself creating a lookup table, dictionary, or registry, consider whether an Enum provides a better, type-safe solution.

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

- Enum members can hold any kind of object — not just numbers or strings.
- You can attach behavior directly to Enum members.
- Enums can serve as registries, configuration models, and even state machines.

Enums can be parameterized to fully participate in the type system, giving you even stronger guarantees of correctness.

As with data classes, Enums allow you to bring your problem domain directly into your code, reducing bugs and improving clarity.

## Basic Enums

The simplest Enum is a set of named constants:

```python
# status.py
from enum import Enum

class Status(Enum):
    OK = 1
    ERROR = 2
    RETRY = 3

# Accessing members:
state = Status.OK
print(state)           # Status.OK
print(state.value)     # 1
print(state.name)      # OK

# Equality and identity:
assert Status.OK == Status.OK
assert Status.OK is Status.OK

# Iteration:
for s in Status:
    print(s.name, s.value)

# Invalid member access:
try:
    Status(4)
except ValueError as e:
    print(e)

# Members are immutable:
try:
    Status.OK.value = 42  # AttributeError
except e:
    print(e)
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

Enum values do not need to be integers:

```python
# colors.py
class Color(Enum):
    RED = "red"
    GREEN = "green"
    BLUE = "blue"
```

Many Python libraries (including modern web frameworks) often use str-based Enums for clearer external representation.

### Enums Improve Reliability

Enums provide:

- Centralized definition
- Type safety
- Namespacing (Status.OK instead of OK)
- Iterable membership
- Prevention of invalid values

Enums aren't simply "constants with names" — they are types that make your program's intent explicit.

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

class StrictEnum[T](Enum):
    value: T

@dataclass(frozen=True)
class MonthData:
    number: int  # 1-12
    days: int    # max number of days

    def __post_init__(self) -> None:
        if not 1 <= self.number <= 12:
            raise ValueError(f"Invalid month number: {self.number}")

    def is_valid_day(self, day: int) -> bool:
        return 1 <= day <= self.days

    def check_day(self, day: int) -> None:
        if not self.is_valid_day(day):
            raise ValueError(f"Invalid day {day} for month {self.number}")

class Month(StrictEnum[MonthData]):
    JANUARY = MonthData(1, 31)
    FEBRUARY = MonthData(2, 28)
    MARCH = MonthData(3, 31)
    APRIL = MonthData(4, 30)
    MAY = MonthData(5, 31)
    JUNE = MonthData(6, 30)
    JULY = MonthData(7, 31)
    AUGUST = MonthData(8, 31)
    SEPTEMBER = MonthData(9, 30)
    OCTOBER = MonthData(10, 31)
    NOVEMBER = MonthData(11, 30)
    DECEMBER = MonthData(12, 31)

    def __str__(self) -> str:
        return self.name

    @classmethod
    def from_number(cls, month_number: int) -> Month:
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
        self.month.value.check_day(self.day)

    def __str__(self) -> str:
        return f"{self.year}-{self.month.value.number:02}-{self.day:02}"
```

The MonthData class ensures that no invalid month definitions can exist.
The Month Enum serves as a registry of legal months.
Day validity is enforced inside MonthData.

Next we combine years, months, and days into a single type-safe structure, `Date`.
Every Date object is validated at creation time.
You can only create legal dates — illegal states are unrepresentable.

Sample usage:

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
month = Month.from_number(4)
d3 = Date(2025, month, 30)
print(d3)  # 2025-04-30
```

All invariants live in one place: the data model.
Construction enforces correctness.
The type checker ensures we cannot accidentally confuse months, days, or years.
Errors are caught at the boundary: when invalid data is provided.