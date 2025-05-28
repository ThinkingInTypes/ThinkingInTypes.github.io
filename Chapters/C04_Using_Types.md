# Using Types

Type annotations improve clarity and enable static type checkers to catch errors early.
We'll look at Python's `typing` module and apply type annotations to variables, functions, and data structures.

## Built-in Types (`int`, `str`, `float`, `bool`, `None`)

Annotating variables with `int`, `str`, `float`, `bool`, or `None` explicitly communicates the expected type of data.
This makes code more readable and helps tools catch mismatches.
For example:

```python
# example_1.py
age: int = 25
name: str = "Alice"
salary: float = 45000.50
is_active: bool = True
no_value: None = None
```

Each variable's type is clearly stated.
A reader can immediately see that `age` should be an integer, `name` a string, and so on.
Type annotations do not change the runtime behavior of the code--Python will not enforce them at runtime--but they serve as important documentation.
They also enable static type checkers and IDEs to detect errors (for instance, if you later try to treat `age` as a string, a type checker would warn you).

Annotating with `None` as a type (as shown for `no_value`) indicates that the variable should hold no value.
It's equivalent to saying the variable's type is `NoneType`.
Using built-in type names in annotations is straightforward and is the foundation for more complex types.

## Variables and Functions

Type annotations can be applied to both variables and function definitions.
In both cases, they clarify what type of data is expected, which helps in reasoning about the code.

### Variables

To annotate variables at the time of assignment, place a colon after the variable name,
followed by the type, and then the assignment:

```python
# example_2.py
user_id: int = 123
username: str = "admin"
level: float
```

Even if we don't immediately assign a value, as in `level`,
we can still provide a type annotation to indicate the intended usage of that variable.

### Functions

Using annotations for functions makes code self-explanatory.
We annotate each function parameter as well as the return type of the function, after an `->` arrow:

```python
# example_3.py
def greet_user(username: str) -> str:
    return f"Welcome, {username}!"
```

Here the parameter `username` expects a `str`, and `greet_user` returns a string (the greeting message).
The annotation `-> str` after the parentheses indicates the return type.
These annotations serve as both documentation and a contract: anyone reading the code can see what type `greet_user` expects and returns.
A type checker flags calls like `greet_user(123)` as errors because `123` is not a `str`.

Imagine a function with multiple parameters or a complex return type--having those types explicitly stated can prevent misuse.

If a function does not return anything, you can annotate its return type as `None`, or omit the return annotation, which implies `None`.
For instance, `def log_message(msg: str) -> None:` tells you the function is only called to perform _side effects_.

## Optional Types and Default Values

If a variable or a function argument is optional, it can either hold a value of a certain type _or_ be `None` to indicate the absence of a value.
To represent this in type annotations, Python provides `Optional` in the `typing` module.
`Optional[T]` is shorthand for "either type `T` or `None`".

For example, consider a function that tries to find a user by ID and returns the user's name if found, or `None` if not found:

```python
# example_4.py
from typing import Optional


def find_user(user_id: int) -> Optional[str]:
    if user_id == 1:
        return "Alice"
    return None
```

