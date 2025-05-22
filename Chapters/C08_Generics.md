# Generics

Generics in Python produce flexible, reusable code that remains type-safe.
They enable the definition of classes, functions, and types that can operate on a variety of types while preserving type
information.
With generics, you can avoid writing duplicate code for similar operations on different types and catch type errors
early during development.

TODO: Probably divide this into "Generics" here and "Advanced Generics" at the end of the book.

## Defining Custom Generics

Python directly supports *parameterized types*.
This allows you to declare a *type variable*, which is a placeholder for an arbitrary type.

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
from typing_extensions import reveal_type


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
# Zipped: ((1, 2, 3), ('a', 'b', 'c'), (3.14, 2.71, 1.41))
print(f"Unzipped: {unzipped}")
# Unzipped: ((1, 'a', 3.14), (2, 'b', 2.71), (3, 'c', 1.41))
```

The `zip_variadic` signature says:

- `args` is a variadic list of tuples, each shaped like `tuple[*T]`.
- The return value is a tuple of rows, where each row is `tuple[*T]` (e.g., one `int` row, one `str` row, one `float`
  row).

### Limitations (2025)

- Requires Python 3.11+ and a type checker that supports it (PyRight does well, mypy still partial)
- Can't yet mix type variable and type variable tuple freely in all places
- Still not supported in some older tools or linters

### Related Concepts

| Feature             | Purpose                                  |
|---------------------|------------------------------------------|
| Type variable       | A single generic type                    |
| Parameter spec      | A tuple of parameter types for callables |
| Type variable tuple | A tuple of arbitrary generic types       |

### Example: N-dimensional Tensor Shape

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

### Example: Argument-Preserving Decorator

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
## Calling greet with args=('Alice', 30),
## kwargs={}
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

### Example: Record Type for Heterogeneous Tuples

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

## Variance

In the context of generics, *variance* describes how subtyping between complex types relates to subtyping between their
component types.
In Python, all generics are invariant by default, meaning `Container[SubType]` is not a subtype of `Container[BaseType]`
even if `SubType` is a subtype of `BaseType`.
This is a common source of confusion for those coming from languages like Java or C#, but it's an important aspect of
type safety.

Python 3.12 introduced variance inference, so you do not have to specify variance.
This is a great benefit, as people often find variance confusing.

### Invariant

A generic class is invariant by default.
For example, given `Dog` is a subclass of `Animal`, `Box[Dog]` is not considered a subtype of `Box[Animal]`.
This is unsafe because you can then put a `Cat` (another `Animal`) into a `Box[Animal]` which is a `Box[Dog]`
internally.
The type checker forbids treating `Box[Dog]` as a `Box[Animal]`.

### Covariance

Covariance usually makes sense for read-only or producer containers.
For example:

```python
# covariance.py
from animals import Animal, Dog


class ReadOnlyBox[T]:
    def __init__(self, content: T):
        self._content = content

    def get_content(self) -> T:
        return self._content


dog_box: ReadOnlyBox[Dog] = ReadOnlyBox(Dog())
# Covariance in action:
animal_box: ReadOnlyBox[Animal] = dog_box
# pet is an Animal, a Dog:
pet: Animal = animal_box.get_content()
```

Here, `ReadOnlyBox[T]` is covariant with the type parameter `T`.
That signals to the type checker that it is safe to treat `ReadOnlyBox[Dog]` as a `ReadOnlyBox[Animal]`,
because `ReadOnlyBox` only produces `T` (via `get_content`) and never consumes it in a type-specific way.
Covariance is appropriate when the generic class is basically a container of `T` that only returns `T` (and doesn't accept `T`
instances that can violate assumptions).

### Contravariance

Contravariance is suitable for consumer objects that only take in data of type `T` and do not produce it.
For example:

```python
# contravariance.py
from animals import Animal, Dog


class Sink[T]:
    def send(self, value: T) -> None:
        print(f"Processing {value}")


