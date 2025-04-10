# Using Types

Python’s type system allows us to annotate our code with expected types, improving clarity and enabling static type checkers to catch errors early.
This chapter introduces Python’s `typing` module and demonstrates how to apply type annotations to variables, functions, and data structures.
The tone will be a bit more formal and technical, reflecting the increasing sophistication of our journey, but the examples remain clear and approachable.

We assume you are using Python 3.10 or later, which supports the latest type  syntax.
(Where relevant, we will also show older syntax for those on earlier versions.) By the end of this chapter, you will be comfortable adding type annotations to your Python code and understanding their effect on documentation and tooling.

## Built-in Types (`int`, `str`, `float`, `bool`, `None`)

Python supports type annotations for its fundamental built-in types.
By annotating variables with types like `int`, `str`, `float`, `bool`, or `None`, we explicitly communicate what kind of data is expected.
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

In this snippet, each variable’s type is clearly stated.
A reader (or a static type checker) can immediately see that `age` should be an integer, `name` a string, and so on.
These annotations do not change the runtime behavior of the code – Python will not enforce them at runtime – but they serve as important documentation.
They also enable static type checkers and IDEs to detect errors (for instance, if you later try to treat `age` as a string, a type checker would warn you).

Annotating with `None` as a type (as shown for `no_value`) indicates that the variable should hold no value (Python’s `NoneType`).
It’s equivalent to saying the variable’s type is "NoneType".
In summary, using built-in type names in annotations is straightforward and is the foundation for more complex types.

## Variables and Functions

Type annotations can be applied to both variables and function definitions.
In both cases, they clarify what type of data is expected, which helps in reasoning about the code.

### Variables

As shown above, variables can be annotated at the time of assignment.
This is done by writing a colon (`:`) after the variable name, followed by the type, and then the assignment.
For example:

```python
# example_2.py
user_id: int = 123
username: str = "admin"
```

Here, `user_id` is declared to be an integer and initialized to 123, and `username` is a string initialized to `"admin"`.
Even if we don’t immediately assign a value, we can still provide a type hint (for instance, `count: int  # declare that count should be int`).
Annotating variables helps other developers (and tools) understand the intended usage of each variable.

### Functions

Functions benefit greatly from type annotations.
We can annotate each function parameter with its expected type, and we can also annotate the return type of the function after an `->` arrow.
Consider the following function:

```python
# example_3.py
def greet_user(username: str) -> str:
    return f"Welcome, {username}!"
```

In this definition, the parameter `username` is expected to be a string, and the function is expected to return a string (the greeting message).
The annotation `-> str` after the parentheses indicates the return type.
These annotations serve as both documentation and a contract: anyone reading the code can see what type `greet_user` expects and returns, and a static type checker will flag calls like `greet_user(123)` as errors because `123` is not a `str`.

Using annotations for functions makes code self-explanatory.
Imagine a function with multiple parameters or a complex return type – having those types explicitly stated can prevent misuse.
It’s worth noting that if a function does not return anything (or returns `None`), you can annotate its return type as `None` (or omit the return annotation, which implies `None`).
For instance, `def log_message(msg: str) -> None:` would clarify that the function returns nothing useful.
By annotating both variables and functions, we set the stage for safer and more understandable code.

## Optional Types and Default Values

In Python, it’s common for a variable or a function argument to be optional, meaning it can either hold a value of a certain type *or* be `None` to indicate the absence of a value.
To represent this in type hints, Python provides `Optional` in the `typing` module.
An `Optional[T]` is simply a shorthand for "either type `T` or `None`".

For example, consider a function that tries to find a user by ID and returns the user’s name if found, or `None` if not found:

```python
# example_4.py
from typing import Optional

def find_user(user_id: int) -> Optional[str]:
    if user_id == 1:
        return "Alice"
    return None
```

Here, the return type is `Optional[str]`, meaning the function returns either a string (the user’s name) or `None` (if no user was found for that ID).
Inside the function, we see this in action: when `user_id` is 1, we return a string `"Alice"`, otherwise we return `None`.
Without the `Optional` annotation, someone reading just the function signature might assume it always returns a string, which would be misleading.
The type hint makes it clear that `None` is a possible outcome.

Optional types often come into play with default arguments as well.
If a function parameter has a default value of `None`, its type should usually be optional.
Consider a greeting function that can optionally personalize the message:

```python
# example_5.py
from typing import Optional

def greet(name: Optional[str] = None) -> str:
    if name:
        return f"Hello, {name}!"
    return "Hello!"
```

In `greet`, the parameter `name` can be a string or `None` (defaulting to `None` when not provided).
We annotate it as `Optional[str]` to reflect that.
The function returns a string either way – if a name is given, it includes the name in the greeting; if not, it returns a generic greeting.
The use of `Optional[str]` here clearly communicates that you can call `greet()` without an argument (treating `name` as `None`), or call `greet("Bob")` with a string.

