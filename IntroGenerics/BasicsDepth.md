# Generics

Python's _type hints_ allow us to write **generic** classes and functions with parameterized types.
For example, modern Python (3.9+) lets us use built-in generics like `list[int]` or `dict[str,int]` directly in annotations.
User-defined generics are built with `TypeVar` and `Generic`: you declare a type variable (e.g. `T = TypeVar('T')`), then subclass `Generic[T]` to define a class with that type parameter.
For instance, defining

```python
from typing import TypeVar, Generic

T = TypeVar('T')

class Box(Generic[T]):
    def __init__(self, value: T) -> None:
        self.value = value
    def get(self) -> T:
        return self.value
```

makes `Box` generic in `T`.
The square-bracket syntax `Box[int]()` is allowed because `Box` inherits from `Generic[T]`.
As [PEP 484] explains, "`Generic[T]` as a base class defines that the class takes a type parameter `T`".
This means type checkers will ensure `Box[int]` only holds `int`s; for example, calling `Box[int]("hi")` would be flagged as a type error.

## Holder Classes

A simple motivating example is a _holder_ class that contains a single value.
Without generics, you might write one holder per type, or use a very broad type like `object`.
For instance:

```python
class Automobile:
    pass

# Holder for Automobile only
class Holder1:
    def __init__(self, value: Automobile) -> None:
        self.value = value
    def get(self) -> Automobile:
        return self.value
```

This `Holder1` only holds `Automobile` objects.
Alternatively, a "generic" approach pre-3.5 is to use `object` (or no annotation) so _any_ type can be stored:

```python
class ObjectHolder:
    def __init__(self, value: object) -> None:
        self.value = value
    def get(self) -> object:
        return self.value

h2 = ObjectHolder(Automobile())
x = h2.get()     # Static type: object (needs cast to use as Automobile)
h2.value = "abc" # Allowed at runtime; static type checker permits it as object
```

While this is flexible, it loses type safety: the caller must cast the result of `get()` to the expected type.
In contrast, a generic holder class in Python uses a `TypeVar` so the compiler infers or checks types for you:

```python
from typing import TypeVar, Generic
from dataclasses import dataclass

T = TypeVar('T')

@dataclass
class Holder(Generic[T]):
    value: T

h_int = Holder[int](value=42)      # T = int
x: int = h_int.get()               # No cast needed; get() returns int
# h_int = Holder[int]("string")   # Static type error: expected int, got str
```

Here `Holder[T]` declares `T` as a type parameter, and all annotations using `T` inside the class become that type.
As PEP 484 notes, subclassing `Generic[T]` makes `T` a valid type inside the class.
Thus `Holder[int]` is treated like a box of ints, and the static checker will report a mismatch if we try to store a non-`int` in it.

## Generic Containers (Stack, RandomList)

Generics shine for containers.
For example, a generic stack can be built easily using a list (or other internal container) with a type parameter:

```python
from typing import TypeVar, Generic

T = TypeVar('T')

class Stack(Generic[T]):
    def __init__(self) -> None:
        self._data: list[T] = []
    def push(self, item: T) -> None:
        self._data.append(item)
    def pop(self) -> T:
        return self._data.pop()
    def is_empty(self) -> bool:
        return not self._data

stack = Stack[int]()
stack.push(1)
stack.push(2)
result = stack.pop()   # result is inferred as int

# The static checker would flag this next line as an error:
# stack.push("hello")  # Error: expected int, got str
```