animal_sink: Sink[Animal] = Sink()
# Contravariance in action:
dog_sink: Sink[Dog] = animal_sink  # type: ignore # Pycharm
# dog_sink expects at least Dog, and Animal is broader:
dog_sink.send(Dog())
## Processing Dog(name=None)
```

In this example, `Sink[T]` is contravariant, indicating it only consumes values of type `T` (here, via `send`).
Because a `Sink[Animal]` can accept a `Dog` (since `Dog` is an `Animal`),
it is safe to assign `animal_sink` to a `dog_sink` reference.
In general, contravariance allows broadening the accepted types when substituting; a `Sink[Animal]` can stand in for a
`Sink[Dog]` because anything that expects to only handle `Dog`s can also handle `Animal`s (but not vice versa).

### Using Variance

Function type variables are always invariant.
Most built-in collections in Python are invariant (e.g., `list` is invariant, which is why `list[Dog]` is not assignable
to `list[Animal]`).
Some abstract collection types or protocols are covariant.
For instance, `collections.abc.Sequence` is covariant in its element type,
because sequences are read-only containers as far as the typing system is concerned.

Understanding variance is an advanced topic--many developers use generics effectively without explicitly declaring
covariant/contravariant type variables.
If you design your own generic classes, think about whether they only produce values of type `T` (covariant),
only consume values of type `T` (contravariant), or both (invariant).
Fortunately, since Python 3.12, invariance is inferred.

## Function Currying with Generics

Function currying is the technique of transforming a function that takes multiple arguments into a chain of functions,
each taking a single argument (or fewer arguments).
In Python, we can leverage generics to curry functions while preserving type information.

For example, imagine a function that takes two arguments, and we want to get a new function that has the first argument
fixed (a partial application).
We can write a generic higher-order function to do this:

```python
# curry_two_arg.py
from typing import Callable


def curry_two_arg[X, Y, Z](
        func: Callable[[X, Y], Z],
) -> Callable[[X], Callable[[Y], Z]]:
    def curried(x: X) -> Callable[[Y], Z]:
        def inner(y: Y) -> Z:
            return func(x, y)

        return inner

    return curried


def multiply(a: int, b: float) -> float:
    return a * b


curried_mul = curry_two_arg(multiply)
# get_double is now Callable[[float], float]:
get_double = curried_mul(2)
print(get_double(3.5))
```

Here, `curry_two_arg` is a generic function that works with any two-argument function.
The type variables `X`, `Y`, `Z` ensure that if `func` takes an `X` and a `Y` and returns `Z`,
then `curry_two_arg(func)` returns a function that takes `X` and returns another function which takes `Y` and returns
`Z`.
In the example, `multiply` takes an `int` and a `float` and returns a `float`, so after currying,
`curried_mul` is a function that takes an `int` and returns a function `Callable[[float], float]`.
The types are correctly maintained.

This kind of generic currying function uses higher-order generics (a function that returns another function).
Python's `Callable` type is used to annotate callables.
We can also achieve a similar result using parameter specifications, which allow capturing an arbitrary list of parameters.
However, using explicit type variables for a fixed small number of parameters is straightforward for illustration.

Currying is not common in idiomatic Python but can be useful for creating specialized functions from generic ones.
The benefit of adding generics in currying (as opposed to writing a lambda or using `functools.partial`)
is that the intermediate and final functions retain precise type information.
This helps catch errors if you pass wrong types to the curried functions and provides better auto-completion in editors.

## Recursive Generics

*Recursive generics* refer to types that are defined in terms of themselves.
This is often needed for recursive data structures (like trees or linked lists) or for type definitions that refer to
themselves (like a JSON structure type that can contain nested instances of itself).

### Self-referencing Generic Classes

Consider a simple tree data structure where each node contains a value and a list of children which are themselves
nodes.
We want to parameterize the tree by the type of its values (e.g., `Tree[int]` or `Tree[str]`).
The class needs to refer to itself for the children.
Here's how we can do it:

```python
# self_referencing.py
# For forward-referenced types:
from __future__ import annotations
from dataclasses import dataclass, field


@dataclass
class Tree[T]:
    value: T
    children: list[Tree[T]] = field(default_factory=list)

    def add_child(self, child_value: T) -> Tree[T]:
        child = Tree(child_value)
        self.children.append(child)
        return child


