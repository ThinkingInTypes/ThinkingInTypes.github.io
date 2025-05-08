# Structural Typing

In type systems, there are two fundamental ways to decide if one type is compatible with another:
_nominal typing_ and _structural typing_.
Nominal typing (name-based typing) means type compatibility is determined by explicit declarations and the class hierarchy--an object's type is what its class name (or inheritance) says it is.
For example, if class `Dog` inherits from class `Animal`, then `Dog` _is-a_ subtype of `Animal` by definition, and a `Dog` instance can be used wherever an `Animal` is expected.
This is how traditional object-oriented languages like Java or C++ work, and it's also the primary mode in Python's type system by default.

On the other hand, structural typing determines type compatibility by the actual structure or capabilities of the object, not its explicit inheritance.
In a structural type system, if an object has all the required methods and attributes of a type, then it qualifies as that type, regardless of its class name or parent classes.
In other words, if it "walks like a duck and quacks like a duck, then it's treated as a duck."
This is the essence of the famous _duck typing_ principle.

Duck typing is a runtime concept in Python:
you invoke methods or attributes on an object, and as long as it supports those operations, things work (if a required method is missing, you get an `AttributeError` at runtime).
Structural typing can be seen as the static, compile-time equivalent of duck typing.
Instead of waiting for a runtime error, a structural type system (with the help of a static type checker) can verify ahead of time that an object has the necessary attributes to be used in a given context.
This approach is more flexible than nominal typing because it doesn't require pre-planned inheritance relationships.
It is also more explicit and safe than unguarded duck typing because the structure is checked (by a type checker) before the code runs.

Python historically embraced duck typing at runtime--you call methods on objects and trust they exist.
Prior to Python 3.8, static type checking in Python (via tools like MyPy, PyRight, etc.)
was largely nominal:
you would use abstract base classes or concrete classes to hint the types, and an object's class had to match the annotation or inherit from a matching class.
This could make it awkward to type-hint code written in a duck-typed style.
For instance, if you had a function that worked with any object that had a `.read()` method, there wasn't a straightforward way to express that in a type hint without making all such objects share a common base class or using `typing.Any`.
Python 3.8 remedied this by introducing _protocols_ in the `typing` module.
A protocol defines a _structural interface_ that other classes can fulfill just by having the right methods/attributes, without inheritance.
This brings the flexibility of duck typing into the realm of static type checking--essentially formalizing "If it quacks like a duck, it can be treated as a duck" in the type system.

In summary, nominal typing ties compatibility to declared relationships (e.g., subclassing an interface or abstract class), whereas structural typing ties compatibility to an object's actual shape (the presence of specific methods/attributes).
Python's type system now supports both:
use nominal typing for clarity and runtime consistency with class relationships, and use structural typing (via protocols) for flexibility and to more directly model Python's duck-typed nature.

## Defining and Using Protocols

To leverage structural typing in Python's type hints, you define _protocols_.
A protocol in Python is essentially an interface or template for a set of methods and attributes.
It's defined by inheriting from `typing.Protocol` (available in the standard library `typing` module as of Python 3.8, or in `typing_extensions` for earlier versions).
By creating a class that subclasses
`Protocol`, you declare a group of methods and properties that form a "protocol."
Static type checkers consider any class with those methods and properties (with compatible types) an implementation of that protocol, even if it doesn't formally inherit from the protocol.

**To define a protocol:** Create a class that inherits `Protocol` and define the method signatures (and any attribute types) that are required.
Protocol methods typically have empty bodies (often using `...` or `pass`) because you're not providing an implementation, just a definition of the interface.
For example, suppose we want a protocol for "speaking" creatures or objects:
it should have a method `speak()` that returns a string.
We can define:

```python
# speaker.py
from typing import Protocol


class Speaker(Protocol):
    def speak(self) -> str: ...
```

Here, `Speaker` is a protocol that any "speaker" object should follow.
Now, any class that defines a `speak(self) -> str` method is considered a `Speaker` for typing purposes.
We can create two completely unrelated classes that fulfill this protocol without explicit inheritance:

```python
# announce.py
from speaker import Speaker


class Dog:
    def speak(self) -> str:
        return "woof"


class Robot:
    def speak(self) -> str:
        return "beep-boop"


def announce(speaker: Speaker) -> None:
    # `speaker` can be any object with .speak() returning str
    print("Announcement:", speaker.speak())


announce(Dog())  # OK, Dog has speak()
## Announcement: woof
announce(Robot())  # OK, Robot has speak()
## Announcement: beep-boop
```

Even though `Dog` and `Robot` do not inherit from `Speaker` (and are not related to each other at all), the static type checker will accept them as valid arguments to `announce` because they structurally conform to the `Speaker` protocol by implementing the required method.
This is the power of structural typing.
The type checker treats `Dog` and `Robot` as subtypes of `Speaker` because they have the right `speak()` method signature.
If we tried to pass an object that lacks a `speak()` method (or has an incompatible signature), the type checker would flag an error, ensuring type safety.

It's important to note that protocols are primarily a static concept--they are enforced by type checkers, not by the Python runtime (by default).
Unlike an abstract base class (ABC), a protocol doesn't require classes to formally subclass it, and Python will not produce an error at runtime if a required method is missing.
For example, in the code above, if we call `announce(Dog())` and `Dog.speak` is missing or misnamed, we would only find out at runtime via an `AttributeError`.
The protocol helps catch such issues before runtime by using tools like Mypy.
The protocols defined in `typing` are optional and have no runtime effect on their own.
This means you can use them freely for type hints without incurring runtime overhead or restrictions.
Protocols do inherit from `abc.ABC` under the hood,
but by default `isinstance()` and `issubclass()` checks against a protocol will not work without an explicit opt-in.

**Using a protocol in type hints:** Once you have a protocol class, you use it as a type in annotations just like you would use an ABC or a concrete class.
In the above example, the function `announce` was annotated to accept a `Speaker`.
That tells readers and type checkers that any argument should "speak."
This is more expressive than using a base class like `Animal` or a union of types--we directly specify the capability we need.
Another example:
Python's standard library defines an `Iterable[T]` protocol (in `collections.abc` or `typing`) that essentially says the object has an `__iter__` method returning an iterator.
If you annotate a function parameter as `Iterable[str]`, any object that can be iterated over to yield strings is accepted--whether it's a list, a tuple, a custom container class with an `__iter__`, etc.
The type checker doesn't require them to inherit from `Iterable`; having the method is enough.
This demonstrates that many idiomatic Python "protocols" (iteration, context managers, etc.)
are recognized structurally.
Python's typing module and static checkers come with several predefined protocols (either explicitly as in `typing.Protocol` classes or implicitly via ABCs with structural hooks) for common patterns.

Let's look at a slightly more elaborate example of defining and using a protocol.
Imagine we have objects that need to support a `close()` method (like files or network connections).
We can define a protocol `Closable` and use it to write a function that closes a batch of resources:

```python
# file_resource.py
from typing import Protocol


class Closable(Protocol):
    def close(self) -> None: ...


class FileResource:
    def __init__(self, path: str):
        self.file = open(path, "w")

    def close(self) -> None:
        self.file.close()


class SocketResource:
    def close(self) -> None:
        print("Socket closed")
```

```python
# file_resource_demo.py
from file_resource import (
    Closable,
    FileResource,
    SocketResource,
)
from typing import Iterable


def close_all(resources: Iterable[Closable]) -> None:
    for res in resources:
        res.close()


# All these have a close():
closables = (
    FileResource("data.txt"),
    SocketResource(),
    open("other.txt", "w"),
)
close_all(closables)
## Socket closed
```

In this code, `Closable` is a protocol requiring a `.close()` method.
We created a `FileResource` class and a `SocketResource` class that both implement `close()`.
We also use a built-in file object from `open()`, which we know has a `close()` method.
The `close_all` function is annotated to accept any iterable of `Closable` objects.
Thanks to structural typing, it doesn't matter that these objects are of different types and don't share a common ancestor named `Closable`--as long as each has a callable `close()` method, the static type checker is satisfied and, at runtime, the code will work.
Mypy considers the built-in file object and our custom classes all as subtypes of `Closable` because they provide the required attribute.

