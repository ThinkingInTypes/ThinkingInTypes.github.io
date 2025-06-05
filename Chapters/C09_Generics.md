# Generics

Generics in Python produce flexible, reusable code that remains type-safe.
They enable the definition of classes, functions, and types that can operate on a variety of types while preserving type
information.
With generics, you can avoid writing duplicate code for similar operations on different types and catch type errors
early during development.

TODO: Probably divide this into "Generics" here and "Advanced Generics" at the end of the book.

## Defining Custom Generics

Python directly supports *parameterized types*.
This declares a *type variable* as a placeholder for an arbitrary type.

### Generic Functions

For functions, a type variable enables the function to accept and return values of the same arbitrary type.
Here is a generic function expressing identity:

```python
# generic_function.py


def identity[T](value: T) -> T:
    return value


print(identity(42))
## 42
print(identity("Hello"))
## Hello
```

Here, the type variable `T` contains the type of both the `value` parameter and the return type.
The type checker enforces that both are the same type.
If you call `identity(42)`, `T` is inferred as `int`, so the function takes returns an `int`.
For `identity("Hello")`, `T` is `str`.
Thus, this function works for any type but always returns the same type it is given.

Generic functions are useful for algorithms that work uniformly on multiple types.
Common examples include utility functions like `identity`, data retrieval functions that return the type of whatever
they fetch, or factory functions that construct objects of a type.

### Old Syntax

Originally, type variables had to be explicitly declared using `TypeVar`:

```python
# typevars.py
from typing import TypeVar

T = TypeVar("T")  # Define a TypeVar named T


def identity(value: T) -> T:
    return value


print(identity(42))
## 42
print(identity("Hello"))
## Hello
```

Python 3.12 removed this requirement, improving the syntax significantly.
This book uses the modern syntax, but you may come across older code that uses `TypeVar`s.

### Generic Classes

For classes, generics allow the class to operate on or store various types without sacrificing type safety.
Here's a generic class `Box` that can hold a value of any type:

```python
# box.py
from dataclasses import dataclass


@dataclass
class Box[U]:
    content: U

    def get_content(self) -> U:
        # reveal_type(self.content)
        return self.content


int_box = Box(123)  # U is inferred as int
str_box = Box("Python")  # U is inferred as str
print(int_box.get_content())
## 123
print(str_box.get_content())
## Python
```

`Box` is a generic class parameterized by `U`.
When we create `Box(123)`, the type checker knows `U` is `int` for that instance.
For `Box("Python")`, `U` is `str` (`Box[str]`).
The attribute `content` and return type of `get_content` are accordingly typed.

