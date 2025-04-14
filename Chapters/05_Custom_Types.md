# Custom Types

- Add variations:
  `NamedTuple`, `Enum`
- Incorporate examples from <https://github.com/BruceEckel/DataClassesAsTypes>

This chapter began as a presentation at a Python conference, inspired by conversations with fellow programmers exploring functional programming techniques.
Specifically, the idea arose from a podcast discussion about Scala's smart types.
After extensive study of functional programming, several concepts coalesced into an approach that leverages Python’s data classes effectively.
This chapter aims to share those insights and illustrate the practical benefits of Python data classes, guiding you towards clearer, more reliable code.

## Misunderstanding Class Attributes

This chapter contains additional tools that modify the normal behavior of class attributes.
It's important to understand that this behavior is created by the tool and that ordinary classes do not behave this way.
Read the [Class Attributes](A06_Class_Attributes.md) appendix for a deeper understanding.

## Ensuring Correctness

Imagine building a customer feedback system using a rating from one to ten stars.
Traditionally, Python programmers use an integer type, checking its validity whenever it's used:

```python
# int_stars.py
# Using 1-10 stars for customer feedback.
from book_utils import Catch


def f1(stars: int) -> int:
    # Must check argument...
    assert 1 <= stars <= 10, f"f1: {stars}"
    return stars + 5


def f2(stars: int) -> int:
    # ...each place it is used.
    assert 1 <= stars <= 10, f"f2: {stars}"
    return stars * 5


stars1 = 6
print(stars1)
## 6
print(f1(stars1))
## 11
print(f2(stars1))
## 30
stars2 = 11
with Catch():
    print(f1(stars2))
## Error: f1: 11
stars1 = 99
with Catch():
    print(f2(stars1))
## Error: f2: 99
```

However, each time the integer is used, its validity must be rechecked, leading to duplicated logic, scattered validation, and potential mistakes.

## Traditional Object-Oriented Encapsulation

Object-oriented programming (OOP) suggests encapsulating validation within the class.
Python typically uses a private attribute (indicated with a single leading underscore) for encapsulation:

```python
# stars_class.py
from typing import Optional
from book_utils import Catch


class Stars:
    def __init__(self, n_stars: int):
        self._number = n_stars  # Private by convention
        self.condition()

    def condition(self, s: Optional[int] = None):
        if s:
            assert 1 <= s <= 10, f"{self}: {s}"
        else:
            assert 1 <= self._number <= 10, f"{self}"

    # Prevent external modification:
    @property
    def number(self):
        return self._number

    # Create readable output:
    def __str__(self) -> str:
        return f"Stars({self._number})"

    # Every member function must guard the private variable:
    def f1(self, n_stars: int) -> int:
        self.condition(n_stars)  # Precondition
        self._number = n_stars + 5
        self.condition()  # Postcondition
        return self._number

    def f2(self, n_stars: int) -> int:
        self.condition(n_stars)  # Precondition
        self._number = n_stars * 5
        self.condition()  # Postcondition
        return self._number


stars1 = Stars(4)
print(stars1)
## Stars(4)
print(stars1.f1(3))
## 8
with Catch():
    print(stars1.f2(stars1.f1(3)))
## Error: Stars(40)
with Catch():
    stars2 = Stars(11)
## Error: Stars(11)
stars3 = Stars(5)
print(stars3.f1(4))
## 9
with Catch():
    print(stars3.f2(22))
## Error: Stars(9): 22
# @property without setter prevents mutation:
with Catch():
    stars1.number = 99
## Error: property 'number' of 'Stars' object has
## no setter
```

This approach centralizes validation yet remains cumbersome.
Each method interacting with the attribute still requires pre-and post-condition checks, cluttering the code and potentially introducing errors if a developer neglects these checks.

## Type Aliases & `NewType`

TODO: Apply to "stars"

Suppose you have a `dict` with nested structures or a `tuple` with many elements.
Writing out these types every time is unwieldy.
Type aliases assign a name to a type to make annotations cleaner and more maintainable.