One thing to be aware of:
protocols by default cannot be used with `isinstance()` or `issubclass()` checks at runtime.
If you try `isinstance(some_obj, Closable)` in the above example, Python will raise a `TypeError` unless you take additional steps.
This is because the protocol is not a real base class of those objects (they never inherited from it).
However, Python's `typing` module provides a decorator `@runtime_checkable` that you can apply to a protocol to make runtime `isinstance` checks possible on it.
Marking a protocol with `@runtime_checkable` means it gets a special `__instancecheck__` that will return True if the object has the required attributes (much like ABCs in `collections.abc` do with their `__subclasshook__`).
For example:

```python
# example_4.py
from typing import runtime_checkable, Protocol
from file_resource import FileResource


@runtime_checkable
class Closable(Protocol):
    def close(self) -> None: ...


# FileResource has close():
print(isinstance(FileResource("data.txt"), Closable))
## True
```

Now `Closable` can be used in `isinstance` and `issubclass` as a structural check.
Use this feature carefully; it's useful for type introspection in frameworks or for asserting an object meets an interface at runtime.
However, it only checks the presence of attributes and not their types and could give false positives if an attribute name matches, but semantics differ.
In most cases, protocols are used purely for static checking and documentation.

## Practical Protocol Examples

Protocols shine in real-world scenarios where you want to decouple code and reduce dependencies on concrete classes.
A common use case is _dependency injection_ and testing.
In Python, it's common to write functions or classes that operate on objects with a particular interface without caring about the concrete implementation.
Protocols let you formally capture that interface in the type system.
This makes your code's expectations clear and allows static analysis to validate those expectations.
Let's discuss a few practical examples.

**1. Dependency injection and interchangeable components:**
Suppose you're writing a service that needs to log messages.
You might want the ability to swap out the logger--sometimes logging to a file, sometimes to the console, or maybe collecting logs in memory for testing.
You can define a protocol for the logger's interface and program against that.
For instance:

```python
# logger_protocol.py
from contextlib import AbstractContextManager
from pathlib import Path
from typing import Protocol


class Logger(Protocol):
    def log(self, message: str) -> None: ...


class FileLogger(AbstractContextManager):
    """
    Logger that writes to a known log file in a fixed directory.
    """

    def __init__(self, path: Path = Path("./log.txt")):
        path.parent.mkdir(parents=True, exist_ok=True)
        self.filename = path
        self._file = self.filename.open("w", encoding="utf-8")

    def log(self, message: str) -> None:
        self._file.write(message + "\n")
        self._file.flush()

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        self._file.close()


class ListLogger:
    """
    Logger that stores messages in a list
    """

    def __init__(self):
        self.messages: list[str] = []

    def log(self, message: str) -> None:
        self.messages.append(message)


def run_process(task_name: str, logger: Logger) -> None:
    logger.log(f"Starting {task_name}")
    # Perform the task ...
    logger.log(f"Finished {task_name}")
```