The class definition `class Box[U]` tells the type system that `Box` has a type parameter `U`.
At runtime, `Box` is just a normal class (after all, Python's generics are mostly static and erased at runtime), but for
type checking, `Box[int]` and `Box[str]` are treated as different instantiations of the generic class.
This prevents, for example, accidentally putting a `str` into a `Box[int]`.

Note that we did not explicitly write `Box[int]` or `Box[str]` when constructing the boxes.
The type checker infers `U` from the constructor argument.
We can also annotate variables or parameters with explicit instantiations like `Box[int]` if needed.

## Constraints and Bounds on Type Variables

Sometimes you want a type variable to be limited to certain types, rather than truly any type.
Python's typing provides two mechanisms for this: *constraints* and *bounds*.

### Constraints

You can specify an explicit finite set of allowable types for a type variable.
This is useful when a function or class should only work with specific types that aren't in an inheritance relationship.
In `add`, we constrain `Number` to be either an `int` or a `float`:

```python
# constrained_type_variable.py


def add[Number: (int, float)](a: Number, b: Number) -> Number:
    return a + b


add(5, 10)  # valid, both int
add(3.5, 2.5)  # valid, both float
# ERROR: cannot mix types:
add(5, 2.5)  # type: ignore
# ERROR: str not allowed for Number:
add("A", "Z")  # type: ignore
```

The `add` function will only accept *one* of those types for both its arguments--you cannot mix types.
Passing any type other than `int` or `float` produces a type checking error.

### Bounds

A bound restricts a type variable to subtypes of a given class (or to classes implementing a given protocol).
This is known as an *upper bound*.
For example, if we have a base class `Animal`, we might want a generic function to only accept subclasses of `Animal`:

```python
# animals.py
from dataclasses import dataclass
from typing import Optional


@dataclass
class Animal:
    name: Optional[str] = None

    def say(self) -> None:
        print(f"{self.name}: Animal sound")


class Dog(Animal):
    def say(self) -> None:
        print(f"{self.name}: Woof")


def speak[T: Animal](creatures: list[T]) -> None:
    for creature in creatures:
        creature.say()
```

`T` is bounded by `Animal`, meaning any substitution for `T` must be `Animal` or a subclass of `Animal`.
The `speak` function can then accept a list of `Animal` or any subtype (like `Dog`).
Inside the function, we know that each item has the `speak()` method (since everything is at least `Animal`).
If we tried to call `speak` with a list of something else (say `str` or `int`), the type checker rejects it.

```python
# animal_demo.py
from animals import Animal, Dog, speak
from book_utils import Catch

pets: list[Dog] = [Dog("Rags"), Dog("Spot")]
speak(pets)  # Dog is a subclass of Animal
## Rags: Woof
## Spot: Woof
speak([Animal("Mittens")])  # Animal is the bound
## Mittens: Animal sound
with Catch():
    speak(["bob"])  # type: ignore
```

Use constraints when the valid types are a specific set of unrelated types.
Use a bound when the valid types share a common base class or trait that you want to enforce.
Bounds are often more flexible, as new subclasses automatically fit the bound without changing the type variable definition.
Constraints are stricter and must be explicitly extended if a new type should be allowed.

### Multiple Type Variables and Relationships

You can use more than one type variable in a generic function or class.
For instance, consider a function that takes two parameters of possibly different types and returns a tuple containing
them:

```python
# multiple_type_variables.py


def pairify[A, B](x: A, y: B) -> tuple[A, B]:
    return x, y


result = pairify("Alice", 5)  # tuple[str, int]
```

Here `A` and `B` are independent type variables.
The type of `result` is a `tuple` whose first element is a `str` and second is an `int`, as inferred from the arguments.

Type variables can also depend on each other through constraints or bounds.
However, Python's typing does not allow directly expressing complex relationships (like saying two type variables must
be the same subtype of some base).
In such cases, it's common to use a single type variable in multiple places to indicate they must match.
You can also use protocols (discussed later) for more complex constraints.

## Type Variable Tuples

A _type variable tuple_ is like `*args`, but for types.
It defines generic classes and functions that accept a variable number of types,
creating more powerful and flexible type-safe abstractions.
This is called _variadic generics_.

Suppose you want a generic `TupleWrapper` that can handle any number of types.
Without type variable tuples, you'd have to manually define each arity.
With it, you can write:

```python
# tuple_wrapper.py


class TupleWrapper[*T]:
    def __init__(self, *values: *T):
        self.values = values


t1 = TupleWrapper(1)  # TupleWrapper[int]
t2 = TupleWrapper("a", 2, 3.14)  # TupleWrapper[str, int, float]
```

The type checker tracks the number and types of elements in `*T` individually.
Let's explore the type variable tuple by implementing a type-safe version of Python's built-in `zip()` function that works on
`tuple`s of different types:

```python
# variadic_zip.py


def zip_variadic[*T](
    *args: tuple[*T],
) -> tuple[tuple[*T], ...]:
    return tuple(zip(*args))


def unzip_variadic[*T](
    packed: tuple[tuple[*T], ...],
) -> tuple[tuple[*T], ...]:
    return tuple(zip(*packed))


a: tuple[int, str, float] = (1, "a", 3.14)
b: tuple[int, str, float] = (2, "b", 2.71)
c: tuple[int, str, float] = (3, "c", 1.41)

zipped = zip_variadic(a, b, c)
unzipped = unzip_variadic(zipped)

print(f"Zipped: {zipped}")
## Zipped: ((1, 2, 3), ('a', 'b', 'c'), (3.14, 2.71, 1.41))
# Zipped: ((1, 2, 3), ('a', 'b', 'c'), (3.14, 2.71, 1.41))
print(f"Unzipped: {unzipped}")
## Unzipped: ((1, 'a', 3.14), (2, 'b', 2.71), (3, 'c', 1.41))
# Unzipped: ((1, 'a', 3.14), (2, 'b', 2.71), (3, 'c', 1.41))
```

