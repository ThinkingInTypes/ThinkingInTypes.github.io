# Generics

## Defining Custom Generics with `TypeVar` and `Generic`

Custom generics allow functions and classes to handle various types flexibly:

### Using `TypeVar`

```python
# example_1.py
from typing import TypeVar

T = TypeVar("T")


def first_item(items: list[T]) -> T:
    return items[0]


print(first_item([1, 2, 3]))  # returns int
## 1
print(first_item(["a", "b"]))  # returns str
## a
```

### Generic Classes

```python
# example_2.py
from dataclasses import dataclass
from typing import Generic, TypeVar

T = TypeVar("T")  # Declare a type variable


@dataclass
class Box(Generic[T]):
    content: T


box_int = Box(123)  # Box[int]
box_str = Box("hello")  # Box[str]
```

Custom generics enhance code reusability and type safety.

## Using Constraints and Bounds with Generics

Generics can include constraints and bounds to restrict allowed types:

### Constraints

```python
# example_3.py
from typing import TypeVar

U = TypeVar("U", int, float)


def add(a: U, b: U) -> U:
    return a + b


add(1, 2)  # valid
add(1.5, 2.5)  # valid
# add("a", "b")  # invalid, detected by type checker
```

### Bounds

```python
# example_4.py
from typing import TypeVar


class Animal:
    def speak(self) -> str:
        return "..."


A = TypeVar("A", bound=Animal)


def animal_sound(animal: A) -> str:
    return animal.speak()


class Dog(Animal):
    def speak(self) -> str:
        return "Woof!"


print(animal_sound(Dog()))  # "Woof!"
## Woof!
```

Constraints and bounds improve specificity in generic type annotations, enhancing code clarity and correctness.

## Variance, Covariance, and Contravariance in Generics

Variance controls type relationships between generic types:

### Covariance (`covariant=True`)

Allows using subtypes in place of parent types:

```python
# example_7.py
from typing import Generic, TypeVar

T_co = TypeVar("T_co", covariant=True)


class ReadOnlyList(Generic[T_co]):
    def __init__(self, items: list[T_co]):
        self.items = items


ints: ReadOnlyList[int] = ReadOnlyList([1, 2, 3])
numbers: ReadOnlyList[float] = (
    ints  # Valid due to covariance
)
```

### Contravariance (`contravariant=True`)

Allows using parent types in place of subtypes, common in callbacks or consumers:

```python
# example_8.py
from typing import TypeVar, Generic

T_contra = TypeVar("T_contra", contravariant=True)


class Processor(Generic[T_contra]):
    def process(self, value: T_contra) -> None:
        print(value)


int_processor: Processor[int] = Processor()
number_processor: Processor[float] = (
    int_processor  # Valid due to contravariance
)
```

Understanding variance ensures accurate type relationships, especially when designing flexible APIs or libraries.

## Currying

Currying is the process of transforming a function that takes multiple arguments into a series of functions that each take a single argument.
Python doesn’t intrinsically support currying the way functional languages like Haskell do, but you can implement it with the `functools` module:

```python
# pseudo_currying.py
from functools import partial


def add(x: int, y: int) -> int:
    return x + y


add_five = partial(add, 5)
print(add_five(3))
## 8
```

`partial()` doesn’t strictly curry, but lets you fix some arguments and get back a new function.

Here's a generic curry decorator for any two-arg function:

```python
# generic_currying_decorator.py
from typing import Callable, TypeVar

A = TypeVar("A")
B = TypeVar("B")
C = TypeVar("C")


def curry(
        func: Callable[[A, B], C],
) -> Callable[[A], Callable[[B], C]]:
    def outer(a: A) -> Callable[[B], C]:
        def inner(b: B) -> C:
            return func(a, b)

        return inner

    return outer


@curry
def multiply(x: int, y: int) -> int:
    return x * y


times_ten = multiply(10)
print(times_ten(3))
## 30
```
