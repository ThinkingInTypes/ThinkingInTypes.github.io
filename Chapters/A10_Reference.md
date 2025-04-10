# Reference

With links to reference material.
Originally generated with ChatGPT 4o in "Deep Research" mode.

## Fundamentals of Type Annotations in Python

### Purpose and Nature

Type annotations (or “type hints”) declare the expected data types of variables, function parameters, and return values.
Python remains *dynamically typed* at runtime – these hints are **not enforced** by the interpreter and are mainly for static analysis and documentation ([typing — Support for type hints — Python 3.13.2 documentation](https://docs.python.org/3/library/typing.html#:~:text=Note)) ([PEP 484 – Type Hints | peps.python.org](https://peps.python.org/pep-0484/#:~:text=performance%20optimizations%20is%20left%20as,an%20exercise%20for%20the%20reader)).
Tools like type checkers (e.g. mypy, Pyright) and IDEs use the hints to catch errors or suggest code completions ([PEP 484 – Type Hints | peps.python.org](https://peps.python.org/pep-0484/#:~:text=Of%20these%20goals%2C%20static%20analysis,for%20code%20completion%20and%20refactoring)).
Python’s core team has no plan to make type hints mandatory; they are optional aids to improve code quality ([PEP 484 – Type Hints | peps.python.org](https://peps.python.org/pep-0484/#:~:text=performance%20optimizations%20is%20left%20as,an%20exercise%20for%20the%20reader)).

### Introduction via PEPs

Function annotation syntax was first introduced by **PEP 3107** (Python 3.0) with no fixed semantics.
**PEP 484** (Python 3.5) later defined a standard for using these annotations as *type hints*, establishing a formal type hinting system ([PEP 484 – Type Hints | peps.python.org](https://peps.python.org/pep-0484/#:~:text=PEP%203107%20added%20support%20for,use%20case%20in%20said%20PEP)).
The `typing` module was added to provide a standard vocabulary of types.
This enabled *gradual typing* – code can be partially or fully annotated, and type checkers will treat unannotated parts as dynamically typed (effectively type `Any`) ([PEP 484 – Type Hints | peps.python.org](https://peps.python.org/pep-0484/#:~:text=The%20type%20system%20supports%20unions%2C,are%20explained%20in%20PEP%20483)) ([PEP 484 – Type Hints | peps.python.org](https://peps.python.org/pep-0484/#:~:text=Any%20function%20without%20annotations%20should,treated%20as%20having%20no%20annotations)).

## Basic Annotation Syntax and Usage

### Function Annotations (Parameters and Return)

You can annotate function parameters and return types using the syntax introduced in PEP 484. For example:

```python
# example_1.py
def greet(name: str, excited: bool = False) -> str:
    return f"Hello, {'!' if excited else ''}{name}"
```

In this example, `name: str` and `excited: bool = False` annotate the parameter types, and `-> str` annotates the return type ([typing — Support for type hints — Python 3.13.2 documentation](https://docs.python.org/3/library/typing.html#:~:text=def%20surface_area_of_cube%28edge_length%3A%20float%29%20,2)).
An unannotated parameter defaults to type `Any` in static analysis ([PEP 484 – Type Hints | peps.python.org](https://peps.python.org/pep-0484/#:~:text=Any%20function%20without%20annotations%20should,treated%20as%20having%20no%20annotations)).
If a function does not return a value (or returns `None`), it’s good practice to annotate the return type as `None` (e.g. `-> None`), especially for `__init__` methods ([PEP 484 – Type Hints | peps.python.org](https://peps.python.org/pep-0484/#:~:text=cannot%20be%20represented%20using%20the,available%20type%20notation)).

### Variable Annotations

Python 3.6 (PEP 526) introduced syntax for annotating variables and class attributes with types.
For example:
`age: int = 21` or `pi: float` (with or without initialization) ([typing — Support for type hints — Python 3.13.2 documentation](https://docs.python.org/3/library/typing.html#:~:text=ClassVar%20indicates%20that%20a%20given,Usage)).
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

Here `stats` is marked as a class-level attribute, whereas `damage` is an instance attribute ([typing — Support for type hints — Python 3.13.2 documentation](https://docs.python.org/3/library/typing.html#:~:text=ClassVar%20indicates%20that%20a%20given,Usage)).
ClassVar helps type checkers distinguish the two.
(At runtime, annotations are stored in the `__annotations__` attribute of the function or class, but they don’t affect execution ([typing — Support for type hints — Python 3.13.2 documentation](https://docs.python.org/3/library/typing.html#:~:text=Note)).)

### Type Comments (Legacy)

In older code or for compatibility, type hints can be given in comments (e.g. `# type: int`) as described in PEP 484. This was mainly used for Python 2 or situations where inline annotation syntax was not available.
Modern Python prefers explicit annotation syntax, but you might encounter type comments or stub files in some codebases.

## Core Built-in Types and Collections in Annotations

### Built-in Types

For types like `int`, `str`, `bool`, etc., you can use the type name directly as an annotation.
For example, `x: int = 5` or `user: str`.
The same goes for classes and custom types – you annotate with the class itself (e.g. `file: io.TextIOBase`).

### Generic Collections (PEP 585)

Modern Python allows using built-in container types directly as generics.
For example, use `list[int]` instead of `typing.List[int]`, `dict[str, float]` instead of `typing.Dict[str, float]`, and so on ([typing — Support for type hints — Python 3.13.2 documentation](https://docs.python.org/3/library/typing.html#:~:text=x%3A%20list)).
PEP 585 (Python 3.9) enabled this, so the `typing` module’s capitalized aliases (List, Dict, etc.)
are no longer necessary in new code ([Did You Know Some Types in Python's Typing Module Are Now ...](https://medium.com/@onurbaskin/did-you-know-some-types-in-pythons-typing-module-are-now-deprecated-551ab9ac1ba1#:~:text=Did%20You%20Know%20Some%20Types,str%2C%20int%5D%20instead%20of%20typing)).
These generics let you specify element types:
e.g. `list[int]` means “list of ints”.
(Note:
these annotations are for the benefit of type checkers; at runtime `list[int]` is mainly recognized by the interpreter for typing purposes but still behaves like a normal list).
Tuples can also be annotated, e.g. `tuple[int, str]` for a fixed-length 2-tuple, or `tuple[int, ...]` for a variable-length tuple of ints.

### Union Types and Optional (PEP 604)

A *union* type means a value could be one of several types.
You can write a union as `typing.Union[X, Y]` or, more readably in Python 3.10+, using the `|` operator:
`X | Y` ([typing — Support for type hints — Python 3.13.2 documentation](https://docs.python.org/3/library/typing.html#:~:text=Union%20type%3B%20%60Union,means%20either%20X%20or%20Y)) ([typing — Support for type hints — Python 3.13.2 documentation](https://docs.python.org/3/library/typing.html#:~:text=Changed%20in%20version%203,subclasses%20from%20unions%20at%20runtime)).
For example, `def parse(data: str | bytes) -> None:` indicates `data` can be either a string or bytes.
If one of the types is `None`, there’s a shorthand:
`Optional[T]` is equivalent to `T | None` ([typing — Support for type hints — Python 3.13.2 documentation](https://docs.python.org/3/library/typing.html#:~:text=typing)).
For example, `Optional[int]` (or `int | None`) means the value can be an int or None.\*\*Important

“Optional” in type hinting refers to "may be None"; it does *not* mean an argument is optional in the sense of having a default.
An argument with a default value isn’t automatically `Optional` unless you explicitly want to allow `None` as a value ([typing — Support for type hints — Python 3.13.2 documentation](https://docs.python.org/3/library/typing.html#:~:text=%60Optional,X%2C%20None)).

### The `Any` Type

`typing.Any` is a special type that essentially **disables type checking** for that variable.
A value of type `Any` is allowed to be passed or assigned to any type, and vice versa ([typing — Support for type hints — Python 3.13.2 documentation](https://docs.python.org/3/library/typing.html#:~:text=typing)).
Every type is compatible with `Any`, and `Any` is compatible with every type ([typing — Support for type hints — Python 3.13.2 documentation](https://docs.python.org/3/library/typing.html#:~:text=typing)).
You might use `Any` when you genuinely cannot predict the type (e.g. a function that can return any type depending on usage).
However, overusing `Any` undermines the benefits of static typing, so it’s best used sparingly when other typing features can’t express the concept.
(If a function can accept literally *any* object, a best practice is to annotate it as `object` rather than `Any` to signal that no specific behavior is assumed ([Typing Best Practices — typing documentation](https://typing.python.org/en/latest/reference/best_practices.html#:~:text=For%20arguments%2C%20prefer%20protocols%20and,Any)).)

### NoReturn / Never

If a function never returns normally (for example, it always raises an exception or calls `sys.exit()`), you can annotate its return type as `NoReturn` (or `Never`, a synonymous alias introduced in Python 3.11) ([typing — Support for type hints — Python 3.13.2 documentation](https://docs.python.org/3/library/typing.html#:~:text=typing)) ([typing — Support for type hints — Python 3.13.2 documentation](https://docs.python.org/3/library/typing.html#:~:text=never_call_me%28arg%29%20%20,or%20NoReturn)).
This signals to type checkers that the function doesn’t produce a value at all.
For instance:

```python
# example_3.py
from typing import NoReturn


def fatal_error(msg: str) -> NoReturn:
    raise RuntimeError(msg)
```

Here, callers can know that `fatal_error()` will not return normally.
`Never`/`NoReturn` is the *bottom type* in the type system, meaning no value can ever have this type (except in a theoretical sense) ([typing — Support for type hints — Python 3.13.2 documentation](https://docs.python.org/3/library/typing.html#:~:text=typing)).
Static analyzers use it to understand control flow (e.g. after a call to a NoReturn function, execution doesn’t continue).

## Type Aliases and Custom Types

### Type Aliases

Sometimes you have a complex type and want to give it a short name (alias) for readability.
You can create a type alias by assignment or using the new `type` statement.
For example:
`Address = tuple[str, int]` creates an alias `Address` for “tuple of (str, int)”.
In Python 3.12+, you can declare aliases more explicitly with the **`type`** keyword (PEP 695):

```python
# example_4.py
type Point = tuple[float, float]
```

This creates a type alias `Point` that static checkers will treat exactly as `tuple[float, float]` ([What’s New In Python 3.12 — Python 3.13.2 documentation](https://docs.python.org/3/whatsnew/3.12.html#:~:text=In%20addition%2C%20the%20PEP%20introduces,creates%20an%20instance%20of%20TypeAliasType)).
Type aliases can also be generic, e.g. `type Response[T] = tuple[T, int]` to parameterize the alias ([What’s New In Python 3.12 — Python 3.13.2 documentation](https://docs.python.org/3/whatsnew/3.12.html#:~:text=Type%20aliases%20can%20also%20be,generic)).
In older versions, you might see `TypeAlias` from `typing` used as an annotation to mark an assignment as a type alias ([typing — Support for type hints — Python 3.13.2 documentation](https://docs.python.org/3/library/typing.html#:~:text=typing)), especially when forward references are involved (to hint to the checker that a string is meant to be a type name) ([typing — Support for type hints — Python 3.13.2 documentation](https://docs.python.org/3/library/typing.html#:~:text=T%20%3D%20TypeVar%28)).
PEP 695 deprecates the need for `TypeAlias` by introducing the explicit alias syntax.

### NewType – Distinct Types Based on Existing Ones

The `typing.NewType` helper lets you define a *distinct* type that is interchangeable with some base type at runtime but treated as a separate type by type checkers.
For example:

```python
# example_5.py
from typing import NewType

UserId = NewType("UserId", int)
```

This creates a new type `UserId` that behaves like an `int` at runtime (it’s essentially an identity function that returns the int you give it) ([typing — Support for type hints — Python 3.13.2 documentation](https://docs.python.org/3/library/typing.html#:~:text=Helper%20class%20to%20create%20low,distinct%20types)) ([typing — Support for type hints — Python 3.13.2 documentation](https://docs.python.org/3/library/typing.html#:~:text=A%20,returns%20its%20argument%20unchanged)), but static type checkers will consider `UserId` incompatible with plain `int` unless explicitly allowed.
This is useful when you want to prevent mix-ups of semantically different values that share an underlying type (e.g. `UserId` vs `ProductId` both as ints).
Using `NewType`, you can catch such mix-ups in static analysis.
(Under the hood, calling `UserId(5)` just returns 5 at runtime, so there’s no extra performance cost beyond a function call ([typing — Support for type hints — Python 3.13.2 documentation](https://docs.python.org/3/library/typing.html#:~:text=the%20statement%20,of%20a%20regular%20function%20call)) ([typing — Support for type hints — Python 3.13.2 documentation](https://docs.python.org/3/library/typing.html#:~:text=In%20contrast%2C%20,is%20expected.%20This%20is)).
In Python 3.10+ `NewType` is implemented as a class for better performance ([typing — Support for type hints — Python 3.13.2 documentation](https://docs.python.org/3/library/typing.html#:~:text=Changed%20in%20version%203.10%3A%20,over%20a%20regular%20function)).)

## Generics and Type Variables

### Generic Functions and TypeVar

Python supports *parametric polymorphism* (generics) in functions and classes.
A **Type Variable** (created with `typing.TypeVar`) represents an unknown type that can vary between calls or instances.
For example, to write a function that returns the same type as it receives, you can do:

```python
# example_6.py
from typing import TypeVar

T = TypeVar("T")


def identity(item: T) -> T:
    return item
```

Here `T` is a type variable that can stand for any type, and the function `identity` is generic – if you pass an `int`, it returns an `int`, if you pass a `str`, it returns a `str`, etc.
As of Python 3.12, you can declare type parameters directly in the function signature (PEP 695) for brevity:

```python
# example_7.py
def identity[T](item: T) -> T:
    return item
```

which is equivalent to the earlier definition ([What’s New In Python 3.12 — Python 3.13.2 documentation](https://docs.python.org/3/whatsnew/3.12.html#:~:text=PEP%20695%20introduces%20a%20new%2C,classes%20%20and%20%20141)).
Type variables can be given **bounds** or **constraints** to restrict what types they can represent.
For instance, `U = TypeVar('U', bound=Number)` means U can be any subclass of `Number` (upper-bounded) while `V = TypeVar('V', int, str)` means V can only be `int` or `str` (union constraint) ([What’s New In Python 3.12 — Python 3.13.2 documentation](https://docs.python.org/3/whatsnew/3.12.html#:~:text=type%20IntFunc%5B,TypeVar%20with%20constraints)).
You can also mark a TypeVar as covariant or contravariant for class inheritance scenarios (useful when defining generic container classes that subclass built-in collections) ([typing — Support for type hints — Python 3.13.2 documentation](https://docs.python.org/3/library/typing.html#:~:text=match%20at%20L597%20OldT%20%3D,OldS%27%2C%20int%2C%20str)), though this is an advanced topic.
In summary, type variables allow writing generic code that’s checked for type consistency – a key feature of PEP 484’s static typing.

### Generic Classes

You can parameterize classes with types as well.
For example:

```python
# example_8.py
from typing import Generic, TypeVar

T = TypeVar("T")


class Box(Generic[T]):
    def __init__(self, content: T):
        self.content = content

    def get_content(self) -> T:
        return self.content
```

`Box[T]` is a generic class that can hold a value of type T. One can create `Box[int]`, `Box[str]`, etc., and the methods will be type-safe.
In Python 3.12+, class definitions too support the simplified generic syntax:
`class Box[T]: ...` (without needing to inherit `Generic[T]`) ([What’s New In Python 3.12 — Python 3.13.2 documentation](https://docs.python.org/3/whatsnew/3.12.html#:~:text=PEP%20695%20introduces%20a%20new%2C,classes%20%20and%20%20141)).
When subclassing generics or creating more complex hierarchies, you might need to be mindful of type variance, but for most user-defined generics, the default invariance (type must match exactly) is fine.

### `typing.Type` for Class Objects

When you want to hint that a function parameter or return is not an *instance* of a class but rather a *class itself*, use `Type[T]` (or `type[T]` in Python 3.9+) where T is a class.
For example, `def factory(cls: type[T]) -> T:` indicates that `factory` expects a class (subclass) of T and will return an instance of that class.
If you want to accept specific subclasses, you can union them:
e.g., `user_class: type[BasicUser]` means a class object inheriting from `BasicUser` ([typing — Support for type hints — Python 3.13.2 documentation](https://docs.python.org/3/library/typing.html#:~:text=def%20new_non_team_user%28user_class%3A%20type%5BBasicUser%20,)).
In documentation, you may see `Type[Base]` to mean “any subclass of Base”.
This is helpful for functions that need to work with class constructors or class methods.

## Structural Subtyping with Protocols

### Protocols (PEP 544)

Python’s static typing supports *structural typing* via **Protocol** classes.
A `Protocol` defines a set of methods and properties that a type must have to satisfy the protocol, without requiring inheritance.
For example:

```python
# example_9.py
from typing import Protocol


class SupportsClose(Protocol):
    def close(self) -> None: ...
```

Any object with a `.close()` method returning None will be considered a `SupportsClose` for static typing purposes, even if it doesn’t inherit from `SupportsClose`.
This is akin to an interface or “duck typing” check.
Protocols enable static type checking of duck-typed code.
If you mark a protocol with `@typing.runtime_checkable`, you can even use `isinstance(obj, ProtocolName)` at runtime (which will just check for the presence of required attributes) ([typing — Support for type hints — Python 3.13.2 documentation](https://docs.python.org/3/library/typing.html#:~:text=Mark%20a%20protocol%20class%20as,a%20runtime%20protocol)).
Protocols can themselves be generic (e.g., an `Iterable[T]` protocol defines an `__iter__` that yields T) ([typing — Support for type hints — Python 3.13.2 documentation](https://docs.python.org/3/library/typing.html#:~:text=Protocol%20classes%20can%20be%20generic%2C,for%20example)).
The standard library defines many protocols (e.g. `typing.Iterable`, `typing.Sized`) that correspond to common Python protocols.
Using Protocols allows one to write functions that accept any object that “has the right methods,” enabling flexible, decoupled code with static checks ([typing — Support for type hints — Python 3.13.2 documentation](https://docs.python.org/3/library/typing.html#:~:text=Protocol%20classes%20are%20defined%20like,this)).
(PEP 544 formalized this in Python 3.8; it’s an extension of the idea of abstract base classes (ABCs) toward a more implicit structural approach.)

## Callable Types and Function Overloading

### Callable\[\[...], ReturnType]

Functions are first-class in Python, so you may want to annotate variables or parameters that are themselves functions (callables).
The `typing.Callable` type is used to describe the signature of a callable.
For example, `Callable[[int, str], bool]` means “a callable that takes an `int` and a `str` and returns a `bool`.”
If you don’t want to specify the parameters (accept any callable returning a specific type), you can use an ellipsis:
`Callable[..., bool]` means any callable returning bool ([typing — Support for type hints — Python 3.13.2 documentation](https://docs.python.org/3/library/typing.html#:~:text=ParamSpec%2C%20Concatenate%2C%20or%20an%20ellipsis,must%20be%20a%20single%20type)).
An example usage:

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

### Overloaded Functions (PEP 484)

Sometimes a function can be called with different argument types and behave differently (especially common in library stubs).
The `@typing.overload` decorator allows you to declare multiple **overload variants** for a function for static typing purposes.
For example:

```python
# example_11.py
from typing import overload, Union


@overload
def read(data: bytes) -> str: ...


@overload
def read(data: str) -> str: ...


def read(data: Union[str, bytes]) -> str:
    # single implementation handling both
    return (
        data.decode() if isinstance(data, bytes) else data
    )
```

Here two overloads declare that `read()` accepts either bytes or str and always returns str.
The implementation (without @overload) handles both.
Type checkers will resolve calls to the appropriate signature.
Overloading is for the benefit of static analysis; at runtime only the final implementation exists ([PEP 484 – Type Hints | peps.python.org](https://peps.python.org/pep-0484/#:~:text=Of%20these%20goals%2C%20static%20analysis,for%20code%20completion%20and%20refactoring)).

### Override decorator (PEP 698)

In Python 3.12 a new `typing.override` decorator was added to improve correctness in class hierarchies.
You place `@override` on a method that is supposed to override a method in the base class.
This doesn’t change runtime behavior, but a type checker will verify that you actually are overriding a base class method and that your method’s signature is compatible with the base class version ([What’s New In Python 3.12 — Python 3.13.2 documentation](https://docs.python.org/3/whatsnew/3.12.html#:~:text=PEP%20698%3A%20Override%20Decorator%20for,Static%20Typing%C2%B6)).
This helps catch errors where you intended to override a method but misspelled its name or got the signature wrong.
Using `@override` can make code maintenance safer in large class hierarchies.

## Parameter Specifications for Higher-Order Functions (PEP 612)

### ParamSpec and Concatenate

**PEP 612** introduced `ParamSpec` (Parameter Specification Variables) to support typing of *higher-order functions* – functions that accept or return other functions with arbitrary signatures.
A ParamSpec, denoted typically as `P = ParamSpec("P")`, captures a *list of parameters* (types and kinds) of a callable.
For example, you might write:

```python
# example_12.py
from typing import ParamSpec, Callable, Concatenate

P = ParamSpec("P")


def make_logged(
    func: Callable[P, int],
) -> Callable[Concatenate[str, P], int]:
    def wrapper(
        prefix: str, *args: P.args, **kwargs: P.kwargs
    ) -> int:
        print(prefix, "Calling:", func.__name__)
        result = func(*args, **kwargs)
        print(prefix, "Result:", result)
        return result

    return wrapper
```

In this example, `make_logged` takes a function `func` that returns an int and has some parameters P. It returns a new function that **adds a `prefix: str` in front of `func`’s parameters**.
We use `Callable[P, int]` to represent the input function’s signature and `Callable[Concatenate[str, P], int]` for the wrapper’s signature.
`Concatenate[str, P]` means we’re prepending a `str` argument in front of the parameter list P ([typing — Support for type hints — Python 3.13.2 documentation](https://docs.python.org/3/library/typing.html#:~:text=typing)).
ParamSpec allows the wrapper to perfectly forward the original function’s parameters while adding new ones, preserving full type information.
This technique is useful for decorators and wrapper functions that modify call signatures.
Without ParamSpec, one might resort to `Callable[..., int]` which loses specific parameter types.
ParamSpecs enable writing precise types for decorators like `@property`, context managers, function adapters, etc., making the static typing of these patterns much more powerful.

## Advanced and New Type Constructs

### Literal Types (PEP 586 and PEP 675)

A **Literal** type allows you to indicate that a value is not just of a general type, but a specific constant value (or one of a specific set of constants).
For example, `Literal["GET", "POST"]` can be used to type a variable that should only ever equal `"GET"` or `"POST"`.
This is helpful for functions that behave differently based on constant string or numeric inputs.
In Python 3.8, **PEP 586** introduced `typing.Literal`.
E.g. `def set_mode(mode: Literal["fast", "slow"]) -> None: ...` means mode *must* be one of those two strings ([typing — Support for type hints — Python 3.13.2 documentation](https://docs.python.org/3/library/typing.html#:~:text=concat%28,cannot%20mix%20str%20and%20bytes)) ([typing — Support for type hints — Python 3.13.2 documentation](https://docs.python.org/3/library/typing.html#:~:text=def%20greet_proper%28cond%3A%20bool%29%20,greetings)).
More recently, **PEP 675** (Python 3.11) added `LiteralString`, a special type to mark *literal strings* for security-sensitive APIs ([What’s New In Python 3.11 — Python 3.13.2 documentation](https://docs.python.org/3/whatsnew/3.11.html#:~:text=PEP%20675%3A%20Arbitrary%20literal%20string,type%C2%B6)).
`LiteralString` is a subtype of `str` that static analyzers treat as strings that are either literal in the source or derived from other literal strings.
The goal is to prevent untrusted or dynamic strings from flowing into places where they could cause injection attacks (SQL queries, shell commands, etc.)
([What’s New In Python 3.11 — Python 3.13.2 documentation](https://docs.python.org/3/whatsnew/3.11.html#:~:text=The%20new%20LiteralString%20annotation%20may,providing%20protection%20against%20injection%20attacks)) ([What’s New In Python 3.11 — Python 3.13.2 documentation](https://docs.python.org/3/whatsnew/3.11.html#:~:text=%29%20,)).
For example:

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

Here, passing a non-literal string to `run_query` would be flagged by a type checker ([What’s New In Python 3.11 — Python 3.13.2 documentation](https://docs.python.org/3/whatsnew/3.11.html#:~:text=query_string%3A%20LiteralString%2C%20table_name%3A%20LiteralString%2C%20,arbitrary_string)).
Literal types thus allow more precise typing for functions expecting fixed values or literal-derived values.

### Final and Constants (PEP 591)

To indicate that a name should not be reassigned (treated as a constant in type-checking), use the `Final` qualifier.
For example, `MAX_SIZE: Final[int] = 100` tells the type checker that `MAX_SIZE` should never be re-bound to a different value or type ([typing — Support for type hints — Python 3.13.2 documentation](https://docs.python.org/3/library/typing.html#:~:text=Changed%20in%20version%203,in%20Final%20and%20vice%20versa)).
Attempting to assign to it elsewhere would be a static error.
You can also mark classes as `final` using `@typing.final` decorator, which means the class is not intended to be subclassed.
Similarly, marking a method with `@final` means it should not be overridden in subclasses.
This is purely for the type checker/linters; Python won’t prevent subclassing or overriding at runtime, but it helps catch design violations in large projects.
Using Final is useful for constants or to explicitly close off class hierarchies when appropriate.

### Annotated Types (PEP 593)

The `typing.Annotated` type was introduced to enrich type hints with additional metadata.
Its syntax is `Annotated[T, X]` where T is a normal type and X is metadata (which can be any value, often a class or string).
This metadata can be used by frameworks or tools at runtime or by linters for additional validation.
For instance, one could annotate a type with a range:
`Annotated[int, Between(0, 100)]` to indicate an int that should lie between 0 and 100. The Python interpreter and core type checkers mostly ignore the second argument of Annotated (they treat the variable as just type T), but specific libraries can inspect it.
This was added in Python 3.9 to support use-cases like data validation, ORM field specifications, or units attached to values, all while keeping the primary type information.
In short, `Annotated` wraps a base type with extra info that third-party consumers can use ([typing — Support for type hints — Python 3.13.2 documentation](https://docs.python.org/3/library/typing.html#:~:text=While%20type%20hints%20can%20be,of%20more%20advanced%20type%20hints)).

### Type Guards (PEP 647)

A *type guard* is a special kind of function that informs the type checker of a type refinement.
Introduced in Python 3.10, `typing.TypeGuard` is used as a return annotation on a boolean function to indicate that if the function returns True, its argument is of a certain type.
For example:

```python
# example_14.py
from typing import TypeGuard


def is_str_list(
    vals: list[object],
) -> TypeGuard[list[str]]:
    return all(isinstance(x, str) for x in vals)
```

Here, `is_str_list` returns a `bool`, but the `TypeGuard[list[str]]` annotation tells the checker that upon a True result, the input `vals` can be treated as `list[str]` (not just list of object).
This enables writing custom `isinstance`-like helpers that narrow types.
Python’s `match` statement and `isinstance` checks also perform narrowing; TypeGuard extends this to user-defined predicates ([typing — Support for type hints — Python 3.13.2 documentation](https://docs.python.org/3/library/typing.html#:~:text=def%20is_str%28val%3A%20str%20,str)).
This concept helps make code with conditional type logic (like parsing JSON to specific shapes) more type-safe and clear to the type checker.

### `Self` Type (PEP 673)

In class methods that return `self` (or class/instance attributes of the same class type), Python 3.11 introduced `typing.Self` to simplify the annotation ([What’s New In Python 3.11 — Python 3.13.2 documentation](https://docs.python.org/3/whatsnew/3.11.html#:~:text=PEP%20673%3A%20)) ([What’s New In Python 3.11 — Python 3.13.2 documentation](https://docs.python.org/3/whatsnew/3.11.html#:~:text=)).
Using `Self` in a method return type or parameter type means “the same type as the class in which this method is defined.”
For example:

```python
# example_15.py
from typing import Self


class MyBuilder:
    def set_name(self, name: str) -> Self:
        self.name = name  # noqa: Instance attribute
        return self
```

The return type `Self` indicates that `set_name` returns the *exact same class* (`MyBuilder` in this case).
In subclasses, it will correctly infer the subclass type ([typing — Support for type hints — Python 3.13.2 documentation](https://docs.python.org/3/library/typing.html#:~:text=from%20typing%20import%20Self%2C%20reveal_type)) ([typing — Support for type hints — Python 3.13.2 documentation](https://docs.python.org/3/library/typing.html#:~:text=In%20general%2C%20if%20something%20returns,SubclassOfFoo)).
Without `Self`, one would have to use a type variable bound to the class, or a string annotation of the class name – both less convenient.
Common use cases for `Self` are fluent interfaces (where methods return `self`), alternative constructors (often classmethods that return an instance of `cls`), and methods like `__enter__` in context managers that conventionally return self ([typing — Support for type hints — Python 3.13.2 documentation](https://docs.python.org/3/library/typing.html#:~:text=Other%20common%20use%20cases%20include%3A)).
`Self` ensures the return type is automatically updated in subclasses, preventing type checkers from thinking a subclass method returning `self` is returning the base class.

### TypedDicts (PEP 589 and extensions)

A **TypedDict** is a way to describe the expected shape of dictionaries with specific string keys.
Introduced in Python 3.8, TypedDict allows you to create a type that expects certain keys with certain value types, mimicking the behavior of JavaScript objects or dataclasses but for dicts.
For example:

```python
# example_16.py
from typing import TypedDict


class Movie(TypedDict):
    title: str
    year: int
```

This defines a type `Movie` that is a dict with keys `"title"` (str) and `"year"` (int) ([typing — Support for type hints — Python 3.13.2 documentation](https://docs.python.org/3/library/typing.html#:~:text=class%20typing)).
Any extra keys would be a type checker error, and missing required keys are also an error.
At runtime, a `TypedDict` is just a plain `dict` (there’s no special dictionary class) ([typing — Support for type hints — Python 3.13.2 documentation](https://docs.python.org/3/library/typing.html#:~:text=class%20typing)), so this is a static construct only.
You can also create TypedDict types using a functional syntax:
`Movie = TypedDict('Movie', {'title': str, 'year': int})` ([typing — Support for type hints — Python 3.13.2 documentation](https://docs.python.org/3/library/typing.html#:~:text=match%20at%20L2372%20An%20alternative,must%20be%20a%20literal%20dict)).
By default all keys are required, but you can make some optional.
Initially, you could specify `total=False` on the TypedDict to make *all* keys optional.
Later, **PEP 655** (Python 3.11) introduced `Required` and `NotRequired` markers to allow fine-grained control:
you can mark individual keys as optional in an otherwise total TypedDict ([What’s New In Python 3.11 — Python 3.13.2 documentation](https://docs.python.org/3/whatsnew/3.11.html#:~:text=year%3A%20NotRequired)) ([What’s New In Python 3.11 — Python 3.13.2 documentation](https://docs.python.org/3/whatsnew/3.11.html#:~:text=The%20following%20definition%20is%20equivalent%3A)).
For example:

```python
# example_17.py
from typing import TypedDict, Required, NotRequired


class Movie(TypedDict, total=False):
    title: Required[str]  # must have title
    year: NotRequired[int]  # may omit year
```

This says `title` is always required, `year` can be omitted ([What’s New In Python 3.11 — Python 3.13.2 documentation](https://docs.python.org/3/whatsnew/3.11.html#:~:text=year%3A%20NotRequired)).
When using `total=False`, by default all keys are optional unless marked `Required`.
Conversely, with `total=True` (default), all keys are required unless marked `NotRequired` ([typing — Support for type hints — Python 3.13.2 documentation](https://docs.python.org/3/library/typing.html#:~:text=match%20at%20L2396%20class%20Point2D,str)).
\
Another addition is **PEP 705** (Python 3.13) which introduced `typing.ReadOnly` for TypedDict.
This lets you designate certain keys as read-only (cannot be changed once set) for static checking purposes ([typing — Support for type hints — Python 3.13.2 documentation](https://docs.python.org/3/library/typing.html#:~:text=match%20at%20L1284%20A%20special,only)).
Example:
`class Config(TypedDict): host: ReadOnly[str]; port: int`. Changing `host` after creation would be flagged.
This is helpful to model immutable data within dictionaries.
\
TypedDicts are particularly useful for structures like configuration dicts or JSON data, where you want static validation of keys.
They are also used in **kwargs type annotations:
Python 3.11 allows “spreading” a TypedDict into function arguments with**kwargs (PEP 692).
For instance, `def create_movie(**kwargs: Unpack[Movie]) -> None:` will ensure that the keyword arguments match the Movie TypedDict schema ([typing — Support for type hints — Python 3.13.2 documentation](https://docs.python.org/3/library/typing.html#:~:text=match%20at%20L1604%20,in%20a%20function%20signature)) ([typing — Support for type hints — Python 3.13.2 documentation](https://docs.python.org/3/library/typing.html#:~:text=from%20typing%20import%20TypedDict%2C%20Unpack)).
Here `typing.Unpack` is used to unpack the TypedDict type.
This feature helps in writing functions that explicitly accept a set of keyword arguments without enumerating them in the function signature.

### Data Class Transform (PEP 681)

Python’s `dataclasses` module and third-party libraries like **Pydantic** or **attrs** generate methods (like `__init__`, `__repr__`) automatically based on class attributes.
PEP 681 introduced the `typing.dataclass_transform` decorator (Python 3.11) which library authors can apply to their decorator or metaclass to hint to static type checkers that the decorator will produce certain dunder methods or behaviors similar to `dataclasses` ([What’s New In Python 3.11 — Python 3.13.2 documentation](https://docs.python.org/3/whatsnew/3.11.html#:~:text=PEP%20681%3A%20Data%20class%20transforms%C2%B6)).
For example, Pydantic’s `BaseModel` or attrs’ `@define` can use this so that type checkers know that after applying the decorator, the class has an `__init__` with parameters corresponding to the annotated fields.
This is a more advanced feature primarily for library developers to improve user experience of static typing when using those libraries.

## Forward References and Postponed Evaluation

### Forward References

It’s common to have types that refer to classes or types not yet defined (e.g., a method in class `A` that returns an instance of class `B` defined later in the file).
To handle this, Python allows using **string literals** in annotations for forward references.
For example:

```python
# example_18.py
class Node:
    def add_child(self, child: "Node") -> None: ...
```

Without the quotes, `Node` wouldn’t be defined at the time of evaluation of the annotation.
Quoted annotations defer evaluation of that name.
In Python 3.7+, an alternative to quoting every forward reference is to use `from __future__ import annotations`, which causes all annotations to be stored as strings by default (PEP 563).
This “postponed evaluation” was optional in 3.7–3.9 and was meant to become the default behavior in Python 3.10. However, that plan was revised:
**PEP 563’s default activation was put on hold** ([What’s New In Python 3.11 — Python 3.13.2 documentation](https://docs.python.org/3/whatsnew/3.11.html#:~:text=PEP%20563%20may%20not%20be,the%20future%C2%B6)).
The Python steering council decided not to turn on the automatic stringification by default due to various issues it caused for runtime introspection and decided to explore a different approach (PEP 649).

### PEP 649 (Deferred Annotations)

PEP 649, accepted for Python’s future (targeted for 3.13+), proposes a new mechanism where annotations are neither evaluated at function definition time nor stored as strings.
Instead, annotations would be stored as code in a special function (`__annotate__`) that computes them on demand ([PEP 649 – Deferred Evaluation Of Annotations Using Descriptors | peps.python.org](https://peps.python.org/pep-0649/#:~:text=Python%20solved%20this%20by%20accepting,for%20runtime%20users%20of%20annotations)) ([PEP 649 – Deferred Evaluation Of Annotations Using Descriptors | peps.python.org](https://peps.python.org/pep-0649/#:~:text=approach%2C%20when%20combined%20with%20a,foster%20future%20innovations%20in%20annotations)).
This aims to solve forward references and performance issues more elegantly:
the evaluation of annotations is deferred until needed, without losing the actual object references or incurring the issues of stringified annotations.
As of the latest Python (3.12), this is still in progress – by default, Python 3.12 still evaluates annotations normally (unless you use the future import).
When writing modern code, you can rely on `from __future__ import annotations` to handle most forward references conveniently (or just use quotes for specific cases).
Static type checkers themselves resolve forward references even if you leave them as raw names, so this is mostly a runtime concern for introspection via `inspect.get_annotations` or similar.
The takeaway:
**forward references** are supported via quoting or future imports, and the language is evolving to make annotation evaluation **lazy by default** in a robust way ([What’s New In Python 3.11 — Python 3.13.2 documentation](https://docs.python.org/3/whatsnew/3.11.html#:~:text=PEP%20563%20may%20not%20be,the%20future%C2%B6)).

## Tools, Stubs, and Best Practices

### Type Checkers and IDE Support

To make the most of type annotations, use a static type checker (like **mypy**, **pyright**, **Pyre**) or an IDE with built-in checking (PyCharm, VS Code, etc.).
These tools will read your annotations and warn you of type mismatches, missing return statements for functions declared to return non-`None`, improper overrides, etc.
The type system is standardized enough that most checkers agree on core behavior ([PEP 484 – Type Hints | peps.python.org](https://peps.python.org/pep-0484/#:~:text=Of%20these%20goals%2C%20static%20analysis,for%20code%20completion%20and%20refactoring)).
You can customize their strictness (for example, disallowing implicit `Any` types).
Run these checkers as part of your development or CI process to catch bugs early.

### Stub Files (PEP 484 & PEP 561)

If you are using a library that isn’t annotated, or you cannot modify source code to add annotations (e.g. C extension modules or third-party code), you can use *stub files* (`.pyi` files) to provide type information.
A stub file is a skeletal version of a module with only `pass` statements and type hints.
PEP 561 describes how libraries can distribute these stubs so that your type checker picks them up ([Distributing type information — typing documentation](https://typing.python.org/en/latest/spec/distributing.html#:~:text=Distributing%20type%20information%20%E2%80%94%20typing,Stub%20files%20serve)).
For instance, popular libraries often ship a `py.typed` marker and include inline types or separate stub packages (e.g. `types-requests`).
As a user, you typically don’t need to write stub files unless you’re providing types for an untyped library or doing something very dynamic.
But it’s good to know that the ecosystem supports them, enabling gradual adoption of typing even for older code.

### General Best Practices

- *Adopt Gradually:* You don’t have to annotate everything at once.
  It’s common to start by annotating function signatures of key modules or adding stubs for critical libraries.
  Unannotated code defaults to `Any` types, which type checkers will by default let pass (or you can configure them to be strict).
- *Be Comprehensive in Signatures:* For a function that you’re annotating, try to annotate **all parameters and the return type**.
  Partial annotations can sometimes mislead type inference.
  If a function returns nothing, use `-> None` for clarity ([PEP 484 – Type Hints | peps.python.org](https://peps.python.org/pep-0484/#:~:text=cannot%20be%20represented%20using%20the,available%20type%20notation)).
  If a parameter has a default, remember that doesn’t automatically make it Optional unless you intend `None` as a valid value ([typing — Support for type hints — Python 3.13.2 documentation](https://docs.python.org/3/library/typing.html#:~:text=%60Optional,X%2C%20None)).
- *Prefer Specific Types or Protocols:* When annotating arguments, use the most general type that works for your function (Liskov substitution principle).
  For example, if your function only needs to read from a collection, annotate it as `Iterable[T]` or `Sequence[T]` instead of `list[T]`, to allow more types (like tuples, sets) ([Typing Best Practices — typing documentation](https://typing.python.org/en/latest/reference/best_practices.html#:~:text=For%20arguments%2C%20prefer%20protocols%20and,Any)).
  If a parameter can be any object with a certain method, consider using a Protocol instead of a concrete class.
  Conversely, for return types, it’s usually best to be as specific as possible (don’t return `Any` if you can return a concrete type).
- *Use Modern Syntax:* Prefer the new concise annotation syntax that Python now supports.
  This means using built-in collection types (e.g. `list[int]` rather than `typing.List[int]`) ([Typing Best Practices — typing documentation](https://typing.python.org/en/latest/reference/best_practices.html#:~:text=Use%20built,where%20possible)), using `X | Y` for unions rather than `typing.Union[X, Y]` ([typing — Support for type hints — Python 3.13.2 documentation](https://docs.python.org/3/library/typing.html#:~:text=Union%20type%3B%20%60Union,means%20either%20X%20or%20Y)), and `X | None` instead of `typing.Optional[X]`.
  These make annotations more readable.
  The older syntax is still accepted for compatibility, but the newer syntax is encouraged in current code.
- *Limit `Any` and Unsafe Casts:* Try to avoid using `Any` unless absolutely necessary.
  If you find yourself needing to bypass the type system (via casts or `# type: ignore` comments), consider if there’s a better way – such as using Union types, overloading, or restructuring code.
  If you do use `Any` (for example, when interfacing with dynamically typed libraries), isolate it at the boundary of your code.
- *Leverage Type Narrowing:* Write code in a type-friendly way.
  Use `isinstance` checks or guard functions (even custom TypeGuard functions) to narrow types, instead of, say, `assert isinstance(x, SomeType)` which some type checkers might not understand.
  Many checkers can infer that after `if isinstance(obj, str): ... else: ...`, in the else branch `obj` is not a str.
  This makes your code safer and your type checker happier.
- *Keep Types Up to Date:* Treat type hints as part of the code documentation.
  If the code changes, update the annotations to match.
  Inconsistencies between code and annotations can be more confusing than no annotations.
  Running a type checker will catch these mismatches.
- *Performance Consideration:* Annotations are designed to have minimal runtime overhead.
  They’re stored as metadata and can be turned into strings with `from __future__ import annotations`.
  Unless you introspect them at runtime (with `typing.get_type_hints()`), they won’t slow down your program.
  That said, using a type checker in development might slightly slow down your build/test cycle, but it’s usually worth the trade-off for the bugs it prevents.

Each of these topics is elaborated in the official [Python typing documentation](https://docs.python.org/3/library/typing.html) and Python Enhancement Proposals.
For further reading, the [“Typing Cheat Sheet” for Python](https://mypy.readthedocs.io/en/stable/cheat_sheet_py3.html) ([typing — Support for type hints — Python 3.13.2 documentation](https://docs.python.org/3/library/typing.html#:~:text=%E2%80%9CTyping%20cheat%20sheet%E2%80%9D)) and the **Static Typing** section on Python’s documentation site ([typing — Support for type hints — Python 3.13.2 documentation](https://docs.python.org/3/library/typing.html#:~:text=%E2%80%9CType%20System%20Reference%E2%80%9D%20section%20of,the%20mypy%20docs)) are excellent resources.
They provide code examples and deeper explanations for advanced scenarios, helping you stay up-to-date with the evolving landscape of type annotations in modern Python.