In `Logger(Protocol)`, we specify that a logger must have a `.log(str)` method.
Our `run_process` function doesn't care _how_ the logging is done, just that the object passed in can `.log` a message.
`FileLogger` and `ListLogger` are two implementations--one writes to a file, the other stores messages in a Python list.
Notice that neither`FileLogger`nor`ListLogger`subclasses`Logger`; they don't need to.
They implicitly satisfy the protocol by having the correct`log`method.
This design is very flexible: you can add new logger classes later (say, a`DatabaseLogger`that writes to a database, or reuse Python's built-in`logging.Logger`by writing an adapter with a`log`method) without changing the code that uses the logger.

Here, `FileLogger` stores results in `log.txt`, and we can use`ListLogger`to capture logs and make assertions on them:

```python
# logger_protocol_demo.py
from logger_protocol import (
    FileLogger,
    ListLogger,
    run_process,
)

with FileLogger() as file_logger:
    run_process("DataCleanup", file_logger)
    print(f"log file: {file_logger.filename}")
    print(file_logger.filename.read_text(encoding="utf-8"))
## log file: log.txt
## Starting DataCleanup
## Finished DataCleanup

# logs to list in memory:
test_logger = ListLogger()
run_process("DataCleanup", test_logger)
print("Captured logs:", test_logger.messages)
## Captured logs: ['Starting DataCleanup',
## 'Finished DataCleanup']
```

The static type checker ensures that any object we pass as a`logger`to`run_process`has a`log(str)`method.
In a nominal type system, you might have to define an abstract base class`Logger` and make every logger inherit it.
With protocols, you get the benefit of an interface without inheritance.
This reduces coupling and makes it easier to integrate third-party classes that weren't written with your ABC in mind.

**2. Testing with fake or mock objects:**
Building on the above example, protocols are extremely handy for unit testing.
In tests, we often use fake objects or mocks to simulate real components (like databases, web services, etc.)
without having to perform the real operations.
With protocols, you can give those test doubles a clear interface.
For example, if you have a function that fetches data from an API, you could define a protocol for the fetcher.
In production, you pass a real HTTP client, in tests you pass a fake object that returns predetermined data.
The protocol assures the fake has the same method signature as the real client.
This avoids type checker warnings and makes tests cleaner.
It's essentially the static typing analog of using an interface in other languages for dependency injection in tests.
Many testing libraries (like `unittest.mock`) create dynamic mocks that can be configured with attributes on the fly; to type-annotate those, you can either cast them to a Protocol or use a Protocol as a base for a fake implementation.
Using protocols in this way documents exactly what methods a mock is expected to provide.
This can prevent situations where your test double is missing a method or has a typo that wouldn't be caught until runtime.
In short, whenever you say "I need an object that can do X in my code, and I might swap different implementations of it," that's a cue to define a protocol for X.

**3.Interface design and third-party integration:**
Protocols can serve as interfaces in your application design.
Even if you're not writing multiple implementations immediately, defining a protocol for a role in your system can clarify the design.
For example, you might define a `DataStore` protocol with methods like `save(item)` and `load(id)` that any storage backend should implement.
Today you only have a database implementation, but tomorrow you might add an in-memory or file-based implementation--the protocol makes the contract clear.
Moreover, if you want to accept objects from a third-party library with the necessary methods, protocols let you do so without subclassing or modifying those classes.
Suppose you're writing a function that can output data to any "file-like" object (something with a `.write()` method).
The `io.TextIOBase` abstract class in Python is nominal, but not every file-like object will inherit it.
By defining your own protocol with a `write(str)` method, your function can accept a wide range of objects (actual file handles, `io.StringIO` instances, custom writer objects) as long as they implement `write`.
This is especially useful when working with libraries that weren't built with your interfaces; you can adapt them via protocols instead of being forced into their class hierarchy.
Protocols thus increase the reusability and extensibility of your code by focusing on what an object can do rather than what it is.

It's worth mentioning that Python's standard library and frameworks have embraced the concept of protocols (even before the formal `Protocol` type existed) by using "duck typing" and abstract base classes.
For instance, the act of iterating in Python checks for an `__iter__` method--any object with `__iter__` is iterable.
The static typing system knows this too:
you don't have to explicitly register your class as an `Iterable` ABC; if it has the right method, tools like Mypy will treat it as iterable.
With `Protocol`, we can create our own such abstractions.
In modern Python, the combination of protocols and `@runtime_checkable` even lets us approximate some features of a language with a built-in interface system.

**4.
Composition and adapters using protocols:** Another practical pattern is using protocols to enable composition and decorators.
Because protocols don't require inheritance, you can make wrapper classes that add functionality while still conforming to an interface.
For example, you might have a basic service class and then a logging wrapper class that takes a service and also implements the same service protocol to proxy calls and add logging.
As long as both implement the protocol, code using the protocol can accept either the plain or the wrapped version.
This was illustrated by defining an `AddServiceProtocol` for an addition service and creating both a normal implementation and a logging decorator implementation that forwards calls.
The key takeaway is that structural typing focuses on the behavior, so even objects that don't share lineage can work together if they fulfill the same behavioral contract.

## Combining Dataclasses with Protocols

```python
# dataclasses_and_protocols.py
from dataclasses import dataclass
from typing import Protocol


class Identifiable(Protocol):
    id: int


@dataclass
class User:
    id: int
    name: str


@dataclass
class Product:
    id: int
    price: float


def print_id(entity: Identifiable) -> None:
    print(f"ID: {entity.id}")


print_id(User(1, "Alice"))
## ID: 1
print_id(Product(101, 19.99))
## ID: 101
```

## Combining Protocols with Generics

Just like classes and functions can be generic (using `TypeVar` to operate over a range of types), protocol classes can be generic as well.
A _generic protocol_ allows you to define a protocol parameterized by a type (or multiple types), enabling more precise typing of method arguments and return values.
Many built-in protocols are generic--for example, `Iterable[T]` is a protocol that can be `Iterable[int]`, `Iterable[str]`, etc., depending on what type it yields.
We can do the same with our own protocols.

To define a generic protocol, we use `TypeVar` and put the type variable in brackets after `Protocol` when defining the class.
Let's say we want to define a container protocol that yields items of some type.
We can make it generic so that a `Container[int]` is a protocol for "container of ints" and `Container[str]` for "container of strings," but both are based on the same generic interface.
For example:

```python
# container.py
from typing import Protocol, TypeVar

T = TypeVar("T", covariant=True)


class Container(Protocol[T]):
    def get_item(self) -> T: ...
```

Here, `Container[T]` is a generic protocol with a single type variable `T`.
It specifies one method `get_item` that returns an object of type `T`.
Now we can implement this protocol for different types by providing concrete type parameters.
For instance, a container of strings and a container of integers:

```python
# container_types.py
class StringContainer:
    def __init__(self, value: str):
        self.value = value

    def get_item(self) -> str:
        return self.value


class IntContainer:
    def __init__(self, value: int):
        self.value = value

    def get_item(self) -> int:
        return self.value
```

`StringContainer` and `IntContainer` each implement `get_item` returning the appropriate type.
They don't subclass `Container`, but structurally they match `Container[str]` and `Container[int]` respectively.
We can write functions that use the generic protocol to accept any kind of container and preserve the type information of the contained item:

```python
# generic_function.py
from typing import TypeVar
from container import Container, T
from container_types import StringContainer, IntContainer


def print_item_and_return(container: Container[T]) -> T:
    item = container.get_item()
    print(f"{item = }, {type(item) = }")
    return item  # Type inferred as C


# Use generic function with different container types:
x: str = print_item_and_return(StringContainer("hello"))
## item = 'hello', type(item) = <class 'str'>
y: int = print_item_and_return(IntContainer(42))
## item = 42, type(item) = <class 'int'>
```

In the function `print_item_and_return`, we used `C` (could also use `T` again) as a type variable for the container's item type.
When we call this function with a `StringContainer`, the type checker knows `C` is `str` in that call, so it infers that the function returns a `str`.
Similarly, with `IntContainer`, `C` becomes `int`.
This is the benefit of generic protocols:
they let you write flexible code that is still type-safe and retains specific type information.
In other words, one protocol can work for many types without losing the ability to distinguish those types when it matters.
The syntax we used (`Container[C]` inside the function annotation) leverages Python's ability to support generics in type hints.
Under the hood, `Container[int]` is a _parameterized protocol_ instance, but conceptually you can think of it like an interface template.

Keep in mind that user-defined generic protocols follow the same rules as normal generic classes for type checking.
You can declare variance for type variables if needed (covariant, contravariant) using `typing.Final` or by special syntax in `TypeVar`, although if you don't declare, the type checker will assume invariance (meaning `Container[SubClass]` is not a subtype of
`Container[BaseClass]` unless you marked variance).
In our container example, this is not an issue because we're primarily using it to carry the exact type.

