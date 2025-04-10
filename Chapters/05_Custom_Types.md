# Custom Types

- Add variations:
  NamedTuple, Enum
- Incorporate examples from <https://github.com/BruceEckel/DataClassesAsTypes>

This chapter began as a presentation at a Python conference, inspired by conversations with fellow programmers exploring functional programming techniques.
Specifically, the idea arose from a podcast discussion about Scala's smart types.
After extensive study of functional programming, several concepts coalesced into an approach that leverages Python’s data classes effectively.
This chapter aims to share those insights and illustrate the practical benefits of Python data classes, guiding you towards clearer, more reliable code.

## Misunderstanding Class Attributes

This chapter contains additional tools that modify the normal behavior of class attributes.
It's important to understand that this behavior is created by the tool, and that ordinary classes do not behave this way.
Read the [Class Attributes](A06_Class_Attributes.md) appendix for deeper understanding.

## The Initial Problem: Ensuring Correctness

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
with Catch():
    print(stars3.f1(4))
## 9
with Catch():
    print(stars3.f2(22))
## Error: Stars(9): 22
# @property without setter prevents mutation:
# stars1.number = 99
# AttributeError: can't set attribute 'number'
```

This approach centralizes validation, yet remains cumbersome.
Each method interacting with the attribute still requires pre-and post-condition checks, cluttering the code and potentially introducing errors if a developer neglects these checks.

## Data Classes

Data classes, introduced in Python 3.7, significantly streamline this process by generating essential methods automatically.
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

In a `dataclass`, validation logic resides exclusively in the `__post_init__` method, executed automatically after initialization.
This guarantees that only valid `Stars` instances exist.

## Immutable Data Classes and Functional Programming

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

## Composing Data Classes

Composition, another functional programming cornerstone, allows building complex data types from simpler ones.
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

## Literal Types

Literal types allow specifying exact permissible values, enhancing type specificity and correctness:

```python
# literal_types.py
from typing import Literal


def set_mode(mode: Literal["auto", "manual"]) -> None:
    print(f"Mode set to {mode}")


set_mode("auto")  # valid
## Mode set to auto
# set_mode('automatic')  # invalid, detected by type checker
```

Literal types ensure values match expected exact constants, improving type safety.

## Leveraging Enums for Type Safety

An Enum is also a type, and is preferable when you have a smaller set of values.
Enums provide additional type safety for fixed-value sets, such as months:

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

```python
# month_data_class.py
from dataclasses import dataclass, field
from typing import List

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
    months: List[Month] = field(
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

`Month` can be created using dataclasses, but it's more complicated than using `Enum`, with questionable benefits.

Using enums makes code both readable and safely constrained, improving robustness.
For simplicity and IDE interactivity, choose enums over data classes for fixed-value sets.

## Specialized Tools

### Typed NamedTuples

A typed `NamedTuple` combines tuple immutability with type annotations and named fields:

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
For brevity and cleanliness, this book will used `NamedTuple`s instead of frozen `dataclass`es whenever possible.

[what generated methods are different between NamedTuple and dataclass?]

### Leveraging TypedDicts for Structured Data

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

### Optional Fields in TypedDict

You can specify optional fields using `NotRequired` (Python 3.11+) or `total=False`:

```python
# optional_typed_dict_fields.py
from typing import TypedDict, NotRequired


class UserSettings(TypedDict):
    theme: str
    notifications_enabled: NotRequired[bool]


settings: UserSettings = {"theme": "dark"}
```

This flexibility allows clear definitions for complex, partially-optional data structures.

## Combining Dataclasses and Enums

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

Strongly-typed domain models help clearly represent domain logic, improving robustness and maintainability.
Define domain entities explicitly to enhance domain logic expressiveness:

```python
# ddd.py
from dataclasses import dataclass
from typing import List, NamedTuple


class Product(NamedTuple):
    name: str
    price: float


@dataclass
class Order:
    order_id: int
    products: List[Product]

    def total(self) -> float:
        return sum(
            product.price for product in self.products
        )
```

Strongly-typed domain models help catch issues early, facilitating clearer, safer, and more maintainable codebases.

## Conclusion

Python data classes simplify managing data integrity and composition, reducing repetitive checks and centralizing validation.
Combined with functional programming principles like immutability and type composition, data classes significantly enhance the clarity, maintainability, and robustness of your code.
Once you adopt this method, you'll find your development process smoother, more reliable, and enjoyable.

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
from typing import List


@dataclass(frozen=True)
class Order:
    order_id: int
    items: List[str] = field(default_factory=list)


order = Order(order_id=123)
# order.order_id = 456  # Error: dataclass is frozen (immutable)
```
