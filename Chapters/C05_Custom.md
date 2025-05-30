## Custom Types: Enums

An `Enum` type is preferable when you have a smaller set of values.
`Enum`s provide additional type safety for fixed-value sets such as months:

```python
# birth_date.py
# "Leap years are left as an exercise."
from dataclasses import dataclass
from enum import Enum

from book_utils import Catch


@dataclass
class Day:
    n: int

    def __post_init__(self) -> None:
        assert 1 <= self.n <= 31, f"{self}"


@dataclass
class Year:
    n: int

    def __post_init__(self) -> None:
        assert 1900 < self.n <= 2022, f"{self}"


class Month(Enum):
    JANUARY = (1, 31)
    FEBRUARY = (2, 28)
    MARCH = (3, 31)
    APRIL = (4, 30)
    MAY = (5, 31)
    JUNE = (6, 30)
    JULY = (7, 31)
    AUGUST = (8, 31)
    SEPTEMBER = (9, 30)
    OCTOBER = (10, 31)
    NOVEMBER = (11, 30)
    DECEMBER = (12, 31)

    @staticmethod
    def number(month_number: int):
        assert 1 <= month_number <= 12, f"Month({month_number})"
        return list(Month)[month_number - 1]

    def check_day(self, day: Day):
        assert day.n <= self.value[1], f"{self} {day}"

    def __repr__(self):
        return self.name


@dataclass
class BirthDate:
    m: Month
    d: Day
    y: Year

    def __post_init__(self):
        self.m.check_day(self.d)


for date in [
    (7, 8, 1957),
    (0, 32, 1857),
    (2, 31, 2022),
    (9, 31, 2022),
    (4, 31, 2022),
    (6, 31, 2022),
    (11, 31, 2022),
    (12, 31, 2022),
]:
    with Catch():
        print(date)
        print(
            BirthDate(
                Month.number(date[0]),
                Day(date[1]),
                Year(date[2]),
            )
        )
        print("-" * 30)
## (7, 8, 1957)
## BirthDate(m=JULY, d=Day(n=8), y=Year(n=1957))
## ------------------------------
## (0, 32, 1857)
## Error: Month(0)
## (2, 31, 2022)
## Error: Month.FEBRUARY Day(n=31)
## (9, 31, 2022)
## Error: Month.SEPTEMBER Day(n=31)
## (4, 31, 2022)
## Error: Month.APRIL Day(n=31)
## (6, 31, 2022)
## Error: Month.JUNE Day(n=31)
## (11, 31, 2022)
## Error: Month.NOVEMBER Day(n=31)
## (12, 31, 2022)
## BirthDate(m=DECEMBER, d=Day(n=31), y=Year(n=2022))
## ------------------------------
```

`Month` can be a data class, but it's more complicated than using `Enum`, and with questionable benefits:

```python
# month_data_class.py
from dataclasses import dataclass, field

from book_utils import Catch


@dataclass
class Day:
    n: int

    def __post_init__(self) -> None:
        assert 1 <= self.n <= 31, f"Day({self.n})"


@dataclass
class Year:
    n: int

    def __post_init__(self) -> None:
        assert 1900 < self.n <= 2022, f"Year({self.n})"


@dataclass
class Month:
    name: str
    n: int
    max_days: int

    def __post_init__(self):
        assert 1 <= self.n <= 12, f"Month({self.n})"
        assert self.max_days in [28, 30, 31], (
            f"Month max_days {self.max_days}"
        )

    def check_day(self, day: Day):
        assert day.n <= self.max_days, f"{self} {day}"

    @staticmethod
    def make_months():
        return [
            Month(m[0], m[1], m[2])
            for m in [
                ("January", 1, 31),
                ("February", 2, 28),
                ("March", 3, 31),
                ("April", 4, 30),
                ("May", 5, 31),
                ("June", 6, 30),
                ("July", 7, 31),
                ("August", 8, 31),
                ("September", 9, 30),
                ("October", 10, 31),
                ("November", 11, 30),
                ("December", 12, 31),
            ]
        ]


@dataclass
class Months:
    months: list[Month] = field(
        default_factory=Month.make_months
    )

    def number(self, month_number: int):
        assert 1 <= month_number <= 12, f"Month({month_number})"
        return self.months[month_number - 1]


@dataclass
class BirthDate:
    m: Month
    d: Day
    y: Year

    def __post_init__(self):
        self.m.check_day(self.d)


months = Months()
for date in [
    (7, 8, 1957),
    (0, 32, 1857),
    (2, 31, 2022),
    (9, 31, 2022),
    (4, 31, 2022),
    (6, 31, 2022),
    (11, 31, 2022),
    (12, 31, 2022),
]:
    with Catch():
        print(date)
        print(
            BirthDate(
                months.number(date[0]),
                Day(date[1]),
                Year(date[2]),
            )
        )
        print("-" * 30)
## (7, 8, 1957)
## BirthDate(m=Month(name='July', n=7, max_days=31), d=Day(n=8),
## y=Year(n=1957))
## ------------------------------
## (0, 32, 1857)
## Error: Month(0)
## (2, 31, 2022)
## Error: Month(name='February', n=2, max_days=28) Day(n=31)
## (9, 31, 2022)
## Error: Month(name='September', n=9, max_days=30) Day(n=31)
## (4, 31, 2022)
## Error: Month(name='April', n=4, max_days=30) Day(n=31)
## (6, 31, 2022)
## Error: Month(name='June', n=6, max_days=30) Day(n=31)
## (11, 31, 2022)
## Error: Month(name='November', n=11, max_days=30) Day(n=31)
## (12, 31, 2022)
## BirthDate(m=Month(name='December', n=12, max_days=31),
## d=Day(n=31), y=Year(n=2022))
## ------------------------------
```