The `zip_variadic` signature says:

- `args` is a variadic list of tuples, each shaped like `tuple[*T]`.
- The return value is a tuple of rows, where each row is `tuple[*T]` (e.g., one `int` row, one `str` row, one `float`
  row).

### Limitations (2025)

- Can't yet mix type variable and type variable tuple freely in all places
- Still not supported in some older tools or linters

### Related Concepts

| Feature             | Purpose                                  |
|---------------------|------------------------------------------|
| Type variable       | A single generic type                    |
| Parameter spec      | A tuple of parameter types for callables |
| Type variable tuple | A tuple of arbitrary generic types       |

### Example: N-dimensional Tensor Shape

// Introduce Tensors

Suppose you're building a generic `Tensor` type that carries its shape as part of its type.
For example, `Tensor[float, 3, 3]` for a 3×3 matrix, or `Tensor[float, 2, 2, 2]` for a 3D cube.
With type variable tuple, we can capture the variable number of dimension sizes.

```python
# n_dimensional_tensor.py
from typing import Literal, TypeAlias


class Tensor[T, *Shape]:
    def __init__(self, data: list, *, shape: tuple[*Shape]):
        self.data = data
        self.shape = shape

    def __repr__(self) -> str:
        return f"Tensor(shape={self.shape})"


Shape3x3: TypeAlias = tuple[Literal[3], Literal[3]]
Shape2x2x2: TypeAlias = tuple[Literal[2], Literal[2], Literal[2]]

t1 = Tensor[float, *Shape3x3](data=[[1.0] * 3] * 3, shape=(3, 3))

t2 = Tensor[int, *Shape2x2x2](
    data=[[[1, 2], [3, 4]], [[5, 6], [7, 8]]],
    shape=(2, 2, 2),
)

print(t1)  # Tensor(shape=(3, 3))
## Tensor(shape=(3, 3))
print(t2)  # Tensor(shape=(2, 2, 2))
## Tensor(shape=(2, 2, 2))
```

- Type checker sees Tensor[float, 3, 3]
- Shape is statically typed as (3, 3)

### An Argument-Preserving Decorator

Here's a decorator that logs a function call without changing its type signature, no matter how many arguments it takes:

```python
# argument_preserving_decorator.py
from typing import Callable


def log_call[**P, R](fn: Callable[P, R]) -> Callable[P, R]:
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        print(f"Calling {fn.__name__} with {args=}, {kwargs=}")
        return fn(*args, **kwargs)

    return wrapper


@log_call
def greet(name: str, age: int) -> str:
    return f"Hi {name}, age {age}"


@log_call
def add(a: int, b: int) -> int:
    return a + b


print(greet("Alice", 30))
## Calling greet with args=('Alice', 30), kwargs={}
## Hi Alice, age 30
print(add(2, 3))
## Calling add with args=(2, 3), kwargs={}
## 5
```

- Type checker knows `greet` returns `str`, and `add` returns `int`
- Arguments are preserved exactly

This isn't strictly a type variable tuple, but it complements it:

- type variable tuple handles variadic type lists
- Parameter specifications handle variadic function arguments

### A Record Type for Heterogeneous Tuples

Let’s say you want a type-safe `Record` that stores a fixed tuple of fields,
where each field can be a different type (like a database row or spreadsheet line):

```python
# heterogeneous_record.py
from dataclasses import dataclass


@dataclass
class Record[*Fields]:
    fields: tuple[*Fields]

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(fields={self.fields})"


print(Record((1, "Alice", 3.14)))
## Record(fields=(1, 'Alice', 3.14))
print(Record((True, None)))
## Record(fields=(True, None))
```

Each `Record` preserves the exact type signature of its fields.