A type alias is a name assignment at the top level of your code.
We normally name type aliases with CamelCase to indicate they are types:

```python
# simple_type_aliasing.py
from typing import get_type_hints

Number = int | float | str
Measurements = list[Number]


def process_measurements(data: Measurements) -> None:
    print(get_type_hints(process_measurements))
    for n in data:
        print(f"{n = }, {type(n) = }")


process_measurements(Measurements([11, 3.14, "1.618"]))
## {'data': list[int | float | str], 'return':
## <class 'NoneType'>}
## n = 11, type(n) = <class 'int'>
## n = 3.14, type(n) = <class 'float'>
## n = '1.618', type(n) = <class 'str'>
process_measurements([11, 3.14, "1.618"])
## {'data': list[int | float | str], 'return':
## <class 'NoneType'>}
## n = 11, type(n) = <class 'int'>
## n = 3.14, type(n) = <class 'float'>
## n = '1.618', type(n) = <class 'str'>
# Not allowed:
# process_measurements(Measurements(
#     [Number(11), Number(3.14), Number("1.618")])
# )
```

Using `Number` and `Measurements` is functionally identical to writing the annotation as `int | float` or `list[Number]`.
The aliases:

- Gives a meaningful name to the type, indicating what the `list` of `Number`s represents--in this case, a collection called `Measurements`.
- Avoids repeating a complex type annotation in multiple places.
- Improves readability by abstracting away the details of the type structure.
- If the definition of `Measurements` changes (if we use a different type to represent `Number`), we can update the alias in one place.

You can see from the output that type aliases do not create new types at runtime;
they are purely for the benefit of the type system and the developer.

### `NewType`

A type alias is a notational convenience, but it doesn't create a new type recognized by the type checker.
`NewType` does create a new, distinct type, preventing accidental misuse of similar underlying types.
You'll often want to use `NewType` instead of type aliasing:

```python
# new_type.py
from typing import NewType, get_type_hints

Number = NewType("Number", int | float | str)
Measurements = NewType("Measurements", list[Number])


def process_measurements(data: Measurements) -> None:
    print(get_type_hints(process_measurements))
    for n in data:
        print(f"{n = }, {type(n) = }")


process_measurements(
    Measurements(
        [Number(11), Number(3.14), Number("1.618")]
    )
)
## {'data': __main__.Measurements, 'return':
## <class 'NoneType'>}
## n = 11, type(n) = <class 'int'>
## n = 3.14, type(n) = <class 'float'>
## n = '1.618', type(n) = <class 'str'>
process_measurements(Measurements([11, 3.14, "1.618"]))
## {'data': __main__.Measurements, 'return':
## <class 'NoneType'>}
## n = 11, type(n) = <class 'int'>
## n = 3.14, type(n) = <class 'float'>
## n = '1.618', type(n) = <class 'str'>
# Not allowed:
# process_measurements([11, 3.14, "1.618"])
```

`get_type_hints` produces information about the function.

`NewType` is intended to create a distinct type at the type-checking level that is based on some other
(usually simpler) type.
Its primary goal is 
to help prevent the mixing of semantically different values that are represented by the same underlying type;
for example, differentiating `UserID` from `ProductID`, even though both are `int`s:

```python
# new_type_users.py
from typing import NewType

UserID = NewType("UserID", int)
ProductID = NewType("ProductID", int)
Users = NewType("Users", list[UserID])

users = Users([UserID(2), UserID(5), UserID(42)])


def increment(uid: UserID) -> UserID:
    # Transparently access underlying value:
    return UserID(uid + 1)


# increment(42)  # Type check error

# Access underlying list operation:
print(increment(users[-1]))
## 43


def increment_users(users: Users) -> Users:
    return Users([increment(uid) for uid in users])


print(increment_users(users))
## [3, 6, 43]
```