The return type of `Optional[str]` means the function returns either a string (the user's name) or `None` (if no user was found for that ID).
A `user_id` of `1` produces a string `"Alice"`, otherwise it returns `None`.
Without the `Optional`, someone looking at the function signature might assume it always returns a string.
The type annotation makes it clear that `None` is a possible outcome.

`Optional` types are useful with default arguments that can be `None`:

```python
# example_5.py
from typing import Optional


def greet(name: Optional[str] = None) -> str:
    if name:
        return f"Hello, {name}!"
    return "Hello!"
```

The use of `Optional[str]` clearly communicates that you can call `greet()` without an argument (treating `name` as `None`), or call `greet("Bob")` with a string.
The function returns a string either way--if a name is given, it includes the name in the greeting; if not, it returns a generic greeting.

You can also write the above annotation as `Union[str, None]` or `str | None`; `Optional` is preferred because it is more and descriptive.

# TODO: sort out whether to prefer Optional or T | None

## Union Types

A _union type_ indicates that a variable or function parameter can accept several different types instead of just one.
The `typing` module provides `Union` for this purpose, and in more recent versions of Python you can use the `|` operator.

### `Union`

Before Python 3.10, the typical way to declare a union of types was to use `typing.Union`, like this:

```python
# example_6.py
from typing import Union


def process_value(value: Union[int, str]) -> str:
    return str(value)
```

The parameter `value` can be either an `int` or a `str`.
The function converts `value` to a string (using the built-in `str()` constructor).
The annotation `Union[int, str]` makes it clear that both types are acceptable, and the type checker will flag an attempt to use any other type.

Unions can include more than two types.
`Union[int, str, float]` means a value can be an `int` or a `str` or a `float`.
However, if you write union that includes `None` (like `Union[X, None]`), remember that you can simplify it using `Optional[X]`.

### The `|` Union Operator

Python 3.10 introduced a more concise syntax for union types using the `|` operator.
Unions written this way indicate use the idea of the logical "OR" to combine the different types.
This rewritten `process_value` definition is equivalent to the previous one using `Union[int, str]`:

```python
# example_7.py


def process_value(value: int | str) -> str:
    return str(value)
```

This syntax is shorter and often clearer--you can read it as, "value is an `int` or `str`".

You can chain the `|` operator to include multiple types (e.g., `int | str | float`), and you can use it with `None`: `str | None` is the same as `Optional[str]`:

```python
# union_plus_optional.py
from typing import Optional


def f1(value: int | str | None) -> str:
    return str(value)


print(f1(42), f1("forty-two"), f1(None))
## 42 forty-two None


def f2(value: Optional[int | str]) -> str:
    return str(value)


print(f2(42), f2("forty-two"), f2(None))
## 42 forty-two None
```

If you must support older Python versions, use `Union`.

## `List`s, `Tuple`s, `Set`s, and `Dict`s

Python's built-in collection types are generic, meaning they can hold items of any type.
With type annotations, we can specify what type of items a particular collection is supposed to contain.
This makes our intentions clear (e.g., a list of integers vs. a list of strings) and helps catch errors such as accidentally putting the wrong type of item in a collection.

The `typing` module provides specialized generic classes for common collections: `List`, `Tuple`, `Set`, and `Dict` (note: in Python 3.9+, you can use the built-in class names with brackets, which we will discuss in the next section).
We use these to annotate collections with their element types.

### Lists

A list is an ordered collection of items.
When annotating a list, we specify the type of its elements inside square brackets:

```python
# example_9.py
from typing import List

scores: List[int] = [95, 85, 75]
```

Here, `scores` is declared to be a list of integers.
The annotation `List[int]` tells us and the type checker that every element of `scores` should be an `int`.
If somewhere else in the code we mistakenly append a string to `scores`, a type checker would complain.
The benefit is clear: by reading the annotation, we know what `scores` contains, and we get early warnings if we misuse it.

### `Tuple`s

`Tuple`s are fixed-size sequences, often used for grouping heterogeneous data.
Unlike lists, where all elements are usually of one type, `Tuple`s often have a fixed structure (e.g., a pair of a `float` and a `float` for coordinates).
We can annotate `Tuple`s by listing the types of each position:

```python
# example_10.py
from typing import Tuple

coordinates: Tuple[float, float] = (23.5, 45.8)
```

The annotation `Tuple[float, float]` means: a `Tuple` with two elements, the first a `float` and the second a `float`.
If we tried to assign `coordinates = (23.5, "north")`, a static checker would flag it, because the second element isn't a `float` as expected.

For `Tuple`s of variable length where all elements are the same type, you can use an ellipsis in the annotation (e.g., `Tuple[int, ...]` for "a `Tuple` of `int` of any length").
However, in many cases where you have a sequence of varying length, a list might be more appropriate.
Use the `Tuple` annotation when the position and count of elements are fixed and meaningful.

### Sets

To annotate a set, we specify the type of its elements:

```python
# example_11.py
from typing import Set

unique_ids: Set[str] = {"abc", "xyz", "123"}
```

The annotation `Set[str]` indicates that every element of the set should be a string.
If code later tries to add a non-string to `unique_ids`, a type checker will report an error.
As with lists, specifying the element type as `Set` makes the intended content clear.
It also helps readers understand what kind of data `unique_ids` holds (e.g., user identifiers, in this case represented as strings).

### Dictionaries

When annotating dictionaries, we must specify two types: one for keys and one for values:

```python
# example_12.py
from typing import Dict

user_data: Dict[str, int] = {"Alice": 30, "Bob": 25}
```

The annotation tells us that `user_data` maps names (`str`) to ages (`int`).
The type annotation ensures that someone doesn't accidentally pass in, say, a dict mapping names to something else like phone numbers (unless it matches the specified types).

Using these collection type annotations (`List`, `Tuple`, `Set`, `Dict`) greatly enhances code documentation.
They specify not just that a variable is a list or dict, but what's inside it.
This is crucial for writing correct code--many bugs come from misunderstanding data types.
Next, we will see that Python has even more convenient ways to write these annotations, especially in newer versions.

## Annotations without Imports

Starting with Python 3.9, Python allows the direct use of built-in collection type names.
This means you can write `list[int]` instead of importing `List` from `typing`, and similarly for `dict`, `tuple`, and `set`.

This removes the extra imports and makes the syntax more natural:

```python
# example_13.py
scores: list[int] = [95, 85, 75]
user_data: dict[str, float] = {
    "Alice": 95.5,
    "Bob": 85.3,
}
```

You can do the same for `tuple` and `set` (e.g., `coordinates: tuple[float, float] = (23.5, 45.8)` or `unique_ids: set[str] = {"a", "b"}`), and the other standard library collection types.

To support Python versions earlier than 3.9, use `typing.List` / `typing.Dict` style,
because bracketed syntax for built-in types won't be recognized in older versions.
This book will use the built-in names whenever possible

There is also a mechanism called `from __future__ import annotations` that can ease adoption of newer annotation features by treating annotations as strings (to avoid evaluation issues), but that is an advanced detail beyond our current scope.
TODO: Add an example

## Specialized Annotations (`Sequence`, `Mapping`, `Iterable`, `Iterator`)

Sometimes you want a more abstract concept of a type.
For example, suppose you write a function that takes anything you can iterate over, rather than a specific type like `list` or `tuple` or `set`.
Or a function that can accept any kind of mapping; not just a built-in `dict`, but maybe an `OrderedDict` or a custom mapping type.
For such cases, the `typing` module provides specialized abstract types: `Sequence`, `Mapping`, `Iterable`, `Iterator`, and others.

These abstract annotations allow broader compatibility.
They indicate the function or variable isn't tied to one specific implementation, but rather to a category of types that share certain behavior.

### `Sequence`

A `Sequence` represents any ordered collection that supports element access by index and has a length.
This includes Python's `list`, `tuple`, `range`, and even `str` (a string can be seen as a sequence of characters).

```python
# example_14.py
from typing import Sequence


def average(numbers: Sequence[float]) -> float:
    return sum(numbers) / len(numbers)
```

In `average`, we accept `numbers` as a `Sequence[float]`.
This means you can pass in a list of floats, a `tuple` of floats, or any sequence (ordered collection) of `float`s, and the function will calculate the average.
If we annotate `numbers` as `List[float]`, the type checker complains if you pass anything that's not explicitly a `list`.
By using the broader `Sequence` type, we allow any suitable container, which makes the function more flexible while still ensuring the elements are `float`s.

### `Mapping`

A `Mapping` represents an object with key-value pairs, like dictionaries.
It is an abstract supertype of `dict` and other mappings.
A `Mapping[K, V]` has keys of type `K` and values of type `V`.

```python
# example_15.py
from typing import Mapping


def get_user_age(users: Mapping[str, int], username: str) -> int:
    return users.get(username, 0)
```

`get_user_age` takes a `users` argument annotated as `Mapping[str, int]`.
This accepts any mapping from `str` to `int`.
It can be anything from a normal `dict` to something like `collections.UserDict` or any custom object that implements the mapping protocol.
The function body uses `users.get(username, 0)` to retrieve an integer age, defaulting to 0 if the username is not found.
By annotating with `Mapping[str, int]` instead of `Dict[str, int]`, we are not forcing the caller to provide a built-in `dict`--any mapping will do.
This gives the function flexibility; for example, it could work with an `os.environ` mapping, which behaves like a dict for environment variables, or a database proxy that implements the mapping interface.

### `Iterable` and `Iterator`

An `Iterable` describes any object that you can loop over (using a `for` loop or other iteration contexts).
If the object has an `__iter__()` method, it implements the `Iterable` protocol.
Examples include `list`s, `set`s, `tuple`s, `dict`s (iterating over keys), file objects (iterating over lines), and more.

An `Iterator` is a subtype of `Iterable` that represents the `Iterator` object returned by calling `iter()` on an `Iterable`.
It implements a `__next__()` method that returns the next item or raises `StopIteration` when there are no more items.
_Generator functions_ (functions using the `yield` keyword) produce iterators.

```python
# example_16.py
from typing import Iterable, Iterator


def print_items(items: Iterable[str]) -> None:
    for item in items:
        print(item)


def generate_numbers(n: int) -> Iterator[int]:
    for i in range(n):
        yield i
```

`items` can be any iterable of strings.
This means you can pass a `list`, a `set`, a `tuple`, or any object that yields strings when iterated.
`print_items` does not care about the concrete type that holds the `str`s.
Restricting `items` to, say, `list[str]`, means we wouldn't be able to pass a `set` of strings, even though you can print each item of a `set`.
`Iterable[str]` makes the function more general purpose.

`generate_numbers` is an example of a generator.
It uses `yield` to produce a sequence of integers from 0 up to `n-1`.
The return type is annotated as `Iterator[int]` because calling `generate_numbers(5)` will produce an iterator of integers.
Annotating this helps users of `generate_numbers` know what to expect: they will get an iterator (which they might loop over or convert to a list, etc.) rather than, say, a fully realized list.
Also, it signals that the function uses `yield` internally.
As a side note, if a function is meant to never return normally (for instance, one that enters an infinite loop or always raises an exception), you could use the special return type `NoReturn` from `typing`, but such cases are rare and beyond our current scope.

Specialized annotations like `Sequence`, `Mapping`, `Iterable`, and `Iterator` let you capture the interface or behavior you require, rather than a specific concrete type.
They are especially useful in library or API design, where over-specifying types can needlessly limit the utility of a function or class.
By using these abstract collection types, you make your code flexible while still retaining the benefits of type checking.

## T-Strings

https://davepeck.org/2025/04/11/pythons-new-t-strings/

Also custom f string format specifiers

## Faster Development, Clearer Results

Type annotations make intentions explicit.
This produces code that is easier to understand and maintain.
Type checkers catch type mismatches early in development.
The type system in Python is gradually typed and opt-in.
You can use as much or as little as makes sense for your project.
Using types effectively is a powerful skill.
