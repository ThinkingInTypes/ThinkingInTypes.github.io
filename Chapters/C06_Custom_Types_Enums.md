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


# Construction syntax returns corresponding value:
print(Status(2))
## Status.ERROR

# Look up by name string:
print(Status["RETRY"])
## Status.RETRY


# Accessing members:
state = Status.OK
print(state)
## Status.OK
print(state.name)
## OK
print(state.value)
## 1

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
    Status(4)  # Lookup syntax
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

### Generated & Non-int Member Values

```python
# custom_and_generated.py
from enum import Enum, auto


class N(Enum):
    ONE = 1
    TWO = 2
    THREE = 3


# Auto-Generate Sequential Values
class N2(Enum):
    ONE = auto()
    TWO = auto()
    THREE = auto()


# Enum values can be types other than int:
class Color(Enum):
    RED = "red"
    GREEN = "green"
    BLUE = "blue"


# Access all members
print(f"{N.__members__ = }")
## N.__members__ = mappingproxy({'ONE': <N.ONE: 1>, 'TWO': <N.TWO:
## 2>, 'THREE': <N.THREE: 3>})
print(f"{N2.__members__ = }")
## N2.__members__ = mappingproxy({'ONE': <N2.ONE: 1>, 'TWO':
## <N2.TWO: 2>, 'THREE': <N2.THREE: 3>})
print(f"{Color.__members__ = }")
## Color.__members__ = mappingproxy({'RED': <Color.RED: 'red'>,
## 'GREEN': <Color.GREEN: 'green'>, 'BLUE': <Color.BLUE: 'blue'>})
# All names:
print([member.name for member in Color])
## ['RED', 'GREEN', 'BLUE']
# All values:
print([member.value for member in Color])
## ['red', 'green', 'blue']
# Ordered by definition order, not value order:
print(list(Color))
## [<Color.RED: 'red'>, <Color.GREEN: 'green'>, <Color.BLUE:
## 'blue'>]
# Enum members are singletons:
print(Color.RED is Color("red"))
## True
# Internal maps:
print(N._member_map_)
## {'ONE': <N.ONE: 1>, 'TWO': <N.TWO: 2>, 'THREE': <N.THREE: 3>}
print(N._value2member_map_)
## {1: <N.ONE: 1>, 2: <N.TWO: 2>, 3: <N.THREE: 3>}
# Check if a value has a corresponding member:
print(2 in N._value2member_map_)
## True
print("blue" in Color._value2member_map_)
## True
```

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

Many Python libraries (including modern web frameworks) use str-based Enums for dot-completion and clearer external representation.

## Flag Enums

```python
# option_flags.py
from enum import Flag, auto


class Option(Flag):
    NONE = 0
    TRACE = auto()
    DEBUG = auto()
    VERBOSE = auto()
    SILENT = auto()
    SAVE = auto()

    @classmethod
    def all(cls) -> "Option":
        return (
            cls.TRACE
            | cls.DEBUG
            | cls.VERBOSE
            | cls.SILENT
            | cls.SAVE
        )


print([(member, member.name, member.value) for member in Option])
## [(<Option.TRACE: 1>, 'TRACE', 1), (<Option.DEBUG: 2>, 'DEBUG',
## 2), (<Option.VERBOSE: 4>, 'VERBOSE', 4), (<Option.SILENT: 8>,
## 'SILENT', 8), (<Option.SAVE: 16>, 'SAVE', 16)]

for k, v in Option.__members__.items():
    print(f"{k} = {v.value} ({v.value:08b})")
## NONE = 0 (00000000)
## TRACE = 1 (00000001)
## DEBUG = 2 (00000010)
## VERBOSE = 4 (00000100)
## SILENT = 8 (00001000)
## SAVE = 16 (00010000)

# Compose options:
opt1 = Option.TRACE | Option.VERBOSE
# Combined flags produce symbolic names, not just numbers:
print(f"{opt1 = } ({opt1.value:08b})")
## opt1 = <Option.TRACE|VERBOSE: 5> (00000101)
opt2 = opt1 | Option.SAVE
print(f"{opt2 = } ({opt2.value:08b})")
## opt2 = <Option.TRACE|VERBOSE|SAVE: 21> (00010101)

# Membership:
print(f"{Option.TRACE in opt2 = }")
## Option.TRACE in opt2 = True
print(f"{Option.VERBOSE not in opt2 = }")
## Option.VERBOSE not in opt2 = False

# Bitwise AND: what options are present in both:
print(f"{opt2 & Option.VERBOSE = }")
## opt2 & Option.VERBOSE = <Option.VERBOSE: 4>
print(f"{opt2 & Option.DEBUG = }")
## opt2 & Option.DEBUG = <Option.NONE: 0>

# Equivalence:
print(f"{(opt2 & Option.SAVE) != Option.NONE = }")
## (opt2 & Option.SAVE) != Option.NONE = True

# Bitwise XOR: what options are missing from opt2:
print(f"Missing: {Option.all() ^ opt2}")
## Missing: Option.DEBUG|SILENT
```