root: Tree[str] = Tree("root")
child_node = root.add_child("child1")
grandchild = child_node.add_child("grandchild1")
```

In `Tree[T]`:

- We use `list[Tree[T]]` to type the `children` as a list of `Tree` nodes with the same value type `T`.
- We needed to use a forward reference for `Tree[T]` inside the class definition.
  In Python 3.11+, the `annotations` feature is on by default, but for earlier versions, we import `annotations` from
  `__future__` to allow the string form of the annotation (`'Tree[T]'`) to be resolved later.
  Alternatively, we could have written `children: list["Tree[T]"] = ...` with quotes around `Tree` as a string literal
  in Python < 3.11 to achieve the same effect.
- The `add_child` method creates a new `Tree[T]` with the given value and appends it to the children.
  It returns the new child node.
  Notice the return type is also `Tree[T]`, not `Tree[Any]` or something unspecified.
  This means if `root` is a `Tree[str]`, `add_child` returns a `Tree[str]` as well.

Such a recursive generic class allows building complex nested structures while keeping type information consistent.
If you try to, say, add a `Tree[int]` as a child of a `Tree[str]`, the type checker will flag an error.
At runtime, this is just a normal class; Python doesn't prevent mixing types in the list, but the static typing helps
you avoid those mistakes in your code.

### F-Bounded Polymorphism (Self types)

TODO: Check that self types are introduced earlier, probably in "Using Types"

Another scenario with recursive generics is when a class needs to use its own type as a type variable.
This is sometimes called *F-bounded polymorphism* or self-referential generics.
A typical example is implementing a fluent interface or a cloning method that returns the same type as the subclass.
Consider a base class that should return an instance of the subclass in a method:

```python
# f_bounded_polymorphism.py
from __future__ import annotations

from dataclasses import dataclass, field
from typing import cast


@dataclass
class Form[T]:
    title: str = ""

    def set_title(self, title: str) -> T:
        self.title = title
        # Returns self as type T for fluent chaining:
        return cast(T, self)


@dataclass
class ContactForm(Form["ContactForm"]):
    fields: list[str] = field(default_factory=list)

    def add_field(self, name: str) -> ContactForm:
        self.fields.append(name)
        return self


form = ContactForm().set_title("Feedback").add_field("email")
```

The generic base class `Form[T]` provides a method that returns `self` as type `T` for type-safe, fluent chaining in subclasses.
`T` is a type variable bounded to `Form` (the base class).
The base class `Form` itself is generic in `T`.
The `set_title` method is annotated to return `T`.

`ContactForm` inherits `Form['ContactForm']`.
By binding `T` to the subclass type, `set_title` will return `ContactForm` when called on a `ContactForm` instance.

The method `add_field` in `ContactForm` returns `ContactForm` explicitly.
Now, the fluent interface works: `ContactForm().set_title(...).add_field(...)` is correctly understood by the type
checker as returning a `ContactForm` with the methods of `ContactForm` available after chaining.

This pattern ensures that each subclass of `Form` will have `set_title` (inherited) returning the subclass type,
not the base type.
It's a bit complex to set up, but it provides more precise typing for chaining methods.
Python 3.11+ provides `typing.Self` (PEP 673) that simplifies this pattern by allowing methods to return `Self` (the type of the actual class).
For example:

```python
# return_self.py
"""
Return `Self` enables type-safe method chaining in subclasses
without the complexity of F-bounded generics.
"""

from dataclasses import dataclass, field
from typing import Self


@dataclass
class Form:
    title: str = ""

    def set_title(self, title: str) -> Self:
        self.title = title
        return self


@dataclass
class ContactForm(Form):
    fields: list[str] = field(default_factory=list)

    def add_field(self, name: str) -> Self:
        self.fields.append(name)
        return self