Under the hood, `Optional[X]` is just an alias for `Union[X, None]` ([PEP 484 – Type Hints | peps.python.org](https://peps.python.org/pep-0484/#:~:text=As%20a%20shorthand%20for%20%60Union,the%20above%20is%20equivalent%20to)) (a union of the type X with `NoneType`).
We will discuss unions next.
You could write the above annotations as `Union[str, None]` and they would mean the same thing.
`Optional` is simply more convenient and descriptive for this common case.

## Union Types

Sometimes a variable or function parameter can accept several different types instead of just one.
In such cases, we can use a *union type* to indicate that a value may be one of multiple types.
The `typing` module provides `Union` for this purpose.
For example, a function might accept either an integer or a string as input.
Using a union, we can express that as `Union[int, str]`.

### `Union`

Before Python 3.10, the typical way to declare a union of types was to use `typing.Union`.
For instance:

```python
# example_6.py
from typing import Union

def process_value(value: Union[int, str]) -> str:
    return str(value)
```

In this function `process_value`, the parameter `value` can be either an `int` or a `str`.
The function will handle it by converting `value` to a string (using the built-in `str()` constructor) and returning the result.
The annotation `Union[int, str]` makes it clear that both types are acceptable.
If someone accidentally calls `process_value` with, say, a list or a float, a type checker would flag that call as incompatible with the function’s annotation.

Unions can include more than two types as well.
For example, `Union[int, str, float]` would mean a value can be an `int` or a `str` or a `float`.
However, if you find yourself writing a union with `None` (like `Union[X, None]`), remember that you can simplify it using `Optional[X]` as discussed above.

### The `|` Union Operator

Python 3.10 introduced a more concise syntax for union types (PEP 604) ([PEP 604 – Allow writing union types as X | Y | peps.python.org](https://peps.python.org/pep-0604/#:~:text=This%20PEP%20proposes%20overloading%20the,calls)) using the vertical bar `|` operator.
This allows us to write the union in a way that resembles typical logical "OR".
The above example can be rewritten using this new syntax:

```python
# example_7.py
def process_value(value: int | str) -> str:
    return str(value)
```

This definition is equivalent to the previous one using `Union[int, str]`.
The expression `int | str` is interpreted by the Python interpreter (and type checkers) as a union of `int` and `str`.
This syntax is not only shorter, but often clearer to read – it reads almost like an English phrase: "value is an int or str".

You can chain the `|` operator to include multiple types (e.g., `int | str | float`).
And as mentioned, you can use it with `None` as well (e.g., `str | None` is the same as `Optional[str]`).
The `|` operator is a nice improvement for those using Python 3.10 and above, but if you need to support older Python versions, you should stick with `Union`.
Regardless of which syntax you use, the idea is the same: union types allow you to be explicit when a value can have multiple types.

## Defining Type Aliases

As codebases grow, type annotations can become complex.
For example, you might have a dictionary with nested structures or a tuple with many elements.
Writing out these types every time can get unwieldy.
Type aliases are a feature that lets you assign a name to a type (especially a complex one) to make annotations cleaner and more maintainable.

Defining a type alias is as simple as assigning a type to a variable at the top level of your code.
By convention, we often name type aliases with CamelCase to distinguish them from regular variables.
Here’s an example:

```python
# example_8.py
from typing import List

UserIDs = List[int]

def process_users(user_ids: UserIDs) -> None:
    for uid in user_ids:
        print(f"Processing user {uid}")
```

In this snippet, `UserIDs` is a type alias for "list of integers" (`List[int]`).
We then use `UserIDs` in the function annotation to indicate that `process_users` expects a list of ints.
This is functionally identical to writing the annotation as `list[int]` or `List[int]` in the function, but using the alias has advantages:

- It gives a meaningful name to the type, indicating what the list of ints represents (in this case, a collection of user IDs).
- It avoids repeating a complex type annotation in multiple places.
If the definition of `UserIDs` changes (say we decide to use a different type to represent user IDs), we can update the alias in one place.
- It improves readability by abstracting away the details of the type structure.

Type aliases do not create new types at runtime; they are purely for the benefit of the type system and the developer.
Think of them as macros or shortcuts for types.
In our example, `UserIDs` will be treated exactly as `List[int]` by a type checker.
You can create aliases for any type, including unions (for instance, `Number = Union[int, float]`) or more complicated generics.
The key is to use them when they make the code easier to understand.

## Lists, Tuples, Sets, and Dictionaries

Python’s built-in collection types are generic, meaning they can hold items of any type.
With type hints, we can specify what type of items a particular collection is supposed to contain.
This makes our intentions clear (e.g. a list of integers vs. a list of strings) and helps catch errors (accidentally putting the wrong type of item in a collection).

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
The benefit is clear: by reading the annotation, we know exactly what `scores` contains, and we get early warnings if we misuse it.

### Tuples

Tuples are fixed-size sequences, often used for grouping heterogeneous data.
Unlike lists, where all elements are usually of one type, tuples often have a fixed structure (e.g., a pair of a float and a float for coordinates).
We can annotate tuples by listing the types of each position:

```python
# example_10.py
from typing import Tuple

coordinates: Tuple[float, float] = (23.5, 45.8)
```

In this example, `coordinates` is a tuple of two floats.
The annotation `Tuple[float, float]` means: a tuple with exactly two elements, the first a float and the second a float.
If we tried to assign `coordinates = (23.5, "north")`, a static checker would flag it, because the second element isn’t a float as expected.

For tuples of variable length where all elements are the same type, you can use an ellipsis in the annotation (e.g., `Tuple[int, ...]` for "a tuple of ints of any length").
However, in many cases where you have a sequence of varying length, a list might be more appropriate.
Use the tuple annotation when the position and count of elements are fixed and meaningful.

### Sets

A set is an unordered collection of unique elements.
To annotate a set, we specify the type of its elements:

```python
# example_11.py
from typing import Set

unique_ids: Set[str] = {"abc", "xyz", "123"}
```

Here, `unique_ids` is a set of strings.
The annotation `Set[str]` indicates that every element of the set should be a string.
If code later tries to add a non-string to `unique_ids`, a type checker will report an error.
As with lists, specifying the element type of a set makes the intended content clear.
It also helps readers understand what kind of data `unique_ids` holds (e.g., user identifiers, in this case represented as strings).

### Dictionaries

A dictionary is a collection of key-value pairs.
When annotating dictionaries, we need to specify two types: one for keys and one for values:

```python
# example_12.py
from typing import Dict

user_data: Dict[str, int] = {"Alice": 30, "Bob": 25}
```

In `user_data`, the keys are strings and the values are integers, indicated by the annotation `Dict[str, int]`.
This tells us that `user_data` maps names (strings) to ages (ints).
If a function expects a dictionary of user ages, using this type hint ensures that someone doesn’t accidentally pass in, say, a dict mapping names to something else like phone numbers (unless it matches the specified types).

Using these collection type annotations (`List`, `Tuple`, `Set`, `Dict`) greatly enhances code documentation.
They specify not just that a variable is a list or dict, but what’s inside it.
This is crucial for writing correct code, as many bugs come from misunderstanding what type of data is being handled.
Next, we will see that Python has even more convenient ways to write these annotations, especially in newer versions.

## Annotations without Imports

When Python’s types were first introduced (PEP 484 and subsequent enhancements), using generics like lists and dictionaries in annotations required importing their `typing` counterparts (`typing.List`, `typing.Dict`, etc.).
However, starting with Python 3.9, the language allows the use of built-in collection types directly as generic types.
This means you can write `list[int]` instead of importing `List` from `typing`, and similarly for `dict`, `tuple`, and `set`.

This change (specified in PEP 585) ([PEP 585 – Type Hinting Generics In Standard Collections | peps.python.org](https://peps.python.org/pep-0585/#:~:text=contexts,to%20parameterize%20contained%20types)) simplifies type annotations by removing the need for extra imports and making the syntax more natural.
Compare the following with the earlier examples:

```python
# example_13.py
scores: list[int] = [95, 85, 75]
user_data: dict[str, float] = {
    "Alice": 95.5,
    "Bob": 85.3,
}
```

This code is equivalent to previous examples but uses the built-in `list` and `dict` with bracketed type parameters.
`scores` is a list of ints, and `user_data` is a dict with string keys and float values.
No `from typing import List, Dict` is required here.

You can do the same for `tuple` and `set` (e.g., `coordinates: tuple[float, float] = (23.5, 45.8)` or `unique_ids: set[str] = {"a", "b"}`), and it works for other collection types introduced in the standard library as well.
Using the built-in generics often makes code cleaner.
It’s recommended for new code if you are on Python 3.9+.

One thing to note: if you need to support Python versions earlier than 3.9, you should stick to the `typing.List` / `typing.Dict` style, because the bracketed syntax for built-in types won’t be recognized in older versions.
There is also a mechanism called `from __future__ import annotations` that can ease adoption of newer annotation features by treating annotations as strings (to avoid evaluation issues), but that is an advanced detail beyond our current scope.

## Specialized Annotations (`Sequence`, `Mapping`, `Iterable`, `Iterator`)

So far, we’ve annotated variables with concrete types (like "list of int" or "dict of str to int").
Sometimes, however, you may want to hint at a more abstract concept of a type.
For example, suppose you write a function that takes anything you can iterate over (it doesn’t need to specifically be a list or a tuple).
Or a function that can accept any kind of mapping (not just a built-in `dict`, but maybe an `OrderedDict` or a custom mapping type).
For such cases, the `typing` module provides specialized abstract types: `Sequence`, `Mapping`, `Iterable`, `Iterator`, and others.

These abstract annotations allow broader compatibility.
By using them, you indicate the function or variable isn’t tied to one specific implementation, but rather to a category of types that share certain behavior.

### `Sequence`

- Sequence represents any ordered collection that supports element access by index and has a length.
This includes Python’s `list`, `tuple`, `range`, and even `str` (a string can be seen as a sequence of characters).

```python
# example_14.py
from typing import Sequence

def average(numbers: Sequence[float]) -> float:
    return sum(numbers) / len(numbers)
```

In `average`, we accept `numbers` as a `Sequence[float]`.
This means you can pass in a list of floats, a tuple of floats, or any sequence (ordered collection) of floats, and the function will calculate the average.
If we had annotated `numbers` as `List[float]`, the function would technically still work with a tuple or a NumPy array (if it supports `__iter__` and `__len__`), but a type checker would complain if you passed anything that’s not explicitly a `list`.
By using the broader `Sequence` type, we allow any suitable container, which makes the function more flexible while still ensuring the elements are floats.

### `Mapping`

- Mapping represents an object with key-value pairs, like dictionaries.
It is an abstract supertype of `dict` (and other mappings).
A `Mapping[K, V]` has keys of type `K` and values of type `V`.

```python
# example_15.py
from typing import Mapping

def get_user_age(users: Mapping[str, int], username: str) -> int:
    return users.get(username, 0)
```

`get_user_age` takes a `users` argument annotated as `Mapping[str, int]`.
This means any mapping from strings to ints is acceptable.
It could be a normal Python dict, but it could also be something like `collections.UserDict` or any custom object that implements the mapping protocol.
The function body uses `users.get(username, 0)` to retrieve an integer age, defaulting to 0 if the username is not found.
By annotating with `Mapping[str, int]` instead of `Dict[str, int]`, we are not forcing the caller to provide a built-in dict — any mapping will do.
This gives the function flexibility (for example, it could work with an `os.environ` mapping, which behaves like a dict for environment variables, or a database proxy that implements the mapping interface).

### `Iterable` and `Iterator`

- Iterable describes any object that you can loop over (using a `for` loop or other iteration contexts).
This means the object has an `__iter__()` method (or in Python terms, it implements the Iterable protocol).
Examples include lists, sets, tuples, dictionaries (iterating over keys), file objects (iterating over lines), and many more.
- Iterator is a subtype of Iterable that represents the actual iterator object returned by calling `iter()` on an iterable.
An iterator yields items one at a time and produces values until it’s exhausted.
It implements a `__next__()` method that returns the next item or raises `StopIteration` when done.
In practice, *generator functions* (functions using the `yield` keyword) produce iterators.

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

In `print_items`, we specify that `items` can be any iterable of strings.
That means you can pass a list of strings, a set of strings, a tuple of strings, or any object that yields strings when iterated.
The function simply loops and prints each item, not caring about the concrete type of `items`.
If we had restricted `items` to, say, `List[str]`, we wouldn’t be able to pass a set of strings, even though printing each item of a set would work just fine.
Thus, `Iterable[str]` makes the function more general purpose.

The `generate_numbers` function is a simple example of a generator.
It uses `yield` to produce a sequence of integers from 0 up to `n-1`.
The return type is annotated as `Iterator[int]` because calling `generate_numbers(5)` will produce an iterator of integers.
Annotating this helps users of `generate_numbers` know what to expect: they will get an iterator (which they might loop over or convert to a list, etc.) rather than, say, a fully realized list.
Also, it signals that the function uses `yield` internally.
As a side note, if a function is meant to never return normally (for instance, one that enters an infinite loop or always raises an exception), you could use the special return type `NoReturn` from `typing`, but such cases are rare and beyond our current scope.

Specialized annotations like `Sequence`, `Mapping`, `Iterable`, and `Iterator` let you capture the interface or behavior you require, rather than a specific concrete type.
They are especially useful in library or API design, where being too specific with types can needlessly limit the utility of a function or class.
By using these abstract collection types, you make your code flexible while still retaining the benefits of type checking.

## Faster Development, Clearer Results

Type annotations make intentions explicit.
This leads to code that is easier to understand and maintain, and it allows static checkers to assist you by catching type mismatches early in development.
The type system in Python is gradually typed and opt-in – you can use as much or as little as makes sense for your project – but knowing how to use it effectively is a powerful skill for an intermediate Python programmer.
