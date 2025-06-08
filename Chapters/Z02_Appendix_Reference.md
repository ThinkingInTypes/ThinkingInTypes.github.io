# Appendix: Reference

Type annotations (or "type hints") declare the expected data types of variables, function parameters, and return values.
Python remains _dynamically typed_ at runtime--these annotations are not enforced by the interpreter and are mainly for static analysis and documentation.
Type checkers and IDEs use the annotations to catch errors or suggest code completions.
Python's core team has no plan to make type annotations mandatory; they are optional aids to improve code quality.

## Introduction via PEPs

Function annotation syntax was first introduced by PEP 3107 (Python 3.0) with no fixed semantics.
PEP 484 (Python 3.5) later defined a standard for using these annotations as _type hints_, establishing a formal type annotation system.
The `typing` module provides a standardized vocabulary of types.
This enables _gradual typing_--code can be partially or fully annotated, and type checkers will treat unannotated parts as dynamically typed (effectively type `Any`).

## Basic Annotation Syntax and Usage

### Function Annotations (Parameters and Return)

You can annotate function parameters and return types using the syntax introduced in PEP 484:

```python
# example_1.py
def greet(name: str, excited: bool = False) -> str:
    return f"Hello, {'!' if excited else ''}{name}"
```

`name: str` and `excited: bool = False` annotate the parameter types, and `-> str` annotates the return type.
An unannotated parameter defaults to type `Any` in static analysis.
If a function does not return a value (or returns `None`), it's good practice to annotate the return type as `None` (e.g.
`-> None`), especially for `__init__` methods.

### Variable Annotations

Python 3.6 (PEP 526) introduced syntax for annotating variables and class attributes with types.
For example: `age: int = 21` or `pi: float` (with or without initialization).
These annotations can appear at the class or module level as well as inside functions.
When annotating class variables (as opposed to instance variables), use `typing.ClassVar`.
For instance:

```python
# example_2.py
from typing import ClassVar


class Starship:
    stats: ClassVar[dict[str, int]] = {}  # class variable
    damage: int = 10  # instance variable
```

