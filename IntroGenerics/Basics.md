# Generics

Python generics allow classes and functions to operate on data of various types while preserving type information for static analysis.
In Python, generics are primarily a static typing feature: they enable more precise type hints but do not change runtime behavior.
In other words, generic types are mainly used by type checkers to catch errors early and to document code intent.
For example, a generic list of integers can be denoted as `list[int]`, distinguishing it from `list[str]`.
Such parameterized types--types with type parameters--are called generic types.
Python's built-in collections (like `list`, `dict`, `tuple`, etc.) support this syntax (since PEP 585), and the `typing` module provides tools (`TypeVar`, `Generic`, `Protocol`, etc.) for defining user-defined generics.

This chapter introduces how to write and use generics in Python using both static typing tools and some runtime mechanisms.
We assume familiarity with Python's basic typing module, so we focus on how to declare generic classes and functions, and how to use features like `TypeVar`, `Generic`, and `Protocol` (structural typing) to write reusable, type-safe code.
We also touch on relevant Python 3.x enhancements (e.g.
`__class_getitem__`) that enable generic behavior at runtime.
Throughout, we provide complete code examples of typical use cases: a simple holder class, tuples for multiple-return values, a custom stack, generic generator functions (suppliers), and protocol-based interfaces.
We emphasize idiomatic patterns and best practices, ensuring each concept is explained from first principles and built up gradually.

## Type Variables and Generic Classes

A type variable is a symbol that stands in for an arbitrary type.
In Python's typing system, we create one with `TypeVar`.
For example:

```python
# example_1.py
from typing import TypeVar

T = TypeVar('T')
```

Here `T` can represent any type.
Once defined, `T` can be used in type annotations for functions or classes.
A class parameterized by a type variable becomes a generic class.
This is typically declared by inheriting from `Generic[T]`:

```python
# example_2.py
from typing import Generic

class Box(Generic[T]):
    def __init__(self, content: T) -> None:
        self.content = content
```

The definition above makes `Box` generic: it can hold a value of any type.
When used, a concrete type argument replaces `T`, e.g.
`Box[int]` is a `Box` of integers.
In practice, type checkers use this to ensure type safety:

```python
# example_3.py
b1 = Box(42)         # Inferred as Box[int], content is int
b2 = Box[str]("hi")  # Explicitly Box[str]
b1.content + 5       # OK, content is int
b2.content + 5       # Error: content is str, not compatible with +
```

This resembles how built-in collections are parameterized (e.g.
`list[str]`, `dict[str, int]`).
In fact, user-defined generic classes work much like built-ins.

A more elaborate example is a generic holder or container class.
For instance, a simple `Holder` class can store and retrieve an item of type `T`:

```python
# example_4.py
from typing import Generic, TypeVar

T = TypeVar('T')

class Holder(Generic[T]):
    def __init__(self, value: T) -> None:
        self._value = value

    def get(self) -> T:
        return self._value
```

Because `Holder` is generic, one can create `Holder[int]` or `Holder[str]`.
The type checker will enforce that the `value` and return type of `get()` match the specified type parameter:

```python
# example_5.py
h1: Holder[int] = Holder(10)
x = h1.get()       # x is inferred as int
h1._value = "oops" # Type error: assigning str to Holder[int]
```

A classic use of generics is implementing custom container classes.
For example, a generic stack might look like this:

```python
# example_6.py
from typing import Generic, TypeVar

T = TypeVar('T')

class Stack(Generic[T]):
    def __init__(self) -> None:
        self._items: list[T] = []  # list of items of type T

    def push(self, item: T) -> None:
        self._items.append(item)

    def pop(self) -> T:
        return self._items.pop()

    def empty(self) -> bool:
        return not self._items
```

This `Stack` class uses `T` to type its items and methods.
It can be used for any element type:

```python
# example_7.py
s_int: Stack[int] = Stack()
s_int.push(5)
value = s_int.pop()     # value is an int

s_str = Stack[str]()
s_str.push("hello")
val2 = s_str.pop()      # val2 is a str

# s_int.push("oops") would be a type error, as "oops" is not an int ([Generics--typing  documentation](https://typing.python.org/en/latest/reference/generics.html#:~:text=The%20,int%2C%20str%5D%5D%60%2C%20etc)).
```

Type checkers will flag incorrect type usages.
Internally, all `Stack` instances still use a regular Python list, but annotating `self._items: list[T]` helps static tools know that each element must be a `T`.

By convention, type variables often have short names (`T`, `U`, `V`, etc.), but more descriptive names can be used if needed.
One can also constrain or bound type variables (e.g.
`TypeVar('T', bound=SomeClass)`) to restrict which types are allowed; this is useful when methods rely on certain operations or interfaces.
For an introductory treatment, it suffices to know that `TypeVar('T')` means "some arbitrary type" and `Generic[T]` makes a class generic over that type.

## Generic Functions and Tuples

Generics are not limited to classes: functions can also be generic.
For example, a function that returns its argument can be annotated to be generic in its parameter and return type:

```python
# example_8.py
from typing import TypeVar

T = TypeVar('T')
def identity(x: T) -> T:
    return x
```

Here `identity(5)` is treated as returning an `int`, whereas `identity("hi")` returns a `str`.
Type checkers infer the concrete `T` from usage.
More complex examples include functions that operate on generic containers.
For instance:

```python
# example_9.py
from typing import Sequence, TypeVar

T = TypeVar('T')
def first_element(xs: Sequence[T]) -> T:
    return xs[0]
```

This function takes a sequence of `T` and returns an element of type `T` .
If you pass a `Sequence[int]`, the return type is `int`.
The typing docs give similar examples, e.g.
`def first[T](l: Sequence[T]) -> T` .

Another common pattern is swapping or returning multiple values of possibly different types.
In Python, functions can return tuples of values.
The `tuple` type is special-cased: it can be parameterized with a type for each position.
For example:

```python
# example_10.py
from typing import Tuple, TypeVar

T = TypeVar('T')
U = TypeVar('U')

def swap(a: T, b: U) -> Tuple[U, T]:
    return b, a

x: int = 1
y: str = "hi"
result = swap(x, y)      # result has static type Tuple[str, int]
```

Here `swap` is generic over two type variables `T` and `U`, and it returns a `tuple` whose first element is of type `U` and second is type `T`.
The typing system allows a tuple to have multiple type parameters to reflect differing types per position.
In practice, this means code like `a, b = swap(a, b)` will type-check only if `a` and `b` have the appropriate types.

For functions that yield multiple values in a loop, generator annotations can also be generic.
A simple example is a generator that repeats a value of type `T`:

```python
# example_11.py
from typing import Iterator, TypeVar

T = TypeVar('T')
def repeat_value(value: T, n: int) -> Iterator[T]:
    for _ in range(n):
        yield value
```

This generator yields values of whatever type `T` is.
If you call `repeat_value("x", 3)`, the static return type is `Iterator[str]`.
(Under the hood, a generator is an iterator; one could also use `Generator[T, None, None]` annotation if sending values or return statements were needed.) The official typing documentation shows analogous examples for generators, e.g.
`Iterator[int]` or `Generator[int, None, None]` annotations for yield-only generators.

Another related concept is a supplier or callback: a function with no arguments that returns a value of type `T`.
In typing terms this is simply `Callable[[], T]`.
For example:

```python
# example_12.py
from typing import Callable, TypeVar

T = TypeVar('T')
Supplier = Callable[[], T]

def use_supplier(supplier: Supplier[T]) -> T:
    return supplier()

def five() -> int:
    return 5

print(use_supplier(five))  # returns 5, type-checker knows it's int
```

Here `Supplier[T]` is an alias for "callable that returns `T`", and `use_supplier` is generic in `T`.
When passed `five`, the checker infers `T = int`, so `use_supplier` has return type `int`.
This is an idiomatic way to annotate functions that accept generic callbacks or factories.