Notice that `Users` uses `UserID` in its definition.
The type checker requires `UserID` for `increment` and `Users` for `increment_users`,
even though we can transparently access the underlying elements of each type (`int` and `list[UserID]`).

## Data Classes

Data classes,
introduced in Python 3.7,
significantly streamline the process of creating types by generating essential methods automatically.
They provide a structured, concise way to define data-holding objects:

```python
# messenger.py
from dataclasses import dataclass, replace


@dataclass
class Messenger:
    name: str
    number: int
    depth: float = 0.0  # Default argument


x = Messenger(name="x", number=9, depth=2.0)
m = Messenger("foo", 12, 3.14)
print(m)
## Messenger(name='foo', number=12, depth=3.14)
print(m.name, m.number, m.depth)
## foo 12 3.14
mm = Messenger("xx", 1)  # Uses default argument
print(mm == Messenger("xx", 1))  # Generates __eq__()
## True
print(mm == Messenger("xx", 2))
## False

# Make a copy with a different depth:
mc = replace(m, depth=9.9)
print(m, mc)
## Messenger(name='foo', number=12, depth=3.14)
## Messenger(name='foo', number=12, depth=9.9)

# Mutable:
m.name = "bar"
print(m)
## Messenger(name='bar', number=12, depth=3.14)
# d = {m: "value"}
# TypeError: unhashable type: 'Messenger'
```

In a `dataclass`, validation logic resides in the `__post_init__` method, executed automatically after initialization.
This guarantees that only valid `Stars` instances exist.

### Immutable Data Classes

Functional programming strongly advocates immutability, preventing accidental changes and thus simplifying reasoning about your code.
Python data classes support immutability through a `frozen=True` parameter:

```python
# frozen_data_classes.py
from dataclasses import dataclass


@dataclass(frozen=True)
class Messenger:
    name: str
    number: int
    depth: float = 0.0  # Default


m = Messenger("foo", 12, 3.14)
print(m)
## Messenger(name='foo', number=12, depth=3.14)
# Frozen dataclass is immutable:
# m.name = "bar"
# dataclasses.FrozenInstanceError: cannot assign to field 'name'
# Automatically creates __hash__():
d = {m: "value"}
print(d[m])
## value
```

We can apply this approach to our `Stars` example:

```python
# stars.py
from dataclasses import dataclass

from book_utils import Catch


@dataclass(frozen=True)
class Stars:
    number: int

    def __post_init__(self) -> None:
        assert 1 <= self.number <= 10, f"{self}"


def f1(s: Stars) -> Stars:
    return Stars(s.number + 5)


def f2(s: Stars) -> Stars:
    return Stars(s.number * 5)


stars1 = Stars(4)
print(stars1)
## Stars(number=4)
print(f1(stars1))
## Stars(number=9)
with Catch():
    print(f2(f1(stars1)))
## Error: Stars(number=45)
with Catch():
    stars2 = Stars(11)
## Error: Stars(number=11)
with Catch():
    print(f1(Stars(11)))
## Error: Stars(number=11)
```

Subsequent functions operating on `Stars` no longer require redundant checks.
Modifying a `Stars` instance after creation raises an error, further safeguarding the data integrity:

```python
# example_4.py
# from stars import Stars

# def increase_stars(rating: Stars, increment: int) -> Stars:
#    return Stars(rating.stars + increment)
```

If this function tries to create an invalid rating, the data class validation immediately raises an error.
This greatly simplifies code maintenance and readability.

Additionally, immutable objects can safely serve as keys in dictionaries, allowing reliable data lookups and caching.

### NamedTuple

In many cases, a `NamedTuple` can be used in lieu of a frozen `dataclass`.
A `NamedTuple` combines `tuple` immutability with type annotations and named fields:

```python
# named_tuple.py
from typing import NamedTuple


class Coordinates(NamedTuple):
    latitude: float
    longitude: float


coords = Coordinates(51.5074, -0.1278)
print(coords)
## Coordinates(latitude=51.5074,
## longitude=-0.1278)
print(coords.latitude)
## 51.5074
# coords.latitude = 123.4567 # Runtime error
```

