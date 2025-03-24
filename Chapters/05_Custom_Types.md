# Custom Types

- Add variations: NamedTuple, Enum
- Incorporate examples from <https://github.com/BruceEckel/DataClassesAsTypes>

This chapter began as a presentation at a Python conference, inspired by conversations with fellow programmers exploring functional programming techniques. Specifically, the idea arose from a podcast discussion about Scala's smart types. After extensive study of functional programming, several concepts coalesced into an approach that leverages Python’s data classes effectively. This chapter aims to share those insights and illustrate the practical benefits of Python data classes, guiding you towards clearer, more reliable code.

## Misunderstanding Class Attributes

This chapter contains additional tools that modify the normal behavior of class attributes.
It's important to understand that this behavior is created by the tool, and that ordinary classes do not behave this way.
Read the [Class Attributes] appendix for deeper understanding.

## The Initial Problem: Ensuring Correctness

Imagine building a simple customer feedback system using a rating from one to ten stars. Traditionally, Python programmers use an integer type, checking its validity whenever it's used:

```python
# example_1.py
def rate_stars(stars: int):
    assert 1 <= stars <= 10, "Stars rating must be between 1 and 10."
    # use stars safely
```

However, each time the integer is used, its validity must be rechecked, leading to duplicated logic, scattered validation, and potential mistakes.

## Traditional Object-Oriented Encapsulation

Object-oriented programming (OOP) suggests encapsulating validation within the class. Python typically uses a private attribute to ensure encapsulation:

```python
# example_2.py
class Stars:
    def __init__(self, stars: int):
        assert 1 <= stars <= 10, "Stars rating must be between 1 and 10."
        self._stars = stars

    @property
    def stars(self):
        return self._stars
```

This approach centralizes validation, yet remains cumbersome. Each method interacting with the attribute still requires pre- and post-condition checks, cluttering the code and potentially introducing errors if a developer neglects these checks.

## Data Classes

Data classes, introduced in Python 3.7, significantly streamline this process by generating essential methods automatically. They provide a structured, concise way to define data-holding objects:

```python
# example_3.py
from dataclasses import dataclass


@dataclass
class Stars:
    stars: int

    def __post_init__(self):
        assert 1 <= self.stars <= 10, "Stars rating must be between 1 and 10."
```

Here, validation logic resides exclusively in the `__post_init__` method, executed automatically after initialization. This guarantees that only valid `Stars` instances exist. Subsequent functions operating on `Stars` no longer require redundant checks:

```python
# example_4.py
def increase_stars(rating: Stars, increment: int) -> Stars:
    return Stars(rating.stars + increment)
```

If this function tries to create an invalid rating, the data class validation immediately raises an error. This greatly simplifies code maintenance and readability.

## Immutable Data Classes and Functional Programming

Functional programming strongly advocates immutability, preventing accidental changes and thus simplifying reasoning about your code. Python data classes support immutability through a `frozen=True` parameter:

```python
# example_5.py
from dataclasses import dataclass


@dataclass(frozen=True)
class Stars:
    stars: int

    def __post_init__(self):
        assert 1 <= self.stars <= 10, "Stars rating must be between 1 and 10."
```

Now, modifying a `Stars` instance after creation raises an error, further safeguarding the data integrity. Additionally, immutable objects can safely serve as keys in dictionaries, allowing reliable data lookups and caching.

## Composing Data Classes

Composition, another functional programming cornerstone, allows building complex data types from simpler ones. Consider a `Person` object composed of `FullName`, `BirthDate`, and `Email` data classes:

```python
# example_6.py
from dataclasses import dataclass


@dataclass(frozen=True)
class FullName:
    name: str

    def __post_init__(self):
        parts = self.name.split()
        assert len(parts) >= 2, "Full name must include at least two parts."


@dataclass(frozen=True)
class BirthDate:
    year: int
    month: int
    day: int

    def __post_init__(self):
        assert 1900 <= self.year <= 2022, "Year must be between 1900 and 2022."
        assert 1 <= self.month <= 12, "Month must be between 1 and 12."
        assert 1 <= self.day <= 31, "Day must be valid for given month."


@dataclass(frozen=True)
class Email:
    address: str

    def __post_init__(self):
        assert "@" in self.address, "Invalid email address."


@dataclass(frozen=True)
class Person:
    name: FullName
    birthdate: BirthDate
    email: Email
```

This hierarchical validation structure ensures correctness and clarity at every composition level. Invalid data never propagates, vastly simplifying subsequent interactions.

## Leveraging Enums for Type Safety

Enums provide additional type safety for fixed-value sets, such as months:

```python
# example_7.py
from enum import Enum


class Month(Enum):
    JANUARY = (1, 31)
    FEBRUARY = (2, 28)
    # other months

    @staticmethod
    def validate(month_number: int, day: int) -> bool:
        month = Month(month_number)
        return 1 <= day <= month.value[1]
```

Using enums makes code both readable and safely constrained, improving robustness. Enums clearly outperform data classes for fixed-value sets due to simplicity and compile-time definitions.

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
print(coords.latitude)
# coords.latitude = 123.4567 # Runtime error
```

`NamedTuple` provides clarity, immutability, and easy unpacking, ideal for simple structured data.
For brevity and cleanliness, this book will used `NamedTuple`s instead of frozen `dataclass`es whenever possible.

### Leveraging TypedDicts for Structured Data

`TypedDict` is useful when defining dictionary structures with known keys and typed values:

```python
# typed_dict.py
from typing import TypedDict


class UserProfile(TypedDict):
    username: str
    email: str
    age: int


user: UserProfile = {"username": "alice", "email": "alice@example.com", "age": 30}
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


user = User(id=1, name="Alice", status=Status.ACTIVE)
print(user)
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
        return sum(product.price for product in self.products)
```

Strongly-typed domain models help catch issues early, facilitating clearer, safer, and more maintainable codebases.

## Conclusion

Python data classes simplify managing data integrity and composition, reducing repetitive checks and centralizing validation. Combined with functional programming principles like immutability and type composition, data classes significantly enhance the clarity, maintainability, and robustness of your code. Once you adopt this method, you'll find your development process smoother, more reliable, and enjoyable.

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