## Protocols and Structural Typing

Generic typing in Python includes protocols, which describe interfaces (structural types).
A `Protocol` is like a lightweight interface: a class that defines certain methods or attributes, and any type that implements those methods is considered to satisfy the protocol (without explicit inheritance).
Protocols themselves can be generic.
For example, the typing module defines `Iterable[T]` and `Iterator[T]` as generic protocols.
We can write our own:

```python
# example_13.py
from typing import Protocol, TypeVar

T = TypeVar('T')
class SupportsLessThan(Protocol[T]):
    def __lt__(self: T, other: T) -> bool: ...

def minimum(a: T, b: T) -> T:
    return a if a < b else b
```

Here `SupportsLessThan[T]` is a protocol requiring that an object supports the `<` operator with another `T`.
While this example is illustrative, in practice Python already has such protocols (for instance, `SupportsFloat`, `SupportsAbs`, etc., in `typing`).
The `minimum` function above is generic in `T` and requires that `T` is comparable with itself.
A type checker will allow `minimum(5, 3)` but flag `minimum(5, "hi")` as an error, since `int` and `str` do not inter-compare correctly.

Protocols with generics become especially useful for describing functions that work on abstract collections.
For example:

```python
# example_14.py
from typing import Protocol, TypeVar

T = TypeVar('T')
class Container(Protocol[T]):
    def __contains__(self, item: T) -> bool: ...
```

Now any class that implements `__contains__` can be used with a `Container[T]` annotation.
You might write `def contains_item(c: Container[int], item: int) -> bool` and a list of ints or a custom container would both be accepted by a type checker.

Protocols support structural subtyping: a class doesn't need to inherit from the protocol to satisfy it.
This makes protocols a powerful complement to generics: they define interfaces for types rather than tying to concrete classes.
In generic code, use protocols to specify required capabilities (methods), and use `Generic[T]` on classes or functions when you want to preserve and propagate an arbitrary type parameter.

## Runtime Generics and `__class_getitem__`

Type hints are usually for static analysis, and by default are erased at runtime (e.g.
`list[int]` yields a special object at runtime, but instances of `list` just behave as normal lists).
However, Python does support some runtime generic behavior.
Since Python 3.7 (PEP 560) and more fully in 3.9 (PEP 585), classes can implement a special method `__class_getitem__` to enable the subscription syntax (`Class[...]`).
The built-in collection types (like `list`, `dict`, `tuple`) use this to return a `GenericAlias` object, which carries type information in attributes (accessible via `typing.get_origin` and `typing.get_args` if needed).
For example:

```python
# example_15.py
from typing import get_origin, get_args

alias = list[int]
print(alias)                  # Prints: list[int]
print(get_origin(alias))      # Prints: <class 'list'>
print(get_args(alias))        # Prints: (<class 'int'>,)
```

At runtime, `list[int]` is not a new class; it's a `GenericAlias` that remembers `int` was the parameter.
This machinery is mainly for type checkers (and tools like IDEs) to inspect types; Python itself still just has the usual `list` class at runtime.

One can also define custom behavior by implementing `__class_getitem__`.
This avoids needing complex metaclasses.
For example:

```python
# example_16.py
class MyGeneric:
    def __init__(self, value):
        self.value = value

    def __class_getitem__(cls, item):
        # For demonstration, return a string indicating parameterization
        return f"{cls.__name__}[{item.__name__}]"

print(MyGeneric[int])  # Prints "MyGeneric[int]"
```

In this toy example, subscribing `MyGeneric[int]` calls `MyGeneric.__class_getitem__(int)`, which returns a formatted string.
In real generic classes (like those in `typing` or built-ins), `__class_getitem__` returns a special object representing a parameterized type.
As one source notes, `__class_getitem__` was introduced so classes could support generics without needing a custom metaclass.