Another scenario for combining protocols with generics is when you want to put protocols as bounds on `TypeVar`s.
For instance, you can declare `T = TypeVar('T', bound=SomeProtocol)` to indicate that a type variable must satisfy a certain protocol.
This is analogous to saying, "T must be a subtype of this Protocol," except since protocols aren't part of the class hierarchy, it really means any type used for T must structurally implement the protocol.
For example, if we have:

```python
# example_9.py
from typing import TypeVar
from logger_protocol import Logger

T = TypeVar("T", bound=Logger)
```

This means any type filling in for T must have a `.log(str) -> None` method.
You could use such a bound in a generic function or class to ensure the operations you perform on T (like calling `log`) are valid.
This is a powerful way to write generic algorithms that operate on any objects meeting a certain interface, without tying them to a base class.

It's also worth noting that Python 3.12 introduced an even more concise way to define generic protocols (and generic classes in general) by allowing type variables in the definition of methods directly (PEP 695--Type Parameter Syntax).
For instance, one could write something like:

```python
# generic_method_in_protocol.py
from typing import Protocol, TypeVar

T = TypeVar("T")


class Container(Protocol):
    def get_item(self, type_: type[T]) -> T: ...
```

This defines a generic method `get_item` in a protocol.
However, under the hood this still creates a generic protocol with a type variable `T`.
Most code at the time of writing still uses the earlier syntax with explicit `TypeVar` declarations, which is what we've shown above.