Here are all the ways you can use `Enum`s:

```python
# enum_examples.py
"""
Comprehensive demonstration of Enum capabilities.
"""

from enum import (
    Enum,
    auto,
    unique,
    IntEnum,
    StrEnum,
    Flag,
    IntFlag,
)


# 1. Basic Enum definition
class Color(Enum):
    RED = 1
    GREEN = 2
    BLUE = 3


print(Color.RED)
## Color.RED
print(Color.RED.name, Color.RED.value)
## RED 1


# 2. Enum with auto values
class Status(Enum):
    PENDING = auto()
    RUNNING = auto()
    DONE = auto()


print(list(Status))
## [<Status.PENDING: 1>, <Status.RUNNING: 2>, <Status.DONE: 3>]


# 3. Custom values and types
class HttpStatus(IntEnum):
    OK = 200
    NOT_FOUND = 404
    INTERNAL_ERROR = 500


print(
    f"HttpStatus.OK = {HttpStatus.OK}, as int: {int(HttpStatus.OK)}"
)
## HttpStatus.OK = 200, as int: 200

# 4. Iteration and comparison
for color in Color:
    print(f"Color: {color.name} = {color.value}")
## Color: RED = 1
## Color: GREEN = 2
## Color: BLUE = 3

print(Color.RED == Color.RED)
## True
print(Color.RED is Color.RED)
## True
print(Color.RED == Color.GREEN)
## False

# 5. Access by name and value
print(Color["BLUE"])
## Color.BLUE
print(Color(2))  # GREEN
## Color.GREEN


# 6. Unique constraint
@unique
class Direction(Enum):
    NORTH = 1
    SOUTH = 2
    EAST = 3
    WEST = 4
    # UP = 1  # Uncommenting this raises ValueError


# 7. Subclassing str or int for JSON-friendliness
class Fruit(StrEnum):
    APPLE = "apple"
    BANANA = "banana"


print(Fruit.APPLE.upper())
## APPLE
print(f"JSON-ready: {Fruit.BANANA!r}")
## JSON-ready: <Fruit.BANANA: 'banana'>


# 8. Methods and properties on Enums
class Shape(Enum):
    CIRCLE = auto()
    SQUARE = auto()

    def sides(self) -> int:
        return {
            Shape.CIRCLE: 0,
            Shape.SQUARE: 4,
        }[self]


print(f"Shape.CIRCLE has {Shape.CIRCLE.sides()} sides")
## Shape.CIRCLE has 0 sides


# 9. Aliases
class Mood(Enum):
    HAPPY = 1
    JOYFUL = 1  # Alias
    SAD = 2


print(
    f"Members: {[m for m in Mood]}"
)  # Only one member per value
## Members: [<Mood.HAPPY: 1>, <Mood.SAD: 2>]
print(f"Alias: {Mood.JOYFUL is Mood.HAPPY}")
## Alias: True


# 10. Bitwise Flags
class Permission(Flag):
    READ = auto()
    WRITE = auto()
    EXECUTE = auto()


user_perm = Permission.READ | Permission.WRITE  # type: ignore
print(f"User permissions: {user_perm}")
## User permissions: Permission.READ|WRITE
print(f"Can execute? {Permission.EXECUTE in user_perm}")
## Can execute? False


# IntFlag for bitwise checks with ints
class Access(IntFlag):
    NONE = 0
    READ = 1
    WRITE = 2
    EXECUTE = 4


perm = Access.READ | Access.EXECUTE
print(f"perm & Access.WRITE: {perm & Access.WRITE}")
## perm & Access.WRITE: 0
print(f"perm has EXECUTE: {bool(perm & Access.EXECUTE)}")
## perm has EXECUTE: True

# 11. Pattern matching
status = Status.DONE
match status:
    case Status.PENDING:
        print("Job is pending")
    case Status.RUNNING:
        print("Job is in progress")
    case Status.DONE:
        print("Job completed")
## Job completed
```

