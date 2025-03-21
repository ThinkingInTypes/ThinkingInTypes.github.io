# Dataclasses

<https://github.com/BruceEckel/DataClassesAsTypes>

This chapter began as a presentation at a Python conference, inspired by conversations with fellow programmers exploring functional programming techniques. Specifically, the idea arose from a podcast discussion about Scala's smart types. After extensive study of functional programming, several concepts coalesced into an approach that leverages Python’s data classes effectively. This chapter aims to share those insights and illustrate the practical benefits of Python data classes, guiding you towards clearer, more reliable code.

## The Initial Problem: Ensuring Correctness

Imagine building a simple customer feedback system using a rating from one to ten stars. Traditionally, Python programmers use an integer type, checking its validity whenever it's used:

```python
def rate_stars(stars: int):
    assert 1 <= stars <= 10, "Stars rating must be between 1 and 10."
    # use stars safely
```

However, each time the integer is used, its validity must be rechecked, leading to duplicated logic, scattered validation, and potential mistakes.

## Traditional Object-Oriented Encapsulation

Object-oriented programming (OOP) suggests encapsulating validation within the class. Python typically uses a private attribute to ensure encapsulation:

```python
class Stars:
    def __init__(self, stars: int):
        assert 1 <= stars <= 10, "Stars rating must be between 1 and 10."
        self._stars = stars

    @property
    def stars(self):
        return self._stars
```

This approach centralizes validation, yet remains cumbersome. Each method interacting with the attribute still requires pre- and post-condition checks, cluttering the code and potentially introducing errors if a developer neglects these checks.

## Introducing Python Data Classes

Data classes, introduced in Python 3.7, significantly streamline this process by generating essential methods automatically. They provide a structured, concise way to define data-holding objects:

```python
from dataclasses import dataclass

@dataclass
class Stars:
    stars: int

    def __post_init__(self):
        assert 1 <= self.stars <= 10, "Stars rating must be between 1 and 10."
```

Here, validation logic resides exclusively in the `__post_init__` method, executed automatically after initialization. This guarantees that only valid `Stars` instances exist. Subsequent functions operating on `Stars` no longer require redundant checks:

```python
def increase_stars(rating: Stars, increment: int) -> Stars:
    return Stars(rating.stars + increment)
```

If this function tries to create an invalid rating, the data class validation immediately raises an error. This greatly simplifies code maintenance and readability.

## Immutable Data Classes and Functional Programming

Functional programming strongly advocates immutability, preventing accidental changes and thus simplifying reasoning about your code. Python data classes support immutability through a `frozen=True` parameter:

```python
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

## Conclusion

Python data classes simplify managing data integrity and composition, reducing repetitive checks and centralizing validation. Combined with functional programming principles like immutability and type composition, data classes significantly enhance the clarity, maintainability, and robustness of your code. Once you adopt this method, you'll find your development process smoother, more reliable, and enjoyable.

> This placeholder text was generated by ChatGPT 4.5.
> It will be significantly rewritten as the book is developed.
> In the meantime you can add comments to either <https://bsky.app/bruceeckel> or [Github Issues](https://github.com/ThinkingInTypes/ThinkingInTypes.github.io/issues).

## Misunderstanding Class Attributes

A number of type tools hack the class attribute syntax; the most obvious is dataclasses but there are others.
It's important to understand that this is special behavior created by the tool, and that ordinary classes do not behave this way.
Read the [Class Attributes] appendix for deeper understanding.

## Using Dataclasses Effectively

Dataclasses simplify class definitions by automatically generating methods like `__init__`, `__repr__`, and `__eq__`:

```python
# example_1.py
from dataclasses import dataclass


@dataclass
class Product:
    name: str
    price: float
    in_stock: bool = True


product = Product("Laptop", 999.99)
print(product)  # Product(name='Laptop', price=999.99, in_stock=True)
```

Dataclasses reduce boilerplate, ensuring concise and readable class definitions.

### Advanced Dataclass Features

Dataclasses support default factories, immutability, and more:

```python
# example_2.py
from dataclasses import dataclass, field
from typing import List


@dataclass(frozen=True)
class Order:
    order_id: int
    items: List[str] = field(default_factory=list)


order = Order(order_id=123)
# order.order_id = 456  # Error: dataclass is frozen (immutable)
```