form = ContactForm().set_title("Feedback").add_field("email")
```

Using `Self` removes the need for the type variable and generic base class.
However, `Self` is limited to describing that a method returns the same type as the class it was called on, whereas the
type variable approach can express more complex relationships.

### Recursive Type Aliases

Sometimes, you might want to define a type alias that refers to itself.
This is common when describing recursive data structures in a type alias form rather than a class.
A classic example is a JSON-like data type, where a JSON value can be a `dict` of string keys to JSON (nested),
or a list of JSON, or a primitive (`str`, `int`, `bool`, etc.).
We can express this as:

```python
# recursive_alias.py
JSON = (
        dict[str, "JSON"]
        | list["JSON"]
        | str
        | int
        | float
        | bool
        | None
)
```

This defines `JSON` as a recursive type alias: it can be a dictionary mapping strings to JSON values, or a list of JSON
values, or a primitive type.
We have to put `'JSON'` in quotes because we are referring to the name `JSON` before it's fully defined
(again, Python 3.11+ with automatic postponed evaluation of annotations handles this without quotes if you use
`from __future__ import annotations` or run in a module where that's the default).

Most type checkers support such recursive type aliases.
In use, if you annotate a variable as `JSON`, the type checker will understand nested structures of dicts and lists
accordingly.
For example:

```python
# recursive_alias_applied.py
from recursive_alias import JSON

config: JSON = {
    "name": "App",
    "features": ["login", "signup"],
    "settings": {"theme": "dark", "volume": 5},
}
```

Overly deep recursion can sometimes confuse type checkers or lead to performance issues in type checking.
Recursive aliases cannot be directly made generic with type variable in the current typing system
(you can wrap recursive structures inside generic classes if needed).

## Structural Subtyping with Protocols

Python's static typing supports two forms of subtype compatibility: *nominal* and *structural*.
Nominal subtyping is the traditional style; an object of class `C` is a subtype of class `B` if `C` subclasses `B`.
Structural subtyping, on the other hand, is about the shape or structure of the type--often called "duck typing"
for types.
If an object has the required methods/attributes, it can be used as that type, regardless of its class in the
inheritance hierarchy.

Python 3.8 introduced *protocols* to facilitate structural typing.
A `Protocol` defines methods and attributes that a type must have, without specifying a particular base class.
Any class that has those members with compatible types is considered a subtype of the protocol, even if it doesn't
explicitly inherit from `Protocol`.
Protocols create interfaces or contracts that can be satisfied by any class, matching Python's dynamic duck typing in a
static type checking context.

### Example: A Drawable Protocol

You define a protocol by subclassing `typing.Protocol` and declaring the methods and properties that must exist.
For example, let's define a protocol for "drawable" objects that must have a `draw()` method:

```python
# drawable.py
from typing import Protocol


class Drawable(Protocol):
    def draw(self) -> None: ...
```

The `...` a.k.a. `pass` means we don't implement behavior in the `Protocol`, we only provide the signature.

Now any object of any class that has a `draw()` method returning `None` is considered a `Drawable` by the type system.
We can write functions that accept a `Drawable`:

```python
# render_drawable.py
from drawable import Drawable


def render(item: Drawable) -> None:
    item.draw()


# Example classes that satisfy the protocol:
class Circle:
    def draw(self) -> None:
        print("Drawing a circle")


class Text:
    def draw(self) -> None:
        print("Rendering text")


circle = Circle()
text = Text()
render(circle)  # OK, Circle has draw()
## Drawing a circle
render(text)  # OK, Text has draw()
## Rendering text
# render(123)   # type checker error: int has no draw()
```

In this snippet, neither `Circle` nor `Text` subclasses `Drawable`,
but they are accepted by the `render` function because they fulfill the structural requirements of the `Drawable`
protocol.
This is static duck typing in action: if it quacks like a duck, treat it as a duck.

**Protocols with Attributes:** Protocols can also specify that an attribute exists (with a certain type).
For example:

```python
# protocols_with_attributes.py
from typing import Protocol


class Named(Protocol):
    name: str


def greet(entity: Named) -> None:
    print(f"Hello, {entity.name}!")
```

Any object with a string attribute `name` qualifies as `Named`.
If you pass an object to `greet` that has a `name` attribute (say an instance of a class that defines `name`), it will
be accepted.

**Generic Protocols:** Protocols can be generic.
For example, the built-in `Iterable[T]` protocol (from `collections.abc` or `typing`) is a generic protocol that
requires an `__iter__` method yielding type `T`.
You can define your own:

```python
# iterable_protocol.py
from typing import Iterator, Protocol


class IterableLike[T](Protocol):
    def __iter__(self) -> Iterator[T]: ...