### IntFlag

```python
# intflag_vs_flag.py
from enum import Flag, IntFlag, auto

from book_utils import Catch


class Flags(Flag):
    FIRST = auto()
    SECOND = auto()
    THIRD = auto()


class IntFlags(IntFlag):
    FIRST = auto()
    SECOND = auto()
    THIRD = auto()


# Both auto-assign powers of two:
for k, v in Flags.__members__.items():
    print(f"{k} = {v.value} ({v.value:08b})")
## FIRST = 1 (00000001)
## SECOND = 2 (00000010)
## THIRD = 4 (00000100)

defined = 3  # FIRST | SECOND
undefined = 903

# Both succeed:
print(f"{IntFlags(defined) = }")
## IntFlags(defined) = <IntFlags.FIRST|SECOND: 3>
print(f"{Flags(defined) = }")
## Flags(defined) = <Flags.FIRST|SECOND: 3>

# IntFlags accepts any value:
print(f"{IntFlags(undefined) = }")
## IntFlags(undefined) = <IntFlags.FIRST|SECOND|THIRD|896: 903>

# Flags requires defined value:
with Catch():
    Flags(undefined)
## Error: <flag 'Flags'> invalid value 903
##     given 0b0 1110000111
##   allowed 0b0 0000000111
```

`IntFlag` accepts any integer.
It decomposes the known parts (`FIRST | SECOND`) and just keeps the remaining bits as numeric.

`Flag` is strict.
It checks whether any bits are unknown (not part of `FIRST` or `SECOND`).
Since `903` contains unknown bits, it fails.

### Ensuring Uniqueness

```python
# unique_values.py
# pyright: reportArgumentType=false
from enum import Enum, unique

from book_utils import Catch

with Catch():

    @unique
    class Color(Enum):
        RED = 1
        GREEN = 2
        BLUE = 3
        DUPLICATE = 3
## Error: duplicate values found in <enum 'Color'>: DUPLICATE ->
## BLUE
```

### Ensuring Continuous Values

```python
# continuous_values.py
# pyright: reportArgumentType=false
from enum import Enum, EnumCheck

# CONTINUOUS Not implemented yet
class Status(Enum, boundary=EnumCheck.CONTINUOUS):
    OK = 1
    WARNING = 2
    ERROR = 3
    MISSING = 5  # error: gap
```

### Ensuring Bitwise Combinations

We can ensure that all possible bitwise combinations of flags have a name.
This helps ensure that your flags are fully named even for combinations.

```python
# all_combinations.py
# pyright: reportArgumentType=false
from enum import Flag, EnumCheck, auto


class AllFlags(Flag, boundary=EnumCheck.NAMED_FLAGS):
    FIRST = auto()  # 1
    SECOND = auto()  # 2
    THIRD = auto()  # 4
    ALL = FIRST | SECOND | THIRD  # 7


# NAMED_FLAGS not implemented yet
class Missing(Flag, boundary=EnumCheck.NAMED_FLAGS):
    FIRST = auto()
    SECOND = auto()
    THIRD = auto()
```

This feature is primarily useful for Flag or IntFlag.

## ...

## Type Safe Dates

This example uses data classes, `Enum`s, and type safety principles.
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
```

The `MonthValue` class enforces data validity by ensuring no invalid month definitions can exist.
Because it's a frozen data class, it cannot be made invalid after creation.

The `Month` `Enum` serves as a registry of legal months:

```python
# month.py
from enum import Enum
from typing import Self

from month_value import MonthValue


class Month(Enum):
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

    def __int__(self) -> int:
        return self.value.number

    def valid_day(self, day: int) -> None:
        if not 1 <= day <= self.value.days:
            raise ValueError(f"Invalid day {day} for {self}")

    @classmethod
    def _missing_(cls, value: object) -> Self:
        if not isinstance(value, int):
            raise TypeError("Expected int")
        for m in cls:
            if m.value.number == value:
                return m
        raise ValueError(f"No such month: {value}")
```

When you try to access an `Enum` member using a value that doesn't exist, the `_missing_` method is invoked.
By default, `_missing_` does nothing, resulting in a `ValueError` when an invalid value is used to create an enum member.
By overriding `_missing_`, you can implement custom logic to handle cases where the provided value doesn't directly match an existing member.
Now you can say `Month(3)` and it will produce `Month.MARCH`.

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
        # Ensure day is within Month's range:
        month.valid_day(day)
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
You can only create legal dates--illegal states are unrepresentable.

```python
# type_safe_date_demo.py
from book_utils import Catch
from type_safe_date import Month, Day, Year, Date

print(Date(Year(2025), Month.FEBRUARY, Day(28)))
## 2025-02-28

# Look up by month number
print(Date(Year(2025), Month(4), Day(30)))
## 2025-04-30

with Catch():
    Day.of(Month.FEBRUARY, 30)
## Error: Invalid day 30 for FEBRUARY

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