`NamedTuple` provides clarity, immutability, and easy unpacking, ideal for structured data.
Their simplicity makes them ideal for simple, lightweight, immutable record types.
For brevity and cleanliness, this book will use `NamedTuple`s instead of frozen `dataclass`es whenever possible.

Both `NamedTuple` and `dataclass` automate the creation of common methods
(such as constructors, `repr`, equality, and sometimes hash methods),
but they do so in different ways and with different design goals in mind.

Rather than generating an `__init__`,
a `NamedTuple` is a subclass of `tuple` and uses a generated `new` method to create instances.
Customization of construction logic is limited because you cannot define an init
(instead, you override new if needed, which is more cumbersome).
`NamedTuple` instances are immutable since they are `tuple` subclasses, so you cannot assign to their fields after creation.
A `NamedTuple` automatically generates a `repr` that prints the field names along with their values
(e.g., Point(x=1, y=2)) in a manner similar to a standard `tuple` representation.
An `__eq__` is generated based on the `tuple`’s content,
and `__hash__` is automatically defined (since `tuple`s are immutable).
`NamedTuple`s inherit `tuple` ordering (lexicographical order) by default.
`NamedTuple` is a subclass of `tuple`, which means all `tuple` operations (indexing, iteration, etc.) work as expected.
Since a `NamedTuple` is implemented as a `tuple` (with immutability and slots by default), it is memory efficient.

A `dataclass` generates an `__init__` that assigns the provided arguments to instance attributes.
By default, `dataclass` instances are mutable; however, you can set `frozen=True` to make them immutable.
This causes the generated `__init__` to assign to immutable fields.
The `repr` method is automatically generated to include the field names and their current values.
It is highly customizable via the `repr` parameter on fields.
By default, `dataclass` automatically generates an eq method that compares instances based on their fields.
If the `dataclass` is mutable (`frozen=False`, which is default), no hash is generated by default
(unless you specifically use `unsafe_hash=True`).
Mutable objects of any kind should generally not be hashed because the hash can change from one access to another.
If the `dataclass` is frozen (immutable), then a hash method is automatically provided.
You can add ordering methods (e.g., lt, le, etc.) by setting `order=True` when declaring the `dataclass`. 
Otherwise, no ordering is generated.
Dataclasses provide a post_init method that runs immediately after the generated init method.
This is a convenient place for additional initialization or validation.
Dataclasses offer per-field customization (default values, default_factory, comparison options, etc.)
that allows fine-tuning of instances behavior.

### Composing Data Classes

Composition, another functional programming cornerstone, creates complex data types from simpler ones.
Consider a `Person` object composed of `FullName`, `BirthDate`, and `Email` data classes:

```python
# dataclass_composition.py
from dataclasses import dataclass


@dataclass(frozen=True)
class FullName:
    name: str

    def __post_init__(self) -> None:
        print(f"FullName checking {self.name}")
        assert len(self.name.split()) > 1, (
            f"'{self.name}' needs first and last names"
        )


@dataclass(frozen=True)
class BirthDate:
    dob: str

    def __post_init__(self) -> None:
        print(f"BirthDate checking {self.dob}")


@dataclass(frozen=True)
class EmailAddress:
    address: str

    def __post_init__(self) -> None:
        print(f"EmailAddress checking {self.address}")


@dataclass(frozen=True)
class Person:
    name: FullName
    date_of_birth: BirthDate
    email: EmailAddress


person = Person(
    FullName("Bruce Eckel"),
    BirthDate("7/8/1957"),
    EmailAddress("mindviewinc@gmail.com"),
)
## FullName checking Bruce Eckel
## BirthDate checking 7/8/1957
## EmailAddress checking mindviewinc@gmail.com
print(person)
## Person(name=FullName(name='Bruce Eckel'),
## date_of_birth=BirthDate(dob='7/8/1957'), email=
## EmailAddress(address='mindviewinc@gmail.com'))
```