In summary, combining protocols with generics lets you express very flexible and reusable type relationships.
You can create protocols that work over a family of types while still preserving type information.
Many of Python's built-in protocols are generic (for example, an iterator protocol `Iterator[T]` yields items of type T), and you can do the same in your own designs.
This enables things like container types, numeric operations, or callback interfaces to be both generic and structural.
When designing a generic protocol, think about what parts of the interface should change with the type (those become type variables) and which are fixed.
The result is a very powerful abstraction that remains easy to use.

## When to Choose Structural Typing Over Nominal Typing

Now that we've explored what structural typing (via protocols) and nominal typing (via concrete classes or ABCs) offer, a natural question arises:
When should you use one over the other? The answer often depends on the context and goals.
Both approaches have their strengths, and in Python they complement each other rather than one completely replacing the other.
Here are some guidelines, pros and cons, and best practices to help decide:

**Use nominal typing (classes/ABCs) when:**

- You want to reuse code via inheritance.
  If you have default method implementations or shared attributes that can be defined in a base class, an abstract base class can provide that.
  Inheritance isn't the only way to reuse code, but when it makes sense
  (e.g., a base class providing common functionality), nominal typing naturally goes along with it because subclasses inherit from the base.

- You need a strict class hierarchy or runtime type information.
  If it's important in your design to maintain actual subclass relationships (perhaps for identity checks, `isinstance` checks, or because you rely on Python's method resolution order and `super()` calls), then using nominal types is appropriate.
  For example, if you have a plugin system where all plugins must register as subclasses of `BasePlugin` to be discovered, that's a nominal approach.