```

Now `IterableLike[T]` can be used to describe any iterable of `T` without forcing a specific inheritance.
For a function that processes an iterable of `T`, you can annotate a parameter as `IterableLike[T]`.
Any class that has an `__iter__` method returning an iterator of `T` will match.
For example, built-in lists, sets, etc., already implement `__iter__`, so they satisfy `IterableLike`.

### Example: File-like Protocol

Suppose we want a function that can write to any file or file-like object (like an open file handle or an in-memory
buffer), without tying it to a specific class.
We can define a protocol for the methods we need (say, a `write` method) and use it as the parameter type:

```python
# file_protocol.py
from typing import Protocol
from pathlib import Path
from io import StringIO


class Writable(Protocol):
    def write(self, __s: str) -> int: ...


def save_message(out: Writable, message: str) -> None:
    out.write(f"{message}\n")


# With a file:
file_path = Path("message.txt")
with file_path.open("w", encoding="utf-8") as f:
    save_message(f, "Hello, World!")

# With an in-memory buffer:
buffer = StringIO()
save_message(buffer, "Hello, Buffer!")
buffer.seek(0)
print(buffer.read())
## Hello, Buffer!
```

In this example, any object that implements `write(str)` can be passed to `save_message`.
We demonstrated it with a real file (opened via `pathlib.Path`) and a `StringIO` buffer.
Both work because both have a compatible `write` method.
The protocol approach allows `save_message` to work with any current or future file-like object, without needing a
common base class or inheritance.

By default, Protocols are a static concept.
You typically wouldn't use `isinstance(x, Drawable)` or `issubclass(C, Drawable)` with a protocol at runtime, because
`Protocol` classes by themselves don't have special status as base classes.
However, if you need to do runtime checks, the `typing.runtime_checkable` decorator can be applied to a Protocol class,
which then allows using
`isinstance(obj, ProtocolName)` to check if an object conforms (this requires that either the object's class explicitly
inherits the Protocol or that the Protocol is annotated with `runtime_checkable`; a purely structural match at runtime
without explicit registration isn't directly supported).
In general, it's more common to rely on static checking for protocols and use normal duck typing at runtime, "asking
forgiveness rather than permission."

**Use cases:** Protocols are useful when you want to accept "any object that has these methods."
For example:

- A serialization utility that works with any object that has a `to_json()` method can define a protocol for that
  method.
- Defining callback signatures via protocols (PEP 544 allows a special case of protocols with `__call__` to match
  callables).

Protocols bring the flexibility of dynamic typing (duck typing) to the static type world.
They avoid over-constraining function arguments to specific classes when all you care about is the presence of a method
or attribute.

## Generic Type Aliases

Type aliases in Python let you create alternative names for types, which can improve code clarity.
For example, you might write `Coordinate = tuple[float, float]` to give a semantic name to a tuple of two floats.
*Generic type aliases* extend this idea by allowing aliases to be parameterized with type variables.

Creating a generic type alias is straightforward: use a type variable in the definition of the alias.
For instance:

```python
# generic_alias.py

type Pair[T] = tuple[T, T]
type StrDict[T] = dict[str, T]
```

Here, `Pair` and `StrDict` are generic type aliases.
`Pair[int]` is equivalent to `tuple[int, int]`, `Pair[str]` to `tuple[str, str]`, etc.
`StrDict[float]` means `dict[str, float]`.

Using generic aliases is straightforward:

```python
# generic_alias_applied.py
from generic_alias import Pair, StrDict

p: Pair[int] = (10, 20)
q: Pair[str] = ("a", "b")
data: StrDict[int] = {"age": 30, "year": 2025}
```

These annotations make the intent clearer: `p` is a pair of ints, `q` a pair of strs, and `data` is a string-to-int map.
The type checker treats `Pair[int]` as `tuple[int, int]`.
If you do not subscript the alias (e.g., just use `Pair` by itself), the type variables are typically treated as `Any`.
For example:

```python
# generic_alias_tuple.py
from generic_alias import Pair