This hierarchical validation structure ensures correctness and clarity at every composition level.
Invalid data never propagates, vastly simplifying subsequent interactions.

## Enumerations

An `Enum` is also a type and is preferable when you have a smaller set of values.
`Enum`s provide additional type safety for fixed-value sets

```python
# param_keyword.py
from enum import Enum

class ParamKeyword(Enum):
    MIN = "MIN"
    MAX = "MAX"
    DEF = "DEF"

ParamType = float | ParamKeyword
```


such as months:

```python
# birth_date.py
# "Leap years are left as an exercise."
from dataclasses import dataclass
from enum import Enum

from book_utils import Catch


@dataclass(frozen=True)
class Day:
    n: int

    def __post_init__(self) -> None:
        assert 1 <= self.n <= 31, f"{self}"


@dataclass(frozen=True)
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
        assert 1 <= month_number <= 12, (
            f"Month({month_number})"
        )
        return list(Month)[month_number - 1]

    def check_day(self, day: Day):
        assert day.n <= self.value[1], f"{self} {day}"

    def __repr__(self):
        return self.name


@dataclass(frozen=True)
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
## BirthDate(m=DECEMBER, d=Day(n=31),
## y=Year(n=2022))
## ------------------------------
```

`Month` can be created using `dataclass`es, but it's more complicated than using `Enum`, with questionable benefits:

```python
# month_data_class.py
from dataclasses import dataclass, field

from book_utils import Catch


@dataclass(frozen=True)
class Day:
    n: int

    def __post_init__(self) -> None:
        assert 1 <= self.n <= 31, f"Day({self.n})"


@dataclass(frozen=True)
class Year:
    n: int

    def __post_init__(self) -> None:
        assert 1900 < self.n <= 2022, f"Year({self.n})"


@dataclass(frozen=True)
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


@dataclass(frozen=True)
class Months:
    months: list[Month] = field(
        default_factory=Month.make_months
    )

    def number(self, month_number: int):
        assert 1 <= month_number <= 12, (
            f"Month({month_number})"
        )
        return self.months[month_number - 1]


@dataclass(frozen=True)
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
## BirthDate(m=Month(name='July', n=7,
## max_days=31), d=Day(n=8), y=Year(n=1957))
## ------------------------------
## (0, 32, 1857)
## Error: Month(0)
## (2, 31, 2022)
## Error: Month(name='February', n=2, max_days=28)
## Day(n=31)
## (9, 31, 2022)
## Error: Month(name='September', n=9,
## max_days=30) Day(n=31)
## (4, 31, 2022)
## Error: Month(name='April', n=4, max_days=30)
## Day(n=31)
## (6, 31, 2022)
## Error: Month(name='June', n=6, max_days=30)
## Day(n=31)
## (11, 31, 2022)
## Error: Month(name='November', n=11,
## max_days=30) Day(n=31)
## (12, 31, 2022)
## BirthDate(m=Month(name='December', n=12,
## max_days=31), d=Day(n=31), y=Year(n=2022))
## ------------------------------
```

Using `Enum`s makes code both readable and safely constrained, improving robustness.
For simplicity and IDE interactivity, choose `Enum`s over data classes for fixed-value sets.

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

`Literal`s can serve as a lightweight substitute for `Enum`s when you only need to restrict values at the type level
and do not require the additional runtime features of `Enum`s. 
This makes `Literal`s attractive for scenarios
like defining a parameter that only accepts a small set of constant values without adding extra code complexity.

### Similarities
- Value Restriction:  
  Both `Literal`s and `Enum`s let you restrict a variable to a fixed set of values.
  For example, `ParamType = Union[float, Literal["MIN", "MAX", "DEF"]]`
  tells a type checker that only these string values are allowed (aside from floats),
  similar to how an `Enum` restricts possible members.