Here `stats` is marked as a class-level attribute, whereas `damage` is an instance attribute.
ClassVar helps type checkers distinguish the two.
(At runtime, annotations are stored in the `__annotations__` attribute of the function or class, but they don't affect execution.)

### Type Comments (Legacy)

In older code or for compatibility, type annotations can be given in comments (e.g.
`# type: int`) as described in PEP 484.
This was mainly used for Python 2 or situations where inline annotation syntax was not available.
Modern Python prefers explicit annotation syntax, but you might encounter type comments or stub files in some codebases.

## Core Built-in Types and Collections in Annotations

### Built-in Types

For types like `int`, `str`, `bool`, etc., you can use the type name directly as an annotation.
For example, `x: int = 5` or `user: str`.
The same goes for classes and custom types--you annotate with the class itself (e.g.
`file: io.TextIOBase`).

### Generic Collections (PEP 585)

Modern Python allows using built-in container types directly as generics.
For example, use `list[int]` instead of `typing.List[int]`, `dict[str, float]` instead of `typing.Dict[str, float]`, and so on.
PEP 585 (Python 3.9) enabled this, so the `typing` module's capitalized aliases (List, Dict, etc.)
are no longer necessary in new code.
These generics specify element types:
e.g.
`list[int]` means "list of ints."
(Note:
these annotations are for the benefit of type checkers; at runtime `list[int]` is mainly recognized by the interpreter for typing purposes but still behaves like a normal list).
Tuples can also be annotated, e.g.
`tuple[int, str]` for a fixed-length 2-tuple, or `tuple[int,...]` for a variable-length tuple of ints.

### Union Types and Optional (PEP 604)

A _union_ type means a value could be one of several types.
You can write a union as `typing.Union[X, Y]` or, more readably in Python 3.10+, using the `|` operator:
`X | Y`.
For example, `def parse(data: str | bytes) -> None:` indicates `data` can be either a string or bytes.
If one of the types is `None`, you can use shorthand:
`Optional[T]` is equivalent to `T | None`.
For example, `Optional[int]` (or `int | None`) means the value can be an `int` or `None`.

The `Optional` annotation refers to "may be `None`"; it does not mean an argument is optional in the sense of having a default.
An argument with a default value isn't automatically `Optional` unless you explicitly want to allow `None` as a value.

### The `Any` Type

`typing.Any` is a special type that essentially disables type checking for that variable.
A value of type `Any` is allowed to be passed or assigned to any type, and vice versa.
Every type is compatible with `Any`, and `Any` is compatible with every type.
You might use `Any` when you genuinely cannot predict the type (e.g., a function that can return any type depending on usage).
However, overusing `Any` undermines the benefits of static typing, so it's best used sparingly when other typing features can't express the concept.
(If a function can accept literally any object, a practice is to annotate it as `object` rather than `Any` to signal that no specific behavior is assumed.)

### NoReturn / Never

If a function never returns normally (for example, it always raises an exception or calls `sys.exit()`), you can annotate its return type as `NoReturn` (or `Never`, a synonymous alias introduced in Python 3.11).
This signals to type checkers that the function doesn't produce a value at all.
For instance:

```python
# example_3.py
from typing import Never


def fatal_error(msg: str) -> Never:
    raise RuntimeError(msg)
```

Here, callers can know that `fatal_error()` will not return normally.
`Never`/`NoReturn` is the _bottom type_ in the type system, meaning no value can ever have this type (except in a theoretical sense).
Static analyzers use it to understand control flow (e.g., after a call to a NoReturn function, execution doesn't continue).

## Type Aliases and Custom Types

### Type Aliases

Sometimes you have a complex type and want to give it a short name (alias) for readability.
You can create a type alias by assignment or using the new `type` statement.
For example, `Address = tuple[str, int]` creates an alias `Address` for "tuple of (str, int)".
In Python 3.12+, you can declare aliases more explicitly with the `type` keyword (PEP 695):

```python
# example_4.py
type Point = tuple[float, float]
```

This creates a type alias `Point` that static checkers will treat as `tuple[float, float]`.
Type aliases can also be generic, e.g.
`type Response[T] = tuple[T, int]` to parameterize the alias.
In older versions, you might see `TypeAlias` from `typing` used as an annotation to mark an assignment as a type alias, especially when forward references are involved (to indicate to the checker that a string is meant to be a type name).
PEP 695 deprecates the need for `TypeAlias` by introducing the explicit alias syntax.

### NewType--Distinct Types Based on Existing Ones

The `typing.NewType` helper defines a distinct type that is interchangeable with some base type at runtime but treated as a separate type by type checkers:

```python
# example_5.py
from typing import NewType

UserId = NewType("UserId", int)
```

This creates a new type `UserId` that behaves like an `int` at runtime (it's essentially an identity function that returns the int you give it), but static type checkers will consider `UserId` incompatible with plain `int` unless explicitly allowed.
This is useful when you want to prevent mix-ups of semantically different values that share an underlying type (e.g.
`UserId` vs `ProductId` both as ints).
Using `NewType`, you can catch such mix-ups in static analysis.
Calling `UserId(5)` just returns 5 at runtime, so there's no extra performance cost beyond a function call.
In Python 3.10+ `NewType` is implemented as a class for better performance.

## Generics and Type Variables

### Generic Functions and TypeVar

Python supports _parametric polymorphism_ (generics) in functions and classes.
A _type variable_ represents an unknown type that can vary between calls or instances.
Type variables allow generic code to be checked for type consistency--a key feature of static typing.

Before Python 3.12, to write a function that returns the same type as it receives, you had to use `TypeVar`:

```python
# example_6.py
from typing import TypeVar

T = TypeVar("T")


def identity(item: T) -> T:
    return item
```

Here `T` is a type variable that can stand for any type, and the function `identity` is generic--if you pass an `int`, it returns an `int`, if you pass a `str`, it returns a `str`, etc.
As of Python 3.12, you can declare type parameters directly in the function signature (PEP 695):

```python
# example_7.py
def identity[T](item: T) -> T:
    return item
```

This is equivalent to the earlier definition.
Type variables can be given _bounds_ or _constraints_ to restrict what types they can represent.
For instance, `[U: Number]` means `U` can be any subclass of `Number` (upper-bounded) while `[V: (int, str)]` means V can only be `int` or `str` (union constraint).

### Generic Classes

You can parameterize classes with type variables:

```python
# example_8.py


class Box[T]:
    def __init__(self, content: T):
        self.content = content

    def get_content(self) -> T:
        return self.content
```

`Box[T]` is a generic class that can hold a value of type T.
One can create `Box[int]`, `Box[str]`, etc., and the methods will be type-safe.

When subclassing generics or creating more complex hierarchies,
you may encounter type variance, but for most user-defined generics,
the default invariance (type must match exactly) is fine.

### `typing.Type` for Class Objects

When you want to indicate that a function parameter or return is not an instance of a class but rather a class itself, use `Type[T]` (or `type[T]` in Python 3.9+) where T is a class.
For example, `def factory(cls: type[T]) -> T:` indicates that `factory` expects a class (subclass) of T and will return an instance of that class.
If you want to accept specific subclasses, you can use a union; for example, `user_class: type[BasicUser]` means a class object inheriting from `BasicUser`.
In documentation, you may see `Type[Base]` to mean "any subclass of Base."
This is helpful for functions that work with class constructors or class methods.

## Structural Subtyping with Protocols

Python's static typing supports _structural typing_ via `Protocol` classes.

### Protocols (PEP 544)

A `Protocol` defines a set of methods and properties that a type must have to satisfy the protocol, without requiring inheritance:

```python
# example_9.py
from typing import Protocol


class SupportsClose(Protocol):
    def close(self) -> None: ...
```

Any object with a `.close()` method returning None will be considered a `SupportsClose` for static typing purposes, even if it doesn't inherit from `SupportsClose`.
This is akin to an interface or "duck typing" check.
Protocols enable static type checking of duck-typed code.
If you mark a protocol with `@typing.runtime_checkable`, you can even use `isinstance(obj, ProtocolName)` at runtime; this checks for the presence of required attributes.
Protocols can themselves be generic (e.g., an `Iterable[T]` protocol defines an `__iter__` that yields `T`).
The standard library defines many protocols (e.g.
`typing.Iterable`, `typing.Sized`) that correspond to common Python protocols.
Using Protocols allows one to write functions that accept any object that "has the right methods," enabling flexible, decoupled code with static checks.
PEP 544 formalized this in Python 3.8; it's an extension of abstract base classes (ABCs) toward a more implicit structural approach.

## Callable Types and Function Overloading

Functions are first-class in Python, so you may want to annotate variables or parameters that are themselves functions (callables).

### Callable

The `typing.Callable` type is used to describe the signature of a callable.
For example, `Callable[[int, str], bool]` means "a callable that takes an `int` and a `str` and returns a `bool`."
If you don't want to specify the parameters (so you can accept any callable returning a specific type), use an ellipsis:
`Callable[..., bool]` means any callable returning bool:

```python
# example_10.py
from typing import Callable


def apply_to_ints(
    func: Callable[[int, int], int], a: int, b: int
) -> int:
    return func(a, b)
```

This function takes another function `func` that adds or combines two ints and returns int.
When you pass a lambda or function to `apply_to_ints`, a type checker will ensure it matches the described signature.

### Overloaded Functions (PEP 484)

Sometimes a function can be called with different argument types and behave differently (especially common in library stubs).
The `@typing.overload` decorator declares multiple _overload variants_ for a function:

```python
# overloaded_functions.py
from typing import overload


@overload
def read(data: bytes) -> str: ...


@overload
def read(data: str) -> str: ...


def read(data: str | bytes) -> str:
    # single implementation handling both
    return data.decode() if isinstance(data, bytes) else data
```

Here two overloads declare that `read()` accepts either bytes or str and always returns str.
The implementation (without @overload) handles both.
Type checkers will resolve calls to the appropriate signature.
Overloading is for the benefit of static analysis; at runtime only the final implementation exists.

### Override decorator (PEP 698)

In Python 3.12 the `typing.override` decorator was added to improve correctness in class hierarchies.
You place `@override` on a method to override a method of the same name in the base class.
This doesn't change runtime behavior,
but a type checker will verify that you are overriding a base class method and that your method's signature is compatible with the base class version.
This helps catch errors where you intended to override a method but misspelled its name or got the signature wrong.
Using `@override` can make code maintenance safer in large class hierarchies.

## Parameter Specification Variables for Higher-Order Functions (PEP 612)

PEP 612 introduced _parameter specification variables_ to support typing of _higher-order functions_--functions that accept or return other functions with arbitrary signatures.
A parameter specification variable, typically denoted `**P`, captures a list of parameters (types and kinds) of a `Callable`.
For example, you might write:

```python
# example_12.py
from typing import Callable


def make_logged[**P](
    func: Callable[P, int],
) -> Callable[..., int]:
    def wrapper(
        prefix: str, *args: P.args, **kwargs: P.kwargs
    ) -> int:
        print(f"{prefix} Calling: {func.__name__}")
        result = func(*args, **kwargs)
        print(f"{prefix} Result: {result}")
        return result

    return wrapper


@make_logged
def add(x: int, y: int) -> int:
    return x + y


add("[LOG]", 3, 4)
## [LOG] Calling: add
## [LOG] Result: 7
```

`make_logged` takes a function `func` that returns an `int` and has some parameters `**P`.
It returns a new function that adds a `prefix: str` in front of `func`'s parameters.
We use `Callable[P, int]` to represent the input function's signature and `Callable[..., int]` for the wrapper's signature.
`**P` allows the wrapper to forward the original function's parameters while adding new ones, preserving full type information.
This technique is useful for decorators and wrapper functions that modify call signatures.

## Advanced and New Type Constructs

### Literal Types (PEP 586 and PEP 675)

A `Literal` type indicates that a value is not just of a general type, but a specific constant value (or one of a specific set of constants).
For example, `Literal["GET", "POST"]` can be used to type a variable that should only ever equal `"GET"` or `"POST"`.
This is helpful for functions that behave differently based on constant string or numeric inputs.
In Python 3.8, PEP 586 introduced `typing.Literal`.
E.g.
`def set_mode(mode: Literal["fast", "slow"]) -> None:...` means mode _must_ be one of those two strings.
More recently, PEP 675 (Python 3.11) added `LiteralString`, a special type to mark literal strings for security-sensitive APIs.
`LiteralString` is a subtype of `str` that static analyzers treat as strings that are either literal in the source or derived from other literal strings.
The goal is to prevent untrusted or dynamic strings from flowing into places where they could cause injection attacks (SQL queries, shell commands, etc.):

```python
# example_13.py
from typing import LiteralString


def run_query(query: LiteralString):  # noqua
    ...


run_query("SELECT * FROM users")  # OK, literal
q = "DROP TABLE users"
# type checker error (q is not literal):
run_query(q)  # type: ignore
```

Here, passing a non-literal string to `run_query` would be flagged by a type checker.
Literal types thus allow more precise typing for functions expecting fixed values or literal-derived values.

### Final and Constants (PEP 591)

To indicate that a name should not be reassigned (treated as a constant in type-checking), use the `Final` qualifier.
For example, `MAX_SIZE: Final[int] = 100` tells the type checker that `MAX_SIZE` should never be re-bound to a different value or type.
Attempting to assign to it elsewhere produces a type error.
You can also mark classes as `final` using `@typing.final` decorator, which means the class is not intended to be subclassed.
Similarly, marking a method with `@final` means it should not be overridden in subclasses.
This is purely for type checker and linters; Python won't prevent subclassing or overriding at runtime, but it helps catch design violations in large projects.
Using `Final` is useful for constants or to explicitly close off class hierarchies when appropriate.

### Annotated Types (PEP 593)

`Annotated` was added in Python 3.9 to enrich type annotations with additional metadata that third-party consumers can use.
It supports use-cases like data validation, ORM field specifications, or units attached to values, all while keeping the primary type information.

Its syntax is `Annotated[T, X]` where `T` is a normal type and `X` is metadata (which can be any value, often a class or string).
This metadata can be used by frameworks or tools at runtime or by linters for additional validation.
For instance, one can annotate a type with a range, as in `Annotated[int, Between(0, 100)]` to indicate an `int` that should lie between 0 and 100.
The Python interpreter and core type checkers mostly ignore the second argument of `Annotated` (they treat the variable as just type `T`), but specific libraries can inspect it.

### Type Guards (PEP 647)

// https://typing.python.org/en/latest/guides/modernizing.html#typing-typeguard

A _type guard_ is a special kind of function that informs the type checker of a type refinement.
Introduced in Python 3.10, `typing.TypeGuard` is used as a return annotation on a boolean function to indicate that if the function returns True, its argument is of a certain type:

```python
# example_14.py
from typing import TypeGuard


def is_str_list(
    vals: list[object],
) -> TypeGuard[list[str]]:
    return all(isinstance(x, str) for x in vals)
```

Here, `is_str_list` returns a `bool`, but the `TypeGuard[list[str]]` annotation tells the checker that upon a True result, the input `vals` can be treated as `list[str]` (not just a `list` of object).
This enables writing custom `isinstance`-like helpers that narrow types.
Python's `match` statement and `isinstance` checks also perform narrowing; TypeGuard extends this to user-defined predicates.
This concept helps make code with conditional type logic (like parsing JSON to specific shapes) more type-safe and clear to the type checker.

### `Self` Type (PEP 673)

In class methods that return `self` (or class/instance attributes of the same class type), Python 3.11 introduced `typing.Self` to simplify the annotation.
Using `Self` in a method return type or parameter type means "the same type as the class in which this method is defined":

```python
# example_15.py
from typing import Self


class MyBuilder:
    def set_name(self, name: str) -> Self:
        self.name = name  # type: ignore
        return self
```

The return type `Self` indicates that `set_name` returns the exact same class (`MyBuilder` in this case).
In subclasses, it will correctly infer the subclass type.
Without `Self`, one would have to use a type variable bound to the class, or a string annotation of the class name--both less convenient.
Common use cases for `Self` are fluent interfaces (methods that return `self`), alternative constructors (`classmethod`s that return an instance of `cls`), and methods like `__enter__` in context managers that conventionally return self.
`Self` ensures the return type is automatically updated in subclasses, preventing type checkers from thinking a subclass method returning `self` is returning the base class.

### TypedDicts (PEP 589 and extensions)

A `TypedDict` is a way to describe the expected shape of dictionaries with specific string keys.
`TypedDict` creates a type that expects certain keys with certain value types,
mimicking the behavior of JavaScript objects or dataclasses but for dicts:

```python
# example_16.py
from typing import TypedDict


class Movie(TypedDict):
    title: str
    year: int
```

This defines a type `Movie` that is a dict with keys `"title"` (str) and `"year"` (int).
Any extra keys would be a type checker error, and missing required keys are also an error.
At runtime, a `TypedDict` is just a plain `dict` (there's no special dictionary class), so this is a static construct only.
You can also create TypedDict types using a functional syntax:
`Movie = TypedDict('Movie', {'title': str, 'year': int})`.
By default, all keys are required, but you can make some optional.
Initially, you could specify `total=False` on the `TypedDict` to make all keys optional.
Later, PEP 655 (Python 3.11) introduced `Required` and `NotRequired` markers to allow fine-grained control:
you can mark individual keys as optional in an otherwise total `TypedDict`:

```python
# example_17.py
from typing import TypedDict, Required, NotRequired


class Movie(TypedDict, total=False):
    title: Required[str]  # must have title
    year: NotRequired[int]  # may omit year
```

This says `title` is always required, `year` can be omitted.
When using `total=False`, by default all keys are optional unless marked `Required`.
Conversely, with `total=True` (default), all keys are required unless marked `NotRequired`.
\
Another addition is PEP 705 (Python 3.13) which introduced `typing.ReadOnly` for TypedDict.
This designates certain keys as read-only (cannot be changed once set) for static checking purposes.
Example:
`class Config(TypedDict): host: ReadOnly[str]; port: int`.
Changing `host` after creation would be flagged.
This is helpful to model immutable data within dictionaries.
\
TypedDicts are particularly useful for structures like configuration dicts or JSON data, where you want static validation of keys.
They are also used in **kwargs type annotations:
Python 3.11 allows "spreading" a TypedDict into function arguments with**kwargs (PEP 692).
For instance, `def create_movie(**kwargs: Unpack[Movie]) -> None:` will ensure that the keyword arguments match the Movie TypedDict schema.
Here `typing.Unpack` is used to unpack the TypedDict type.
This feature helps in writing functions that explicitly accept a set of keyword arguments without listing them in the function signature.

### Data Class Transform (PEP 681)

Python's `dataclasses` module and third-party libraries like _Pydantic_ or _attrs_ generate methods (like `__init__`, `__repr__`) automatically based on class attributes.
PEP 681 introduced the `typing.dataclass_transform` decorator (Python 3.11) which library authors can apply to their decorator or metaclass to tell static type checkers that the decorator will produce certain dunder methods or behaviors similar to `dataclasses`.
For example, Pydantic's `BaseModel` or attr's `@define` can use this so that type checkers know that after applying the decorator, the class has an `__init__` with parameters corresponding to the annotated fields.
This is a more advanced feature primarily for library developers to improve user experience of static typing when using those libraries.

## Forward References and Postponed Evaluation

### Forward References

It's common to have types that refer to classes or types not yet defined (e.g., a method in class `A` that returns an instance of class `B` defined later in the file).
To handle this, Python allows using _string literals_ in annotations for forward references.
For example:

```python
# example_18.py
class Node:
    def add_child(self, child: "Node") -> None: ...
```

The quotes allow `Node` to be incompletely defined when the annotation is evaluated.
Quoted annotations defer evaluation of that name.
In Python 3.7+, an alternative to quoting every forward reference is to use `from __future__ import annotations`, which causes all annotations to be stored as strings by default (PEP 563).
This "postponed evaluation" was optional in 3.7--3.9 and was meant to become the default behavior in Python 3.10.
However, that plan was revised:
PEP 563's default activation was put on hold.
The Python steering council decided not to turn on the automatic stringification by default due to various issues it caused for runtime introspection and decided to explore a different approach (PEP 649).

### PEP 649 (Deferred Annotations)

PEP 649, accepted for Python's future (targeted for 3.13+), proposes a new mechanism where annotations are neither evaluated at function definition time nor stored as strings.
Instead, annotations would be stored as code in a special function (`__annotate__`) that computes them on demand.
This aims to solve forward references and performance issues more elegantly:
the evaluation of annotations is deferred until needed, without losing the object references or incurring the issues of stringified annotations.
As of the latest Python (3.12), this is still in progress--by default, Python 3.12 still evaluates annotations normally (unless you use the future import).
When writing modern code, you can rely on `from __future__ import annotations` to handle most forward references conveniently (or just use quotes for specific cases).
Static type checkers themselves resolve forward references even if you leave them as raw names, so this is mostly a runtime concern for introspection via `inspect.get_annotations` or similar.
The takeaway:
forward references are supported via quoting or future imports, and the language is evolving to make annotation evaluation lazy by default in a robust way.

## Tools, Stubs, and Practices

### Type Checkers and IDE Support

To make the most of type annotations, use a static type checker or an IDE with built-in checking (PyCharm, VS Code, etc.).
These tools will read your annotations and warn you of type mismatches, missing return statements for functions declared to return non-`None`, improper overrides, etc.
The type system is standardized enough that most checkers agree on core behavior.
You can customize their strictness (for example, disallowing implicit `Any` types).
Run these checkers as part of your development or CI process to catch bugs early.

### Stub Files (PEP 484 & PEP 561)

If you are using a library that isn't annotated, or you cannot modify source code to add annotations (e.g., C extension modules or third-party code), you can use _stub files_ (`.pyi` files) to provide type information.
A stub file is a skeletal version of a module with only `pass` statements and type annotations.
PEP 561 describes how libraries can distribute these stubs so that your type checker picks them up.
For instance, popular libraries often ship a `py.typed` marker and include inline types or separate stub packages (e.g.
`types-requests`).
As a user, you typically don't write stub files unless you're providing types for an untyped library or doing something very dynamic.
But it's good to know that the ecosystem supports them, enabling gradual adoption of typing even for older code.

### General Best Practices

- Adopt Gradually: You don't have to annotate everything at once.
  It's common to start by annotating function signatures of key modules or adding stubs for critical libraries.
  Unannotated code defaults to `Any` types, which type checkers will by default let pass (or you can configure them to be strict).
- Be Comprehensive in Signatures: For a function that you're annotating, try to annotate all parameters and the return type.
  Partial annotations can sometimes mislead type inference.
  If a function returns nothing, use `-> None` for clarity.
  If a parameter has a default, remember that doesn't automatically make it Optional unless you intend `None` as a valid value.
- Prefer Specific Types or Protocols: When annotating arguments, use the most general type that works for your function (Liskov substitution principle).
  For example, if your function only needs to read from a collection, annotate it as `Iterable[T]` or `Sequence[T]` instead of `list[T]`, to allow more types (like tuples, sets).
  If a parameter can be any object with a certain method, consider using a Protocol instead of a concrete class.
  Conversely, for return types, it's usually best to be as specific as possible (don't return `Any` if you can return a concrete type).
- Use Modern Syntax: Prefer the new concise annotation syntax that Python now supports.
  This means using built-in collection types (e.g.
  `list[int]` rather than `typing.List[int]`) , using `X | Y` for unions rather than `typing.Union[X, Y]` , and `X | None` instead of `typing.Optional[X]`.
  These make annotations more readable.
  The older syntax is still accepted for compatibility, but the newer syntax is encouraged in current code.
- Limit `Any` and Unsafe Casts: Try to avoid using `Any` unless absolutely necessary.
  If you find yourself needing to bypass the type system (via casts or `# type: ignore` comments), consider if there's a better way--such as using Union types, overloading, or restructuring code.
  If you do use `Any` (for example, when interfacing with dynamically typed libraries), isolate it at the boundary of your code.
- Leverage Type Narrowing: Write code in a type-friendly way.
  Use `isinstance` checks or guard functions (even custom TypeGuard functions) to narrow types, instead of, say, `assert isinstance(x, SomeType)` which some type checkers might not understand.
  Many checkers can infer that after `if isinstance(obj, str):...
else:...`, in the else branch `obj` is not a str.
  This makes your code safer and your type checker happier.
- Keep Types Up to Date: Treat type annotations as part of the code documentation.
  If the code changes, update the annotations to match.
  Inconsistencies between code and annotations can be more confusing than no annotations.
  Running a type checker will catch these mismatches.
- Performance Consideration: Annotations are designed to have minimal runtime overhead.
  They're stored as metadata and can be turned into strings with `from __future__ import annotations`.
  Unless you introspect them at runtime (with `typing.get_type_hints()`), they won't slow down your program.
  That said, using a type checker in development might slightly slow down your build/test cycle, but it's usually worth the trade-off for the bugs it prevents.

Each of these topics is elaborated in the official and Python Enhancement Proposals.
For further reading, the typing section in the Python documentation is an excellent resource.
They provide code examples and deeper explanations for advanced scenarios, helping you stay up to date with the evolving landscape of type annotations in modern Python.

## References

1. [typing--Support for type hints--Python 3.13.2 documentation](https://docs.python.org/3/library/typing.html)
2. [PEP 484--Type Hints | peps.python.org](https://peps.python.org/pep-0484/)
3. [Did You Know Some Types in Python's Typing Module Are Now...](https://medium.com/@onurbaskin/did-you-know-some-types-in-pythons-typing-module-are-now-deprecated-551ab9ac1ba1)
4. [Typing Best Practices--typing documentation](https://typing.python.org/en/latest/reference/best_practices.html)
5. [What's New In Python 3.12--Python 3.13.2 documentation](https://docs.python.org/3/whatsnew/3.12.html)
6. [What's New In Python 3.11--Python 3.13.2 documentation](https://docs.python.org/3/whatsnew/3.11.html)
7. [PEP 649--Deferred Evaluation Of Annotations Using Descriptors | peps.python.org](https://peps.python.org/pep-0649/)
8. [Distributing type information--typing documentation](https://typing.python.org/en/latest/spec/distributing.html)
9. [Python typing documentation](https://docs.python.org/3/library/typing.html)
10. ["Typing Cheat Sheet" for Python](https://mypy.readthedocs.io/en/stable/cheat_sheet_py3.html)