# type checker treats this as tuple[Any, Any]:
r: Pair = (
    "x",
    5,
)
```

This will not raise an immediate error, because `Pair` unqualified is basically `tuple[Any, Any]`,
but it defeats the purpose of the alias since it's not enforcing that both elements share the same type.
Always supply type parameters for a generic alias to avoid inadvertently falling back to `Any`.

### Alias vs. Direct Use

Type aliases don't create new types at runtime; they are solely for type checking and readability.
In code, `Pair[int]` does not exist as a real class; it's just an alias for `tuple[int, int]`.
If you inspect `Pair[int]` at runtime, you'll get the underlying type.
For example:

```python
# inspect_alias.py
from generic_alias import Pair
from typing import get_origin, get_args

print(get_origin(Pair[int]))
## <class 'tuple'>
print(get_args(Pair[int]))
## (<class 'int'>, <class 'int'>)
```

This shows that `Pair[int]` is recognized by the typing introspection as a tuple with two int arguments.
Type aliases are resolved during type checking and are essentially transparent at runtime.

### Parameterized Aliases in Functions and Classes

You can use generic aliases to simplify annotations inside other generics.
For example:

```python
# vector.py

type Vector[T] = list[tuple[T, T]]


def scale_points(
        points: Vector[int], factor: int
) -> Vector[int]:
    return [(x * factor, y * factor) for (x, y) in points]
```

Here `Vector[int]` is easier to read than `list[tuple[int, int]]`.
The type checker ensures consistency just as if we wrote the full type.

### Declaring Aliases Explicitly

Python 3.10 introduced `TypeAlias` to explicitly declare that an assignment is a type alias (especially when the right-hand side might be ambiguous).
For example:

```python
# typealias_annotation.py
from typing import TypeAlias

Coordinates: TypeAlias = tuple[float, float]
```

However, for simple cases, just using a capitalized variable name for the alias as above is usually clear enough to type
checkers.
(By convention, user-defined type aliases often start with a capital letter.) Python 3.12 is expected to bring a new
syntax for generic aliases using the `type` keyword (PEP 695), but that's beyond the scope of this chapter.

## Guidelines

Generics greatly enhance the expressiveness of Python's type system, but they can also introduce complexity.

### Pitfall: Invariance Confusion

As mentioned earlier, most types are invariant.
A common mistake is expecting container types to be covariantly interchangeable:

```python
# invariance_confusion.py
from animals import Animal, Dog

animals: list[Animal] = [Animal()]
dogs: list[Dog] = [Dog()]
animals = dogs  # type: ignore
```

Here a newcomer might think "a list of Dogs is a list of Animals," but that's not allowed because of invariance.
The pitfall is not realizing that mutation of the list can break type assumptions.
If you find yourself needing to treat a `list[SubType]` as a `list[BaseType]`, reconsider your design or use abstract
interfaces (`Sequence[BaseType]` which is covariant for reading, or `Collection[BaseType]`).
Alternatively, copy the list to a new covariant container if needed for output only.

### Pitfall: Too General (or Overuse of Any)

Using a type variable when your function expects a more specific capability can lead to confusing errors or overly
permissive acceptance.
For example:

```python
# too_general.py


def sort_items[T](items: list[T]) -> list[T]:
    # PyRight issue:
    return sorted(items)  # type: ignore
```

This function will type-check, but it's not truly safe for all `T`--it assumes that the items are comparable (have an ordering defined).
If you call `sort_items` on a list of objects that can't be ordered, you'll get a runtime error.
The type checker wouldn't catch it because `T` was unconstrained (it can be anything).
A better approach is to constrain `T` to types that support ordering:

```python
# bound_type_variable.py
from typing import Protocol, Any


class Comparable(Protocol):
    def __lt__(self, other: Any) -> bool: ...


def sort_items[U: Comparable](items: list[U]) -> list[U]:
    return sorted(items)