### Differences
- Type Checking vs. Runtime Behavior:
  - `Literal`: `Literal`s are a static type hint introduced in PEP 586. They exist solely for type checking and do not create a distinct runtime type. The type checker (and your IDE) knows that only those exact values are allowed, but at runtime, they are just ordinary values (e.g., ordinary strings).
  - `Enum`: An `Enum` is a real class (inheriting from `enum.Enum`) that creates distinct runtime objects. `Enum`s provide additional functionality like iteration over members, comparison, and custom methods. They work both at runtime and during static type checking.

- Overhead and Simplicity:
  - `Literal`: Using `Literal`s is simple and lightweight if you just want to specify allowed constant values. There’s no additional boilerplate, so it’s a good choice when you only need type constraints.
  - `Enum`: `Enum`s come with more structure and can encapsulate behavior. However, they require defining a class and are slightly heavier in terms of syntax and runtime footprint.

### Choosing between `Literal` and `Enum`
- Use `Literal`s if:
  - You need a simple, compile-time constraint on allowed values without extra runtime behavior.
  - You want minimal boilerplate and are comfortable relying on your static type checker and IDE for guidance.

- Use `Enum`s if:
  - You need runtime features, such as iterating over allowed values, custom methods, or more semantic richness (e.g., when each value might need its own behavior or additional attributes).
  - You want a self-documenting interface that clearly models a set of related constants as a distinct type.

Both approaches improve type safety,
but if you need more robust functionality or runtime introspection, an `Enum` might be the better choice.

### Converting a `Literal` to a `Set`

You can write an expression that looks like it's checking for membership in a `Literal` but it won't work:

```python
# literal_to_set.py
from typing import Literal

ParamVal = Literal["DEF", "MIN", "MAX"]
print(ParamVal)
print("MIN" in ParamVal)
print("NOPE" in ParamVal)

# Convert literal values to a set:
allowed_set = set(ParamVal.__args__)  # type: ignore
print(allowed_set)
print("MIN" in allowed_set)
print("NOPE" in allowed_set)
```

To check for membership, you must convert it to a `set` using the `__args__` property.

## Choosing Between `Enum`, `Literal`, and `Set`

Each approach has its strengths and trade‐offs.
The best choice depends on your requirements for type safety, runtime behavior, and code clarity.

### `Literal`

Pros:
- Static Type Safety: Type checkers can enforce that only the allowed constant values appear in your code.
- Minimal Overhead: `Literal`s have no runtime cost; they serve solely as hints at the type level.
- Simplicity: Using literals is straightforward and requires no extra boilerplate code.

Cons:
- No Runtime Distinction: At runtime, `"MIN"`, `"MAX"`, and `"DEF"` are ordinary strings. 
  You lose benefits like custom methods or iteration over members.
- Limited Expressiveness: `Literal`s only provide type-checking constraints and no additional behavior beyond that.

When to Use:
- Use `Literal`s when you need to enforce a small set of constant values at the type level, and you are comfortable relying on static type checkers and IDEs for guidance.
- They are ideal for simple cases where you want to ensure that only a few specific string values (alongside other types, like numbers) are accepted.

### `Enum`

`Enum`s create a distinct type at runtime and define a collection of symbolic names bound to constant values. For example:



Pros:
- Runtime Features: `Enum`s are real classes at runtime, so they support iteration, comparison, and custom methods.
- Clarity and Self-Documentation: Using an `Enum` clearly signals that the parameter is one of a predetermined, fixed set. 
  IDE autocompletion can also list the valid members.
- Extra Functionality: You can add methods or properties to an `Enum` if the values need to carry extra meaning (for instance, mapping to specific instrument settings).

Cons:
- Additional Overhead: `Enum`s require a bit more code and syntax compared to `Literal`s.
- Slightly Heavier: While typically negligible, there is a bit more runtime overhead as `Enum`s are actual objects.