`Enum`s improve robustness by making code both readable and safely constrained.
For simplicity and IDE interactivity, choose `Enum`s over data classes for fixed-value sets.

TODO: Can enum names be brought into scope?

### Enum Mixins

An `Enum` defines a closed set of named values.
Allowing inheritance conflicts with the meaning of "the set of valid members."
Thus, Python forbids subclassing a concrete `Enum` class to make a new `Enum`.

The only thing you can inherit when dealing with `Enum`s is mixins, like adding methods:

```python
# enum_mixins.py
from enum import Enum


class StrMixin(str):
    pass


class Color(StrMixin, Enum):
    RED = "red"
    GREEN = "green"
```

Here, Color mixes in `str` behavior.
Because it's an `Enum`, you can't inherit from `Color`.

### Enums and Exhaustivity

Because you can't inherit from an `Enum`, an `Enum` can be included in exhaustivity analysis during pattern matching:

```python
# enum_exhaustivity.py
from enum import Enum


class Status(Enum):
    OPEN = "open"
    CLOSED = "closed"
    PENDING = "pending"

    def handle(self) -> str:
        match self:
            case Status.OPEN:
                return f"open: {self}"
            case Status.CLOSED:
                return f"closed: {self}"
            case Status.PENDING:
                return f"pending: {self}"
            # Not possible, but some type checkers
            # haven't caught up yet:
            case _:
                return f"Unhandled: {self}"


print(Status.OPEN.handle())
## open: Status.OPEN
print(Status.CLOSED.handle())
## closed: Status.CLOSED
print(Status.PENDING.handle())
## pending: Status.PENDING
```

Because `Enum`s are closed, you know all possible `Status` members: `OPEN`, `CLOSED`, `PENDING`.
The type checker warns you if you forget to handle a case.
No "unknown" cases can sneak in later because `Enum`s can't be subclassed.

// What different types can Enum members be? Can you mix types within a single Enum?
// Can you provide type annotations to Enum members?

### Attaching Functionality to Enum Members

```python
# state_machine.py
from __future__ import annotations
from enum import Enum
from typing import Callable


def open_next(self: Status) -> Status:
    _ = self  # Silence unused variable warning.
    print("Moving from OPEN to PENDING.")
    return Status.PENDING


def pending_next(self: Status) -> Status:
    _ = self
    print("Moving from PENDING to CLOSED.")
    return Status.CLOSED


def closed_next(self: Status) -> Status:
    _ = self
    print("CLOSED is a final state. Staying put.")
    return Status.CLOSED


class Status(Enum):
    OPEN = ("open", open_next)
    PENDING = ("pending", pending_next)
    CLOSED = ("closed", closed_next)

    def __init__(
        self,
        label: str,
        next_handler: Callable[[Status], Status],
    ) -> None:
        self._label = label
        self._next_handler = next_handler

    def next(self) -> Status:
        return self._next_handler(self)

    @property
    def label(self) -> str:
        return self._label


state = Status.OPEN
while state != Status.CLOSED:
    print(state.label)
    state = state.next()
## open
## Moving from OPEN to PENDING.
## pending
## Moving from PENDING to CLOSED.
```

Each `Enum` member (`Status.OPEN`, etc.) carries two pieces of information:

1. A label: "open" or "pending" or "closed"

2. A handler function `_next_handler`

In the `__init__`, we capture these and assign to instance attributes (`_label`, `_next_handler`).
The `next()` method calls the stored function.

### A Finite State Machine

A _Finite State Machine_ (FSM) chooses its next state based on the current state and one or more inputs.
All the information of an FSM is initialized in the state transition table, so we want that to be
fully typed and as clean as possible. Here's a way to do that:

```python
# finite_state_machine.py
from __future__ import annotations
from enum import Enum
from typing import Dict


class Event(Enum):
    SUBMIT = "submit"
    APPROVE = "approve"
    REJECT = "reject"
    REOPEN = "reopen"


class Status(Enum):
    OPEN = "open"
    PENDING = "pending"
    CLOSED = "closed"

    def __init__(self, label: str) -> None:
        self._label = label

    def on_event(self, event: Event) -> Status:
        mapping = _TRANSITIONS.get(self, {})
        next_state = mapping.get(event)
        if next_state is None:
            print(f"Invalid {self.name} & {event.name}")
            return self
        print(f"{self.name} + {event.name} -> {next_state.name}")
        return next_state

    @property
    def label(self) -> str:
        return self._label


# Mapping of transitions: {current_status: {event: next_status}}
_TRANSITIONS: Dict[Status, Dict[Event, Status]] = {
    Status.OPEN: {Event.SUBMIT: Status.PENDING},
    Status.PENDING: {
        Event.APPROVE: Status.CLOSED,
        Event.REJECT: Status.OPEN,
    },
    Status.CLOSED: {Event.REOPEN: Status.OPEN},
}


def run(initial: Status, events: list[Event]) -> None:
    """
    Execute a sequence of events starting from the given initial status.
    """
    state = initial
    print(f"Starting at {state.label}")
    for event in events:
        state = state.on_event(event)
        print(f"Now at {state.label}")


workflow = [
    Event.SUBMIT,
    Event.REOPEN,
    Event.REJECT,
    Event.SUBMIT,
    Event.APPROVE,
    Event.REOPEN,
]
run(Status.OPEN, workflow)
## Starting at open
## OPEN + SUBMIT -> PENDING
## Now at pending
## Invalid PENDING & REOPEN
## Now at pending
## PENDING + REJECT -> OPEN
## Now at open
## OPEN + SUBMIT -> PENDING
## Now at pending
## PENDING + APPROVE -> CLOSED
## Now at closed
## CLOSED + REOPEN -> OPEN
## Now at open
```

## `Literal`: The Lightweight `Enum`

`Literal` types specify a set of permissible values to ensure values match expected exact constants:

```python
# literal_types.py
from typing import Literal


def set_mode(mode: Literal["auto", "manual"]) -> None:
    print(f"Mode set to {mode}")


set_mode("auto")  # valid
## Mode set to auto
# set_mode('automatic')  # invalid, detected by type checker
```

`Literal`s can serve as a lightweight substitute for `Enum`s when you only need to restrict values at the type level and do not require the additional runtime features of `Enum`s.
This makes `Literal`s attractive for scenarios like defining a parameter that only accepts a small set of constant values without adding extra code complexity.

// What types can a Literal contain?
// Sequence of small examples showing everything you can do with Literals

### Pattern Matching on Literals

```python
# literal_pattern_matching.py
from typing import Literal

Command = Literal["start", "stop", "pause"]


def run_command(cmd: Command) -> str:
    match cmd:
        case "start":
            return "System starting..."
        case "stop":
            return "System stopping..."
        case "pause":
            return "System pausing..."
        # Should not need this; some type checkers
        # require it anyway:
        case _:  # Unreachable
            raise ValueError(f"Unhandled command: {cmd}")


def run_string(cmd: str) -> str | None:
    match cmd:
        case "start":
            return "System starting..."
        case "stop":
            return "System stopping..."
        case "pause":
            return "System pausing..."
    return None
```

In `run_command`, the `cmd` parameter is restricted to the values `"start"`, `"stop"`, or `"pause"`.
The `match` statement uses pattern matching on these `Literal` values.
A type checker will warn you if a branch is missing.
This is called `exhaustiveness checking`.

However, with the `match` in `run_string` there's no way to know what the legal cases are, so exhaustiveness checking is
not possible.

[Example of exhaustiveness checking with subclasses]

### Examples

Can literals be created dynamically?
Probably not.
Example of Country with states, states with counties, counties with towns and cities,
How far can `Literal` go? Is there a limit to the number of Literals in a single element?
Compare that with the same example using Enums.
Perhaps an example that mixes `Literal`s and `Enum`s

### Similarities

- Value Restriction:  
  Both `Literal`s and `Enum`s let you restrict a variable to a fixed set of values.
  For example, `ParamType = Union[float, Literal["MIN", "MAX", "DEF"]]`
  tells a type checker that only these string values are allowed (aside from floats),
  similar to how an `Enum` restricts possible members.