```

Now `sort_items` explicitly requires that the item type implements `<` (as per the `Comparable` protocol).

Don't use a totally unconstrained type variable if the function or class really needs the type to have some capability.
Either use a type bound or a protocol to encode that requirement.
Conversely, if you truly intend a function to accept anything (like a generic passthrough that just returns what it was
given), then using `Any` might be appropriate, or a type variable with no constraints if you need to preserve the type
identity.
A function using `Any` will accept and return anything without errors--it turns off type checking for that element.

### Pitfall: Ignoring type variable Scope

Unless the function is truly generic, generics can cause more confusion than clarity.
Remember that a type variable is specific to the generic function or class where it's used.
If you define a type variable at the top of a module and use it in a function signature, that function is generic.
If you intended the function to only work with one specific type, you might accidentally make it generic.

If a type variable appears only once in a function signature, that function is technically generic, but there's no way to
connect the type to anything else
(e.g., a return value or another parameter).
Type checkers will flag this as suspicious:

```python
# accidental_genericity.py
global_var = None


# warning: type variable "T" appears only     │
# once in generic function signature
def set_value[T](x: T) -> None:  # type: ignore
    global global_var
    global_var = x
```

If `global_var` is not also parameterized by `T` somehow, this use of `T` is misleading.
The function `set_value` as written can accept any type, and the type of `global_var` cannot be described properly after
calling it (it can be `int` if called with `int`, `str` if called with `str`, etc.).
This is probably a design mistake.
In such cases, use a normal specific type (or `Any`) if the function isn't meant to be generic.
Use type variable only for functions that really need to be generic.

### Practice: Use Descriptive Type Variable Names for Clarity

While the convention is to use single-letter type variables like `T`, `U`, `V` for simple cases, in more complex generics
consider using more descriptive names.
For example:

```python
# descriptive_type_variables.py


class BiMap[KT, VT]: ...
```

This can make the code more self-documenting, especially if there are multiple type parameters that have roles (key vs.
value, input vs. output, etc.).

### Practice: Leverage Protocols for Flexibility

If you find yourself wanting to accept "any object that has method X," don't force a class hierarchy for typing
purposes.
Use a Protocol.
This decouples your code's type requirements from specific implementations.
It makes your functions more reusable.
The standard library's `typing` module provides many ready-made protocols (like `Iterable`, `Iterator`, `Sequence`,
`Mapping`, etc.) which you should use in type annotations instead of concrete types when possible.
For instance, if a function just needs to read from a container, annotate it as accepting `Iterable[T]` rather than
`list[T]`.
This way, `tuple`s, `set`s, or any `Iterable` will also be accepted.

### Practice: Version Compatibility

The typing ecosystem has evolved quickly.
Be aware of the Python version you are targeting:

- Python 3.7 and earlier: Use `from __future__ import annotations` to avoid forward reference issues.
  The `typing_extensions` module provides `Protocol`, `Literal`, `Final`, etc., which were not yet in `typing`.
  Also, generic built-in types like `list[int]` were not available; you had to use `typing.List[int]`.
- Python 3.8: `typing.Protocol` introduced via PEP 544.
  Also `Literal` and `Final` were added.
- Python 3.9: Built-in generic types like `list[int]`, `dict[str, int]` are supported (PEP 585), so you no longer need
  to import those from `typing`.
  Also, `typing.Annotated` was introduced for adding metadata to types.
- Python 3.10: The `X | Y` union syntax (PEP 604) replaces `typing.Union[X, Y]` for brevity.
  `typing.TypeAlias` was introduced for explicit alias declarations (PEP 613).
- Python 3.11: `typing.Self` was introduced (PEP 673) for easier self-referential return types.
  Also, variance for certain standard collections might be adjusted in the background (for example, `str` and `bytes`
  now share `AnyStr` logic differently, and `typing.AnyStr` is essentially `TypeVar('AnyStr', str, bytes)`).
- Python 3.12+ (future): PEP 695 (Type Parameter Syntax) will allow writing `class MyClass[T]: ...` and
  `def func[X](arg: X) -> X: ...` directly, and the `type` statement for aliases (e.g.,
  `type ListOrSet[T] = list[T] | set[T]`).
  These make generics more concise but require newer Python versions.

## References

1. [Generics--typing documentation](https://typing.python.org/en/latest/reference/generics.html)
2. [Protocols and structural subtyping--typing documentation](https://typing.python.org/en/latest/reference/protocols.html)
3. [Protocols and structural subtyping--typing documentation](https://typing.python.org/en/latest/reference/protocols.html#protocol-types#:~:text=Structural%20subtyping%20is%20based%20on,latter%2C%20and%20with%20compatible%20types)