When to Use:
- Use `Enum`s when you need not only type safety at the static level but also runtime assurance--such as when you need to iterate over allowed options or attach extra behavior.
- `Enum`s are excellent for cases where the set of allowed values is fixed, and you might want to use them throughout your codebase in a uniform, well-documented manner.

### `Set`

A set is a built-in Python data structure that holds unique elements.
In the context of allowed values, you might define
`ALLOWED_KEYWORDS = {"MIN", "MAX", "DEF"}`

Pros:
- Dynamic Membership Testing: `Set`s allow you to easily check if a given value is in the allowed collection using the `in` operator.
- Runtime Flexibility: You can modify the set at runtime if needed (though for constants this might not be necessary).
- Simplicity in Validation: When writing custom validation code, a set easily confirms membership.

Cons:
- Not a Type Annotation: `Set`s do not integrate with static type checkers. They only serve at runtime to check if a value belongs to the allowed set.
- No Static Safety: Unlike `Literal`s or `Enum`s, sets don’t give you compile-time guarantees or IDE autocompletion for allowed values.

When to Use:
- Use sets for runtime validation where you need a simple way to confirm membership (e.g., inside a helper function that checks if a value is valid).
- They are ideal when the allowed values are defined once and only used for dynamic checks, not for type annotations.

### Choosing

Each approach has its specific use cases:
- `Literal`s provide a quick and easy way to inform static type checkers without extra runtime behavior.
- `Enum`s add clarity and runtime functionality at the cost of a little extra complexity.
- `Set`s work well if your validation is purely runtime-oriented and you don’t need the additional benefits of static type restrictions.

Choosing between them depends on whether you prioritize compile-time type checking and better IDE support
(favoring `Literal`s or `Enum`s) or need flexible, dynamic validation (favoring `set`s).
In many cases, combining these approaches can be effective--for example,
using `Literal`s in type annotations and a `set` for quick runtime membership checks in helper functions.

## TypedDicts for Structured Data

`TypedDict` is useful when defining dictionary structures with known keys and typed values:

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


settings: UserSettings = {"theme": "dark"}
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
## User(id=1, name='Alice', status=<Status.ACTIVE:
## 'active'>)
```

## Domain-Driven Design (DDD)

Strongly typed domain models help clearly represent domain logic, improving robustness and maintainability.
Define domain entities explicitly to enhance domain logic expressiveness:

```python
# ddd.py
from dataclasses import dataclass
from typing import NamedTuple


class Product(NamedTuple):
    name: str
    price: float


@dataclass
class Order:
    order_id: int
    products: list[Product]

    def total(self) -> float:
        return sum(
            product.price for product in self.products
        )
```

Strongly typed domain models help catch issues early, facilitating clearer, safer, and more maintainable codebases.

## The Power of Custom Types

Creating custom types simplifies managing data integrity and composition,
reduces repetitive checks, and centralizes validation.
Combined with functional programming principles like immutability and type composition,
custom types significantly enhance the clarity, maintainability, and robustness of your code.
Once you adopt this approach, you'll find your development process smoother, more reliable, and far more enjoyable.

## (Generated) Dataclass Intro Notes

Dataclasses simplify class definitions by automatically generating methods like `__init__`, `__repr__`, and `__eq__`:

```python
# generated_methods.py
from dataclasses import dataclass


@dataclass
class Product:
    name: str
    price: float
    in_stock: bool = True


product = Product("Laptop", 999.99)
print(product)
## Product(name='Laptop', price=999.99,
## in_stock=True)
```

Dataclasses reduce boilerplate, ensuring concise and readable class definitions.

Dataclasses support default factories, immutability, and more:

```python
# example_9.py
from dataclasses import dataclass, field
from book_utils import Catch


@dataclass(frozen=True)
class Order:
    order_id: int
    items: list[str] = field(default_factory=list)


order = Order(order_id=123)
with Catch():
    order.order_id = 456
## Error: cannot assign to field 'order_id'
```