### Differences

- Type Checking vs. Runtime Behavior:
    - `Literal`: `Literal`s are a static type annotation introduced in PEP 586.
      They exist solely for type checking and do not create a distinct runtime type.
      The type checker (and your IDE) knows that only those exact values are allowed, but at runtime,
      they are ordinary values (e.g., ordinary strings).
    - `Enum`: An `Enum` is a real class (inheriting from `enum.Enum`) that creates distinct runtime objects. `Enum`s
      provide additional functionality like iteration over members, comparison, and custom methods. They work both at
      runtime and during static type checking.

- Overhead and Simplicity:
    - `Literal`: Using `Literal`s is easy and lightweight if you just want to specify allowed constant values. There’s
      no additional boilerplate, so it’s a good choice when you only need type constraints.
    - `Enum`: `Enum`s come with more structure and can encapsulate behavior. However, they require defining a class and
      are slightly heavier in terms of syntax and runtime footprint.

### Choosing between `Literal` and `Enum`

- Use `Literal`s if:
    - You need a simple, compile-time constraint on allowed values without extra runtime behavior.
    - You want minimal boilerplate and are comfortable relying on your static type checker and IDE for guidance.

- Use `Enum`s if:
    - You need runtime features, such as iterating over allowed values, custom methods, or more semantic richness (e.g.,
      when each value might need its own behavior or additional attributes).
    - You want a self-documenting interface that clearly models a set of related constants as a distinct type.

Both approaches improve type safety,
but if you need more robust functionality or runtime introspection, an `Enum` might be the better choice.

### Literal Support for Enums

The type checker knows the exact value of an `Enum` member and can narrow types accordingly.
Because of this, type checkers can treat `Enum` values as `Literal`s.

```python
# enum_exhaustiveness.py
from enum import Enum


class Color(Enum):
    RED = "red"
    GREEN = "green"
    BLUE = "blue"


# Did you intentionally leave out Color.BLUE?
def paint1(color: Color) -> str:
    if color == Color.RED:
        return "You chose red"
    elif color == Color.GREEN:
        return "You chose green"
    else:
        return "Something else"


print(paint1(Color.BLUE))
## Something else


# Exhaustiveness checking:
def paint2(color: Color) -> str:
    match color:
        case Color.RED:
            return "You chose red"
        case Color.GREEN:
            return "You chose green"
        case Color.BLUE:
            return "You chose blue"
```

The type checker warns you if a branch is missing.
This is essentially `Literal`-style exhaustiveness for `Enum`s.

### Converting a `Literal` to a `Set`

You can write an expression that looks like it's checking for membership in a `Literal` but it won't work:

```python
# literal_to_set.py
from typing import Literal

ParamVal = Literal["DEF", "MIN", "MAX"]
print(ParamVal)
## typing.Literal['DEF', 'MIN', 'MAX']
print("MIN" in ParamVal)  # type: ignore
## False
print("NOPE" in ParamVal)  # type: ignore
## False

# Convert literal values to a set:
allowed_set = set(ParamVal.__args__)  # type: ignore
print(allowed_set)
## {'MIN', 'MAX', 'DEF'}
print("MIN" in allowed_set)
## True
print("NOPE" in allowed_set)
## False
```

To check for membership, you must convert it to a `set` using the `__args__` property, as seen in `allowed_set`.

## Choosing Between `Enum`, `Literal`, and `Set`

Each approach has its strengths and trade-offs.
The best choice depends on your requirements for type safety, runtime behavior, and code clarity.

### `Literal`

Pros:

- Static Type Safety: Type checkers can enforce that only the allowed constant values appear in your code.
- Minimal Overhead: `Literal`s have no runtime cost; they serve solely as type annotations.
- Simplicity: Using literals is straightforward and requires no extra boilerplate code.

Cons:

- No Runtime Distinction: At runtime, `"MIN"`, `"MAX"`, and `"DEF"` are ordinary strings.
  You lose benefits like custom methods or iteration over members.
- Limited Expressiveness: `Literal`s only provide type-checking constraints and no additional behavior beyond that.

When to Use:

- Use `Literal`s when you need to enforce a small set of constant values at the type level, and you are comfortable
  relying on static type checkers and IDEs for guidance.
- They are ideal for simple cases where you want to ensure that only a few specific string values (alongside other
  types, like numbers) are accepted.