This mirrors typical generic-stack examples.
In fact, the official typing docs give a `Stack[T]` example almost identical to this, noting that `stack = Stack[int]()` behaves like `list[int]`.
They even illustrate that pushing a wrong type is caught by static analysis. (At runtime, Python won't prevent it, but a type checker like mypy or Pyright will warn.)

We could also implement a linked-node stack in Python, similar to the Java example.
For instance:

```python
from typing import Optional
from dataclasses import dataclass

U = TypeVar('U')
@dataclass
class Node(Generic[U]):
    value: U
    next: Optional['Node[U]'] = None

class LinkedStack(Generic[U]):
    def __init__(self) -> None:
        self.top: Optional[Node[U]] = None

    def push(self, item: U) -> None:
        self.top = Node(item, self.top)

    def pop(self) -> U:
        if self.top is None:
            raise IndexError("pop from empty stack")
        value = self.top.value
        self.top = self.top.next
        return value
```

This `LinkedStack[U]` can hold any type `U` in its nodes.
Type annotations (with the help of `Generic[U]`) ensure that `push` and `pop` remain consistent with the chosen type.

Another container example from the Java chapter is the `RandomList<T>` (a list that selects a random element).
In Python, we can do:

```python
import random

S = TypeVar('S')
class RandomList(list[S]):
    def select(self) -> S:
        return random.choice(self)

# Usage:
rs = RandomList[str](["a", "b", "c"])
print(rs.select())  # statically known to be str
```

Here `RandomList` simply subclasses the built-in `list` (which is generic in modern Python) and adds a `select()` method.
Because `RandomList` is parameterized by `S`, a `RandomList[str]` only holds strings, and `select()` is guaranteed (to the type checker) to return a `str`. (At runtime it just picks via `random.choice`.)

## Tuple-Like Classes

Another common pattern is a **tuple class** that holds multiple heterogeneous values.
In Python, we can use a `@dataclass` or a `NamedTuple` to define fixed-field tuples with generics.
For example, a generic 2-tuple:

```python
from typing import NamedTuple, TypeVar, Generic

A = TypeVar('A')
B = TypeVar('B')

class Pair(Generic[A, B], NamedTuple):
    first: A
    second: B

p = Pair[int, str](1, "hello")
print(p.first, p.second)  # 1 hello
```

This creates an immutable tuple-like class `Pair[A,B]`.
The `[A,B]` after `class Pair` declares two type parameters. (This syntax is supported in Python 3.11+ as a "generic NamedTuple," but for compatibility one could also write it with a `TypeVar` and subclassing `Generic[A,B]`.) Alternatively, using `@dataclass`:

```python
from dataclasses import dataclass

@dataclass
class Point(Generic[A, B]):
    x: A
    y: B

pt = Point[int, int](3, 4)
print(pt)  # Point(x=3, y=4)
```

Both approaches allow us to bundle two values of possibly different types (here `A` and `B`) into one object.
The `final`-like immutability in the Java example isn't required here, but with `NamedTuple` the fields are read-only.

One nice feature in modern Python is **pattern matching** (PEP 634) with such classes.
For example:

```python
match p:
    case Pair(first=f, second=s):
        print(f, s)
```

If `p` is a `Pair`, this destructures it into its fields.
Similarly, dataclasses support attribute patterns:

```python
match pt:
    case Point(x=xx, y=yy):
        print(xx, yy)  # prints 3 4
```

Pattern matching works with generic dataclasses and `NamedTuple`s, letting you easily unpack tuple-like objects.

## Generic Functions and Varargs

You can also write **generic functions** with `TypeVar`.
For instance, set operations (union, intersection) generalize over any element type `T`:

```python
from typing import TypeVar, Set

T = TypeVar('T')

def union(a: Set[T], b: Set[T]) -> Set[T]:
    return a.union(b)

def intersection(a: Set[T], b: Set[T]) -> Set[T]:
    return a.intersection(b)

a = {1, 2, 3}
b = {3, 4}
result = union(a, b)          # type: Set[int]
result = intersection(a, b)   # type: Set[int]
```

Here each function is parameterized by `T`, so it works for `Set[int]`, `Set[str]`, etc., while preserving type safety. (Python's built-in set methods `union()` and `intersection()` already do the work, but annotating them with generics ensures correct type hints.) This mirrors the Java `Sets.union<T>(Set<T>,Set<T>)` example ([23_Generics.md](file://file-Qs58AEMVCtFpXpYSkswneT#:~:text=public%20static%20,a%29%3B%20result.retainAll%28b%29%3B%20return%20result)).

For functions, Python's type system can **infer type variables** per call.
For example, in PEP 484 they illustrate:

```python
from typing import TypeVar
U = TypeVar('U')

def identity(x: U) -> U:
    return x

a = identity(42)    # U is inferred as int
b = identity("hi")  # U is inferred as str
```

Each call fixes `U` based on the argument.
As the PEP notes, "`fun_1(1)` ⇒ `T` inferred to be int, and `fun_2('a')` ⇒ `T` inferred to be str."
This is similar to Java's generic methods where type arguments are inferred from parameters.

For variable-argument (varargs) functions, you can use generics too.
For example, a function that makes a list from its arguments:

```python
T = TypeVar('T')

def make_list(*args: T) -> list[T]:
    return list(args)

print(make_list(1))           # [1]        (type List[int])
print(make_list(1, 2, 3))     # [1, 2, 3]  (type List[int])
# print(make_list(1, "a"))    # MyPy would complain: U both int and str
```

Here `make_list(*args: T)` means all arguments must be the same type `T`. (Python's type checker will flag mixing types like `1, "a"` as incompatible for one `TypeVar`.) This parallels the Java `makeList(T... args)` example ([23_Generics.md](file://file-Qs58AEMVCtFpXpYSkswneT#:~:text=%60%60%60java%20%2F%2F%20generics%2FGenericVarargs.java%20import%20java.util.)).

Python 3.11+ even supports _variadic type variables_ (PEP 646) with the `*Ts` syntax to capture heterogeneous `*args`, but that's advanced.
For many cases, a simple `TypeVar` as above suffices.

## Supplier/Generator Classes

In Java, a `Supplier<T>` is an interface with a `get()` method returning `T`.
In Python, we might use a `Callable[[], T]` or simply write a class with a method to produce objects.
For example, the Java "BasicSupplier" that uses reflection (see `BasicSupplier<T>` in the chapter) can be mimicked in Python by passing a type (class) and instantiating it:

```python
from typing import Type, TypeVar

T = TypeVar('T')

class BasicSupplier(Generic[T]):
    def __init__(self, cls: Type[T]) -> None:
        self.cls = cls
    def get(self) -> T:
        return self.cls()   # Assumes T has a no-arg constructor
    @staticmethod
    def create(cls: Type[T]) -> 'BasicSupplier[T]':
        return BasicSupplier(cls)

# Example usage:
supplier = BasicSupplier.create(dict)  # supposes T = dict
empty_dict = supplier.get()           # returns {} as a dict
```

This `BasicSupplier[T]` stores a `type[T]` and its `get()` returns a new instance of `T`.
The static method `create()` is just a convenience, mirroring the Java example.
Because `BasicSupplier` is generic, `BasicSupplier[int]` would type-check to supply ints (if `int()` were sensible).
In practice, Python often prefers plain functions or lambdas for simple suppliers, but this shows the structure of a generic class.

We can also define **iterators or generators** with generics.
For example, a Fibonacci generator class:

```python
from typing import Iterator

class Fibonacci:
    def __init__(self):
        self.a, self.b = 0, 1
    def __iter__(self) -> Iterator[int]:
        return self
    def __next__(self) -> int:
        val = self.a
        self.a, self.b = self.b, self.a + self.b
        return val

fib_iter = Fibonacci()
for _, num in zip(range(5), fib_iter):
    print(num)  # prints 0,1,1,2,3
```

This `Fibonacci` class generates integers.
We could annotate it with `Iterator[int]` to make it generic in its output type. (More idiomatically, one would write a generator function with `yield`, but a class example is closer to the Java `Supplier<Integer>`.)

## Protocols and Structural Typing

Python lets us define _interfaces_ (like Java interfaces) in a _structural_ (duck-typed) way.
A protocol can be generic too.
For example, many built-in protocols are generic: the standard `Iterable[T]` is defined as:

```python
from typing import Protocol, Iterator

class Iterable(Protocol[T]):
    def __iter__(self) -> Iterator[T]: ...
```

(By convention Python's `collections.abc.Iterable` is a protocol with an abstract `__iter__`.
The notes that `Iterable[T]` is a generic `Protocol`.)

We can write our own protocol.
For example, suppose we want any object that has a method `f()` returning `None`:

```python
from typing import Protocol

class HasF(Protocol):
    def f(self) -> None:...

class Example:
    def f(self) -> None:
        print("Called f()")

def apply_f(x: HasF) -> None:
    x.f()

e = Example()
apply_f(e)  # OK: Example has method f(), so it matches Protocol
```

Here `HasF` is a generic protocol (in this case with no type parameters, just behavior).
Any class that has an `f()` method compatible with the signature "implements" `HasF` by structure.
This lets us treat structural interfaces similarly to Java's bounded generics. (Java's `Manipulator2<T extends HasF>` example effectively guarantees `T` has method `f()`.
In Python, we would just require `HasF` or rely on duck typing.)

Protocols can also be generic.
For example, you could define a `Serializer[T]` protocol that requires a `serialize(self, x: T) -> str` method.
Like other generics, `class Serializer(Protocol[T])` would be generic in `T`.
Python's `typing` reference and PEP 544 describe how protocols and generics combine.
The key point is that generic protocols allow us to express: "any type that has these methods (for any concrete type parameter)", and type checkers will enforce method signatures.

## Built-in and Custom Generic Collections

In recent Python versions (3.9+), built-in collection types are themselves generic via `__class_getitem__`.
So you can directly write `list[int]`, `dict[str,int]`, `tuple[float,str,float]`, etc.
Internally, these use special machinery (PEP 560) so that subscription on the class works at runtime.
As PEP 585 explains, this lets us use a unified syntax for generics in annotations.
For instance:

```python
my_list: list[str] = ["a", "b", "c"]   # list of str
my_map: dict[str, int] = {"x": 1}      # dict of str->int
```

A custom generic class (one we wrote ourselves) usually inherits from `Generic` to get this behavior.
But thanks to Python 3.7+ adding `__class_getitem__` to the type system, _all_ classes can be subscripted at runtime.
In other words, `C[int]` works for any class `C`; it produces a `typing.GenericAlias` (or `types.GenericAlias` in 3.9+) so that static tools see the type parameter.
This feature was explicitly added "for better support of generic types."
One benefit is that you don't need a custom metaclass to allow `C[T]`; the special `__class_getitem__` method handles it behind the scenes.

For example, you could write:

```python
class Wrapper:
    def __init__(self, x):
        self.x = x

W = Wrapper[int]   # At runtime, this produces a typing alias (Wrapper[int])
```

This is mostly useful in annotations, since at runtime `W` is not a real class (it's a generic alias).
But it lets type checkers see that `Wrapper[int]` should hold an `int`.

In practice, Python developers often rely on built-in generics (like `list`, `dict`, or `collections.deque`, all of which support parameters) and on simple generic classes via `TypeVar` and `Generic`.

## Summary

Overall, Python's generics (via the `typing` module) allow us to write type-parameterized classes and functions much like Java's generics, but in a way that is optional and mostly enforced by static analysis.
We declare `TypeVar` type variables and use `Generic[T]` (or `Protocol[T]`) to make generic classes.
The syntax `ClassName[TypeArg]` works in annotations (and at runtime thanks to `__class_getitem__`).
Using `@dataclass` or `NamedTuple` with type variables gives us concise tuple-like or container classes.
Type checkers then ensure that, for example, `Stack[int]` only ever contains `int`s, or that a generic function returns the correct type as documented.
This makes our code safer and clearer while preserving Python's flexibility.

**Key points:** Python generics use `TypeVar` and `Generic` ; built-in types (`list`, `dict`, etc.) are generics in type hints ; `typing.Protocol` enables structural (interface-like) typing; type inference in generics works per-call.
These tools let intermediate Python programmers write reusable, type-safe generic code in modern Python.

**Sources:** Python's official typing documentation and PEPs, as well as tutorials and examples from the Python community.

## References
1. [PEP 484](https://peps.python.org/pep-0484/)
2. [PEP 585--Type Hinting Generics In Standard Collections | peps.python.org](https://peps.python.org/pep-0585/)
3. [PEP 484--Type Hints | peps.python.org](https://peps.python.org/pep-0484/)
4. [Python 3.12 Preview: Static Typing Improvements--Real Python](https://realpython.com/python312-typing/)
5. [Generics--typing documentation](https://typing.python.org/en/latest/reference/generics.html)
6. [Named Tuples--typing documentation](https://typing.python.org/en/latest/spec/namedtuples.html)
7. [__INLINE_CODE_99__](https://peps.python.org/pep-0544/)
8. [documentation](https://peps.python.org/pep-0544/)
9. [Protocols--typing documentation](https://typing.python.org/en/latest/spec/protocol.html)
10. [PEP 560--Core support for typing module and generic types | peps.python.org](https://peps.python.org/pep-0560/)
11. [Why are generics in Python implemented using **class_getitem** instead of **getitem** on metaclass - Stack Overflow](https://stackoverflow.com/questions/73464414/why-are-generics-in-python-implemented-using-class-getitem-instead-of-geti)