In practice, end users rarely need to implement `__class_getitem__` themselves--generics are usually defined using `Generic[T]` and friends.
But knowing it exists helps understand, for example, why built-ins like `list` and `tuple` support indexing (subscriptions) in type annotations (a feature standardized by PEP 585).

In summary, at runtime generic types do not change class behavior or enforce types; they exist to carry type metadata.
Python's design keeps runtime and static typing largely separate, but features like `__class_getitem__` bridge the gap to make static-like syntax possible.

## Idiomatic Patterns and Best Practices

When using generics in Python:

- Prefer Generic to dynamic checks: Generics help document and verify code without runtime overhead.
Avoid unnecessary type-checking code and rely on annotations.
For example, use `list[T]` or `List[T]` annotations instead of checking types in code.

- Name type variables clearly: Single-letter names (`T`, `U`, `V`) are common, but descriptive names (e.g.
`KT`, `VT` for "key type" and "value type" in a mapping) can clarify meaning.
Some common conventions: `T` for a generic type, `V` for value, `K` for key, `E` for element.

- Use bounds for interfaces: If a type variable must support certain operations, use `bound`.
For example, `S = TypeVar('S', bound=SupportsClose)` to indicate `S` must have a `close()` method.

- Differentiate class and function generics: A method inside a generic class can refer to the class's type variables.
If a function is generic independent of a class, define its own `TypeVar`.
Don't mix a class's `T` with a function's `T` accidentally.

- Mixing generic and concrete bases: When subclassing, you can extend generic base classes.
For example `class MyMap(Mapping[KT, VT])` makes `MyMap` generic.
But if you inherit from a concrete generic container, you cannot add new type parameters.
(The typing docs cover these rules in detail .)

- Built-in generics syntax: Since Python 3.9+, you can write built-in generics directly: use `list[int]`, `dict[str, float]`, etc., in annotations.
(For older versions, import from `typing` like `from typing import List`.) This is now the recommended style as it avoids duplicating typing and runtime classes.

- Prefer structural types (Protocols) for flexible interfaces: If a function only needs certain methods from its input, use a protocol type instead of a concrete class.
E.g., use `Iterable[T]` rather than `list[T]` if any iterable is fine.

- Be aware of type erasure: At runtime, generic type parameters are not enforced.
A `Stack[int]` is the same as `Stack[str]` at runtime.
Therefore, do not rely on type parameters for logic.
They are for tools and readability.
If runtime behavior must vary by type, use other patterns (e.g., factory functions).

- Document assumptions: Even with type hints, document what a generic type means.
For instance, in a generic container class docstring, note that it holds "elements of type T" or similar.

Finally, keep in mind that generics are an advanced feature.
You can write a lot of correct Python without them, but they greatly enhance clarity in larger codebases.
As the official documentation notes, user-defined generics are optional, not mandatory, and many programs work well without declaring custom type variables.
Use generics where they make code more maintainable and safe, especially in libraries or interfaces meant for reuse.

Summary: Python's generics (via `TypeVar`, `Generic`, and related tools) let you write classes and functions that are abstract over types while still providing static type-checking guarantees.
You define type variables and use them in annotations, enable generic subscription (`Class[T]`), and optionally define protocols for interface constraints.
Built-in collection types now support parameterized annotations (`list[int]`, `tuple[str, float]`, etc.), and generator/coroutine types can similarly be parameterized.
The combination of generics and protocols enables expressive, type-safe code without sacrificing Python's dynamism.

## References
1. [Generics--typing documentation](https://typing.python.org/en/latest/reference/generics.html)
2. [typing--Support for type hints--Python 3.13.3 documentation](https://docs.python.org/3/library/typing.html)
3. [Why are generics in Python implemented using **class_getitem** instead of **getitem** on metaclass - Stack Overflow](https://stackoverflow.com/questions/73464414/why-are-generics-in-python-implemented-using-class-getitem-instead-of-geti)