- The interface is large or complex, with many methods, and tightly coupled to an implementation.
  While you could model this with a protocol, it may be clearer to use an abstract class to group behavior.
  If multiple methods are meant to be overridden together, an ABC can enforce that at instantiation time (trying to instantiate a subclass that hasn't implemented all abstract methods raises an error).
  In short, for class designs that naturally form an "is-a" hierarchy and possibly share some code, nominal typing fits well.

**Use structural typing (protocols) when:**

- You want to keep it lightweight and focused purely on the method/attribute requirements.
  Protocols are great for defining a narrow interface that multiple disparate classes can implement without formal coupling.
  If you only care about one or a few methods on an object (and not about its exact type), a protocol lets you specify just that.
  This is especially useful for function parameters:
  you can annotate a function to accept any object with a `.close()` method, or a `.write()` method, etc., without forcing a common base class.

- You are working with third-party or existing classes that you can't modify to fit into your class hierarchy.
  Structural typing shines here because you can define a protocol that matches the external class's abilities.
  For example, if a third-party library gives you objects that have a `.to_json()` method,
  and you want to treat those objects uniformly in your code,
  you can create a `ToJsonable` protocol with `to_json(self) -> str` and use that in your type hints.
  Any object from the library will satisfy the protocol if it has the method,
  without you needing to make it inherit from anything.
  This decoupling is very powerful in a language as dynamic as Python,
  where often we "duck type" through frameworks--now you can put an actual type hint on it.

- You need generic interfaces or extension of existing ones.
  Protocols are useful for creating ad-hoc interfaces that might not have been foreseen initially.
  For instance, you might realize that two classes in different parts of your system happen to have similar methods for, say, resetting their state.
  You could retroactively define a `Resettable` protocol and update type hints to use it, without touching the classes themselves.
  If you later make those classes formally implement an ABC, fine--but the protocol gave you an immediate way to express the concept in types and check it.
  Additionally, if you're designing a library and want to allow users to plug in their own objects (as long as they have certain methods), providing a protocol in your public API documentation is a nice way to communicate that.
  Users can either implement that Protocol (statically) or just ensure their classes match the signature.

**Pros and Cons Summary:** Nominal typing (using concrete classes and ABCs) offers clarity in terms of design--it's very clear that ClassX is a kind of InterfaceY because it explicitly inherits it.
It also allows enforcement:
abstract base classes can ensure at runtime that certain methods are implemented (attempting to instantiate a subclass that hasn't implemented an abstract method will error out).
They can also provide default behavior.
However, nominal typing is less flexible--everything must be planned or adapted to fit the hierarchy.
If you want an external class to be treated as an InterfaceY, you might have to write an adapter or subclass it, which could be clunky or impossible (if you don't control that class).
Structural typing (using protocols) is extremely flexible and mirrors Python's dynamic nature--you get to "write the interface after the fact."
It encourages designing for capabilities rather than inheritance.
The downside is that protocols are primarily static--they rely on the developer running a type checker.
Python won't stop you from passing an object that does not fulfill the protocol (until you call a missing method and get an error at runtime, just like normal duck typing).
So if you need guaranteed enforcement in a running program, protocols alone won't give you that (they are optional).
That said, in a team or project using type checks as part of CI, protocols can prevent a lot of mistakes.
Another minor con is that protocols, if overused, could make it less obvious which classes actually implement which interface; with nominal typing you can always search for subclasses of an ABC.
A mix is often best: use protocols for the broad "this is what we expect" contracts, especially for external boundaries and flexible APIs, and use concrete classes or ABCs internally when you want more structure or reuse.

**Best practices:** It's not an either/or choice--you can use both in the same codebase.
For example, you might define an ABC with some default methods for a complex interface but also define a protocol for a subset of that interface for use in a more generic function.
Choose structural typing when you want minimal coupling and maximum flexibility, especially at boundaries of your system or for "pluggable" functionality.
Choose nominal typing when you want an explicit, enforced contract and possibly to leverage inheritance of code.
Remember that protocols are most valuable when you are using static type checking; if your project doesn't use type checks, then a protocol is a `abc.ABC` with no abstract methods--it won't enforce anything by itself at runtime.
In such cases, if enforcement is needed, an ABC with abstract methods (or even just documentation) might be better.
However, even in purely dynamic contexts, many developers find protocols useful as documentation:
by reading the Protocol class, you know what an object is expected to do.

In Python's type system evolution, protocols were introduced to complement nominal typing, not to replace it.
They give you the freedom to write code in the Pythonic duck-typed style while still reaping the benefits of static analysis.
A good guideline is to use protocols to describe roles that can be played by objects of different class hierarchies and use nominal typing for relationships within a class hierarchy.
By following these practices, you can make your code both flexible and robust, leveraging the best of both worlds in Python's type system.

## References

1. [Github Issues](https://github.com/ThinkingInTypes/ThinkingInTypes.github.io/issues)
2. [Protocols and structural subtyping--mypy 1.15.0 documentation](https://mypy.readthedocs.io/en/stable/protocols.html)
3. [What's the Difference Between Nominal, Structural, and Duck Typing?--DEV Community](https://dev.to/awwsmm/whats-the-difference-between-nominal-structural-and-duck-typing-11f8)
4. [Duck typing--Wikipedia](https://en.wikipedia.org/wiki/Duck_typing)
5. [Python Protocols: Leveraging Structural Subtyping--Real Python](https://realpython.com/python-protocol/)
6. [PEP 544--Protocols: Structural subtyping (static duck typing) | peps.python.org](https://peps.python.org/pep-0544/)
7. [Abstract Base Classes and Protocols--Justin A. Ellis](https://jellis18.github.io/post/2022-01-11-abc-vs-protocol/)
8. [Protocols and Composition in Python--DEV Community](https://dev.to/fwojciec/protocols-and-composition-in-python-8mm)