### `Enum`

`Enum`s create a distinct type at runtime and define a collection of symbolic names bound to constant values. For
example:

Pros:

- Runtime Features: `Enum`s are real classes at runtime, so they support iteration, comparison, and custom methods.
- Clarity and Self-Documentation: Using an `Enum` clearly signals that the parameter is one of a predetermined, fixed
  set.
  IDE autocompletion can also list the valid members.
- Extra Functionality: You can add methods or properties to an `Enum` if the values need to carry extra meaning (for
  instance, mapping to specific instrument settings).

Cons:

- Additional Overhead: `Enum`s require a bit more code and syntax compared to `Literal`s.
- Slightly Heavier: While typically negligible, there is a bit more runtime overhead as `Enum`s are objects.

When to Use:

- Use `Enum`s when you need not only type safety at the static level but also runtime assurance--such as when you need
  to iterate over allowed options or attach extra behavior.
- `Enum`s are excellent for cases where the set of allowed values is fixed, and you might want to use them throughout
  your codebase in a uniform, well-documented manner.

### `Set`

A set is a built-in Python data structure that holds unique elements.
In the context of allowed values, you might define
`ALLOWED_KEYWORDS = {"MIN", "MAX", "DEF"}`

Pros:

- Dynamic Membership Testing: `Set`s check if a given value is in the allowed collection using the `in` operator.
- Runtime Flexibility: You can modify the set at runtime if needed (though for constants this might not be necessary).
- Simplicity in Validation: When writing custom validation code, a set easily confirms membership.

Cons:

- Not a Type Annotation: `Set`s do not integrate with static type checkers. They only serve at runtime to check if a
  value belongs to the allowed set.
- No Static Safety: Unlike `Literal`s or `Enum`s, sets don’t give you compile-time guarantees or IDE autocompletion for
  allowed values.

When to Use:

- Use sets for runtime validation where you need a simple way to confirm membership (e.g., inside a helper function that
  checks if a value is valid).
- They are ideal when the allowed values are defined once and only used for dynamic checks, not for type annotations.

### Choosing

Each approach has its specific use cases:

- `Literal`s provide a quick and easy way to inform static type checkers without extra runtime behavior.
- `Enum`s add clarity and runtime functionality at the cost of a little extra complexity.
- `Set`s work well if your validation is purely runtime-oriented, and you don’t need the additional benefits of static
  type restrictions.

Choosing between them depends on whether you prioritize compile-time type checking and better IDE support
(favoring `Literal`s or `Enum`s) or need flexible, dynamic validation (favoring `set`s).
In many cases, combining these approaches can be effective--for example,
using `Literal`s in type annotations and a `set` for quick runtime membership checks in helper functions.

## TypedDicts for Structured Data

`TypedDict` is useful when defining dictionary structures with known keys and typed values.

```python
# typed_dict.py
from typing import TypedDict


class UserProfile(TypedDict):
    username: str
    email: str
    age: int


user: UserProfile = {
    "username": "alice",
    "email": "alice@example.com",
    "age": 30,
}
```

`TypedDict` clarifies expected keys and types, providing type safety for dictionary data.

### Optional Fields

You can specify optional fields using `NotRequired` (Python 3.11+) or `total=False`:

```python
# optional_typed_dict_fields.py
from typing import TypedDict, NotRequired


class UserSettings(TypedDict):
    theme: str
    notifications_enabled: NotRequired[bool]


# Only the required field is provided:
tettings: UserSettings = {"theme": "dark"}
```

This flexibility allows clear definitions for complex, partially optional data structures.

## Combining Dataclasses and `Enum`s

```python
# dataclasses_and_enums.py
from dataclasses import dataclass
from enum import Enum


class Status(Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"


@dataclass
class User:
    id: int
    name: str
    status: Status


print(User(id=1, name="Alice", status=Status.ACTIVE))
## User(id=1, name='Alice', status=<Status.ACTIVE: 'active'>)
```

## Domain-Driven Design (DDD)

Strongly typed domain models help clearly represent domain logic, improving robustness and maintainability.
Define domain entities explicitly to enhance domain logic expressiveness:

```python
# ddd.py
from dataclasses import dataclass


@dataclass
class Product:
    name: str
    price: float


@dataclass
class Order:
    order_id: int
    products: list[Product]

    def total(self) -> float:
        return sum(product.price for product in self.products)
```

Strongly typed domain models help catch issues early, facilitating clearer, safer, and more maintainable codebases.
