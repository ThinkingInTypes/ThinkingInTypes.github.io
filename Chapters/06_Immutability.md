# Immutability

## Why Immutability Matters

Immutability--the inability to change an object or variable after its creation--offers several key benefits in software design.
By making data immutable, we greatly simplify the mental model needed to understand program state.
In particular, immutability makes programs easier to reason about by eliminating the possibility of unexpected changes to data.
This reduction in "the realm of possibility" for how data can evolve means fewer potential bugs and side effects in our code.
An immutable variable gives us one less thing to worry about when tracing through a program's logic, because once it's set, it won't arbitrarily change under us.

Another major benefit is safety in concurrent contexts.
In multithreaded code, shared mutable state is a common source of issues like data races.
Immutability helps prevent these by ensuring that once a shared object is created, threads can read it without needing locks or fear of one thread modifying it out from under another.
Even in single-threaded programs, immutability prevents accidental modifications that could lead to corrupted state.
With mutable state, a stray assignment or method call can silently alter data and introduce bugs that are hard to track down.
In contrast, if you attempt to modify an immutable piece of state, it will typically fail fast--either with a clear error at runtime or (ideally) an error caught by a static analysis tool before the code even runs.
This fail-fast behavior makes bugs much easier to detect and fix.

Some concrete advantages of embracing immutability:

- **Easier Reasoning:** You can trust that values won't change unexpectedly, making functions behave more predictably.
- **Thread-Safety:** Immutable objects can be freely shared between threads without synchronization, since no thread can alter them and cause race conditions.
- **Avoiding Bugs:** Accidental mutations are caught early--either by a runtime exception or by a type checker--instead of corrupting state silently.
- **Safe Sharing and Caching:** You can safely reuse or cache immutable objects (even as keys in dictionaries or members of sets) since their hash or contents won't change after creation.
  This aligns with Python's rule that objects used as dictionary keys must be immutable (e.g., using a tuple instead of a list for a key).

In summary, designing with immutability leads to code that is safer, more robust in concurrent environments, and easier to understand.
Python, as a dynamic language, doesn't enforce immutability by default, but it provides patterns and tools to achieve immutable-like behavior where beneficial.
Next, we'll explore how Python historically handles immutability through convention, and then dive into modern features for enforcing immutability via typing and dataclasses.

## Immutability by Convention in Python

Python does not have a built-in `const` declaration to make a variable truly immutable, nor does it allow truly unchangeable user-defined objects in all cases.
Instead, Python developers have traditionally relied on conventions and certain immutable built-in types to signal that something should not be changed.

One common convention is the use of ALL_CAPS names for constants.
According to PEP 8 (Python's style guide),
"constants are usually defined on a module level and written in all capital letters with underscores separating words".
For example, one might write:

```python
# example_1.py
MAX_OVERFLOW = 1000  # intended to be a constant
DATABASE_URL = (
    "postgres://localhost/db"  # constant configuration
)
```

By writing these names in uppercase, we indicate to other developers (and ourselves) that these values should be treated as immutable constants.
The Python interpreter won't stop you from reassigning `MAX_OVERFLOW` to a different value--this is purely a human convention--but following this naming scheme makes the code's intent clear.
Many linters will flag reassignment of all-caps "constant" variables as a potential issue, reinforcing the convention.

Another historical approach is to leverage Python's immutable built-in types.
Python itself has immutable types like `int`, `float`, `str`, `tuple`, and `frozenset`.
When you want to prevent modifications to a collection of values, you might use a tuple instead of a list, or a frozenset instead of a set.
For instance, if you have a fixed set of options, using a tuple (`options = ("red", "green", "blue")`) conveys that this sequence is not to be altered.
This isn't enforced by syntax, but the type's lack of mutating methods provides some safety.
Trying to call a mutating method on an immutable type will result in an `AttributeError` or a runtime error (for example, attempting to append to a tuple will fail since tuples have no `append` method).

In summary, before formal language support for immutability, Python developers used naming conventions and choice of immutable types to signal immutability.
This approach relies on discipline: the interpreter won't stop someone from breaking the rules, but clear conventions help maintain correctness.
Python's philosophy has long been _"we are all consenting adults here"_--meaning if someone really wants to mutate something, the language lets them, but by following conventions like all-caps constants and using immutable data types, you can largely avoid accidental mutations.

Modern Python, however, has introduced better ways to enforce immutability or at least catch mutations early.
The two main tools we'll discuss are the `Final` type hint (for variables and attributes that shouldn't be reassigned) and frozen dataclasses (for creating immutable data objects).
These provide a more formal way to achieve immutability beyond just convention.

## Using `Final` for Constants and Immutable References

Python 3.8 introduced the `Final` qualifier in the `typing` module (as described in ).
The `typing.Final` annotation allows you to declare that a name--whether a module-level variable, a class attribute, or an instance attribute--is intended to never be reassigned after its initialization.
This is a purely static indication; it's enforced by type checkers (like mypy, pyright, etc.), not by the Python runtime.

### Declaring Final Variables

To use it, import `Final` from `typing` and annotate your constant definitions.
For example:

```python
# example_2.py
from typing import Final

PI: Final[float] = 3.14159
MAX_CONNECTIONS: Final = 100  # type inferred as int
```

Here, `PI` and `MAX_CONNECTIONS` are marked as `Final`, signaling that these names should never be re-bound to a new value.
A type checker will enforce this.
If later in the code you attempt to do `PI = 3.14` (reassigning the constant), the type checker will emit an error, e.g.
"Error: can't assign to final attribute".
The same goes for changing `MAX_CONNECTIONS`.
The Python interpreter itself will not stop you from doing this reassignment, but using `Final` elevates the constant from a mere convention to something that static analysis tools can verify.

According to the Python typing documentation, _"Final names cannot be reassigned in any scope.
Final names declared in class scopes cannot be overridden in subclasses."_.
In other words, marking a variable as `Final` means:

- **No rebinding:** You can assign to it only once; the type checker flags subsequent assignments in code.
- **No override in subclass:** If you mark a class attribute as `Final`, a subclass cannot override that attribute with a new value.

Let's illustrate this with a quick example:

```python
# example_3.py
from typing import Final

RATE: Final = 3000


class BaseConfig:
    TIMEOUT: Final[int] = 60


class SubConfig(BaseConfig):
    # Error: can't override a final attribute in BaseConfig
    TIMEOUT = 30  # type: ignore
```

In the above code, `RATE` is a module-level constant.
If somewhere else we had `RATE = 2500`, a tool like mypy would report an error ("can't assign to final name 'RATE'").
Similarly, `BaseConfig.TIMEOUT` is a constant class attribute; attempting to override it in `SubConfig` would be flagged ("can't override a final attribute").
This helps maintain invariants in class hierarchies.

It's important to note that `Final` can also be used for instance attributes in `__init__`.
If you have an instance attribute that should only be set once (in the initializer) and never changed, you can annotate it with `Final` in the class body and then assign it in the constructor.
For example:

```python
# example_4.py
from typing import Final
from dataclasses import dataclass


@dataclass
class User:
    name: Final[str] = "Uninitialized"
    id: Final[int] = -1

    def __init__(self, name: str, id: int):
        object.__setattr__(self, "name", name)
        object.__setattr__(self, "id", id)
```

Here, `User.name` and `User.id` are intended to never change after the object is created.
We use `Final[str]` and `Final[int]` in the annotation.
The `__init__` uses `object.__setattr__` to bypass immutability enforcement (more on that technique in the next section about frozen dataclasses).
A type checker would ensure that no code later tries to reassign `user.name` or `user.id`.
For dataclasses, it's more idiomatic to use the `frozen=True` parameter (discussed below) rather than manually handling `Final` on instance attributes, but this example shows it's possible.

**Runtime behavior of Final:** At runtime, `Final` does not truly "freeze" the value.
It does not make the object itself immutable--it only prevents the name from being rebound in type-checked code.
For instance, if you declare `numbers: Final[list[int]] = [1, 2, 3]`, you are not supposed to reassign `numbers` to a new list, but you _can still mutate the list itself_ (e.g.
`numbers.append(4)` will succeed) because the list object is still mutable.
The type checker might warn you if the type is `Final[Sequence[int]]` instead (since `Sequence` has no `append` method), but with `Final[list[int]]` the list methods are available.
In short, marking something `Final` guarantees that the _name_ won't be re-bound to a different object, but it does not magically make the object's contents immutable.
If true immutability of the content is needed, combine `Final` with an immutable type (e.g., use a tuple or use an immutable interface like `Sequence` instead of `list`).
For example:

```python
# example_5.py
from typing import Final, Sequence

data1: Final = [
    1,
    2,
    3,
]  # `data1` won't be re-assigned, but list can mutate
data2: Final[Sequence[int]] = [
    1,
    2,
    3,
]  # `data2` treated as Sequence, so no mutation methods
```

In the above, `data1.append(4)` is allowed by the type system (though `data1` name can't be re-bound), whereas `data2.append(4)` would be rejected by a type checker because a `Sequence[int]` is assumed to be immutable (it lacks an `append` method).
This demonstrates the difference between preventing reassignment of a variable and ensuring true immutability of the object.

Finally, note that Python also provides a `@final` decorator in `typing` which can be applied to classes or methods.
This is related to immutability in the sense of preventing changes in inheritance.
Decorating a class with `@final` means you intend it not to be subclassed, and a type checker will flag any subclass attempt as an error.
Similarly, marking a method with `@final` means it should not be overridden in any subclass.
This is more about preventing _behavioral modification_ via inheritance rather than value mutation.
It can be useful in design to ensure certain classes remain closed for extension (similar to `final` classes in Java).
At runtime, as of Python 3.11, the `@final` decorator sets a `__final__ = True` attribute on the class or function to help introspection, but it doesn't enforce anything on its own.
Like the `Final` annotation, `@final` is a tool for communicating intent and catching errors early with the help of static analysis.

In summary, `Final` in Python typing is a lightweight way to get some of the benefits of immutability by preventing reassignments.
It formalizes the "ALL_CAPS means constant" convention into something a type checker can understand.
Combined with immutable types or interfaces, it can help you create APIs that promise not to mutate state.
However, for more complex state (especially when you want to bundle multiple values), Python's dataclasses offer another approach to enforce immutability at runtime.

## Immutable Data Classes

Functional programming strongly advocates immutability, preventing accidental changes and thus simplifying reasoning about your code.
By default, dataclass instances are mutable (their fields can be assigned to freely).
However, `dataclasses` support an immutability feature: if you specify `frozen=True` in the `@dataclass` decorator, the resulting class will prevent any assignment to its fields after object creation.
In other words, a frozen dataclass instance is effectively immutable (or "frozen") once it's constructed.

```python
# example_6.py
from dataclasses import dataclass

from book_utils import Catch


@dataclass(frozen=True)
class Point:
    x: int
    y: int


p = Point(x=1, y=2)
print(p.x, p.y)  # Outputs: 1 2
## 1 2

with Catch():
    # Attempting to modify a field produces an error:
    p.x = 5  # type: ignore
## Error: cannot assign to field 'x'

p.__dict__["x"] = 5  # Bypassing 'frozen'
```

Running this code will result in a runtime error at the line `p.x = 5`.
Specifically, Python will raise a `dataclasses.FrozenInstanceError` with the message "cannot assign to field 'x'".
The dataclass machinery has made the `Point` class's instances immutable by overriding the attribute-setting behavior: any attempt to set an attribute on a frozen instance triggers that exception.

Under the hood, when you use `@dataclass(frozen=True)`, Python generates an `__setattr__` method (and a `__delattr__` method) for your class that intercepts all attempts to set or delete attributes and immediately throws a `FrozenInstanceError`.
This effectively locks down the instance after `__init__` finishes.
The exception `FrozenInstanceError` is a subclass of `AttributeError`, which is consistent with what Python normally throws if you try to assign to a read-only attribute.

Because of this, frozen dataclasses give you actual runtime enforcement of immutability.
Unlike the `Final` type hint, which is only checked by static analyzers, a frozen dataclass will actively prevent mutation in a running program.
This can be a powerful tool for ensuring certain objects remain constant.
It's especially handy for value objects (like points, coordinates, config objects, etc.) where you want to make sure their state doesn't change once created.

### Example: Frozen Dataclass in Action

Let's illustrate with a more detailed example and show what happens if we attempt mutation:

```python
# frozen_person.py
from dataclasses import dataclass

from book_utils import Catch


@dataclass(frozen=True)
class Person:
    name: str
    age: int


person = Person(name="Alice", age=30)
print(person.name)  # "Alice"
## Alice
with Catch():
    # Trying to modify a frozen dataclass field:
    person.age = 31  # type: ignore
## Error: cannot assign to field 'age'

person.__dict__["age"] = 31  # Disable 'frozen'
```

The auto-generated `__setattr__` method of the dataclass raises an error.
This demonstrates that our `Person` instance is effectively read-only.

True immutability in Python can't be enforced; if you go out of your way to subvert immutability, you can.
The goal of frozen dataclasses is to protect against _accidental or careless_ mutations, not to provide an unbreakable security boundary.
In normal usage, you would treat the frozen instance as completely immutable.

Because instances of frozen dataclasses are immutable (by design and by behavior), they are also hashable by default, provided the class is comparable.
The dataclass decorator, by default, will generate an `__eq__` method for you (unless you opt out).
If you set `frozen=True` (and do not disable equality), it will also generate a `__hash__` method so that instances can be used in sets or as dictionary keys.
Specifically, if `eq=True` and `frozen=True`, Python will automatically add a `__hash__` method for the class based on its fields.
This makes sense: an object that is equal based on its field values and cannot change those values can safely be hashed.
Conversely, a mutable dataclass (eq=True, frozen=False) gets a `__hash__ = None` by default, marking it as unhashable (since its hash could change if fields changed).
This is an example of how immutability (or lack thereof) interacts with Python's runtime behavior.

```python
# frozen_data_classes.py
from dataclasses import dataclass
from book_utils import Catch


@dataclass(frozen=True)
class Messenger:
    name: str
    number: int
    depth: float = 0.0  # Default


print(messenger := Messenger("foo", 12, 3.14))
## Messenger(name='foo', number=12, depth=3.14)
# Frozen dataclass is immutable:
with Catch():
    messenger.name = "bar"  # type: ignore

# Automatically creates __hash__():
d = {messenger: "value"}
print(d[messenger])
## value
```

We can apply this approach to the `Stars` example:

```python
# stars.py
from dataclasses import dataclass

from book_utils import Catch


@dataclass(frozen=True)
class Stars:
    number: int

    def __post_init__(self) -> None:
        assert 1 <= self.number <= 10, f"{self}"


def f1(s: Stars) -> Stars:
    return Stars(s.number + 5)


def f2(s: Stars) -> Stars:
    return Stars(s.number * 5)


stars1 = Stars(4)
print(stars1)
## Stars(number=4)
print(f1(stars1))
## Stars(number=9)
with Catch():
    print(f2(f1(stars1)))
## Error: Stars(number=45)
with Catch():
    stars2 = Stars(11)
## Error: Stars(number=11)
with Catch():
    print(f1(Stars(11)))
## Error: Stars(number=11)
```

Subsequent functions operating on `Stars` no longer require redundant checks.
Modifying a `Stars` instance after creation raises an error, further safeguarding the data integrity:

```python
# modify_stars.py
from stars import Stars


def increase_stars(rating: Stars, increment: int) -> Stars:
    return Stars(rating.number + increment)
```

If this function tries to create an invalid rating, the data class validation immediately raises an error.
This greatly simplifies code maintenance and readability.

Additionally, immutable objects can safely serve as keys in dictionaries, allowing reliable data lookups and caching.

### How `Final` and `frozen` Work

Understanding how these features are implemented gives insight into their guarantees and limitations.

#### `Final`

This is entirely a compile-time (static) concept.
When you declare a variable or attribute with `Final`, the Python interpreter records that in the `__annotations__` of the module or class, but it does not prevent assignments at runtime.
The enforcement comes from type checkers.
Tools like mypy will scan your code and, if you try to reassign a `Final` variable, they will emit an error and refuse to consider the code type-safe.
As of Python 3.11, marking classes or methods with the `@final` decorator will set a `__final__ = True` attribute on the object, which is mostly for introspection or tooling--Python won't stop you from subclassing a `@final` class or overriding a
`@final` method at runtime, but doing so would likely cause your type checker to complain or your linter to warn you.
One key thing to remember is that `Final` is about the name binding, not the object's mutability: a `Final` list can still be changed in content, and `Final` doesn't make a dataclass frozen or anything of that sort.
It's a tool for design-by-contract: signaling intent and catching mistakes early.

#### Frozen dataclass

This provides _runtime_ enforcement by generating code.
When you use `frozen=True`, the dataclass decorator modifies your class definition.
It creates a custom `__setattr__` and `__delattr__` on the class that will raise `FrozenInstanceError` whenever someone tries to set or delete an attribute on an instance.
During object creation, the dataclass-generated `__init__` uses `object.__setattr__` internally for each field to bypass the restriction while initializing values.
Once construction is done, any further attribute setting goes through the overridden `__setattr__` and is blocked.
Because this is done in pure Python, it's not absolutely unbreakable (a savvy user could call `object.__setattr__` themselves, or manipulate low-level object state), but it is more than sufficient for ensuring standard use of the class remains immutable.
The design principle is that _"It is not possible to create truly immutable Python objects.
However, by using `frozen=True` you can emulate immutability."_ In day-to-day practice, a frozen dataclass is as good as immutable.

### Performance considerations

The convenience of frozen dataclasses comes with a minor cost.
As noted, setting attributes in `__init__` uses a slightly slower path (calling `object.__setattr__` for each field).
In the vast majority of cases this overhead is negligible (a few extra function calls during object creation).
It's rare to create so many objects that this becomes a bottleneck, but it's something to be aware of.
Accessing attributes and all other operations on a frozen dataclass are just as fast as on a regular class; it's only the initialization that's marginally slower.
For `Final` type hints, there is virtually no runtime cost at all, since it doesn't inject any checking--it's purely a compile-time concept.

### Combining `Final` and frozen dataclasses

You generally don't need `Final` annotations inside a frozen dataclass.
If a dataclass is frozen, all its fields are effectively final by design; you can't rebind them after construction.
For example, if you have `@dataclass(frozen=True) class C: x: int`, a type checker will treat `c.x` as a read-only property.

Note that in a dataclass, a bare `x: Final[int] = 3` is treated as an instance field default, whereas normally a `Final` at class level means a class variable.
You can use `Final` to indicate a class-level constant inside a dataclass.
However, it doesn't make sense to use `Final` on fields (instance attributes), because `frozen=True` already makes those fields immutable.

### Using `__post_init__` in Frozen Dataclasses

One challenge with frozen dataclasses is that you cannot assign to fields outside the initializer--but what if you need to compute one field based on others?
In a regular (mutable) dataclass, it's common to use a `__post_init__` method to perform additional initialization or validation after the auto-generated `__init__` has run.
With frozen dataclasses, however, you must be careful: by the time `__post_init__` executes, the `__setattr__` override that enforces immutability is already in place.
Any attempt to do `self.field = value` in `__post_init__` will trigger a `FrozenInstanceError` just like an outside assignment would (because internally it uses the same attribute-setting mechanism).

So how can we set up derived fields or perform adjustments in `__post_init__` for a frozen class?
The answer is to bypass the frozen `__setattr__` using the base class (`object`) method.
Python lets us call the underlying `object.__setattr__` method directly, which will ignore our dataclass's override and actually set the attribute.
This is exactly how dataclasses themselves initialize fields for frozen instances.
The dataclass documentation notes: _"There is a tiny performance penalty when using `frozen=True`: `__init__` cannot use assignment to initialize fields, and must use `object.__setattr__`."_.
The dataclass-generated `__init__` knows to do this for the fields that are set in the constructor.
We can apply the same technique in `__post_init__`.

**Correct approach:** Use `object.__setattr__(self, 'field_name', value)` in your `__post_init__` for any field that needs to be set on a frozen dataclass.
This calls the built-in `object` class's `__setattr__` implementation, which actually writes to the instance's `__dict__` (bypassing our dataclass's restriction).

Let's demonstrate this with an example.
Suppose we want to have a `Rectangle` dataclass that stores width and height, and we also want to store the area as a field for quick access.
We want the class to be frozen (immutable).
We can declare `area` as a field with `init=False` (so it's not passed to the constructor), and then compute it in `__post_init__` as follows:

```python
# example_8.py
from dataclasses import dataclass, field


@dataclass(frozen=True)
class Rectangle:
    width: float
    height: float
    area: float = field(
        init=False
    )  # area will be computed, not passed by caller

    def __post_init__(self):
        # Bypass immutability to set the derived field
        object.__setattr__(
            self, "area", self.width * self.height
        )
```

Here, `area` is intended to be a derived attribute (width _ height).
We marked it with `field(init=False)` so that dataclasses knows not to expect it as a parameter.
In `__post_init__`, we calculate the area and assign it using `object.__setattr__`.
This is the crucial step to avoid the `FrozenInstanceError`.
We could also use `super.setattr('area', self.width _ self.height)`--since the immediate base class is`object`, this has the same effect.
After `__post_init__` the `Rectangle`instance will a correct `area` but be frozen for further modifications.

Let's test this behavior:

```python
# example_9.py
from book_utils import Catch
from example_8 import Rectangle

r = Rectangle(3.0, 4.0)
print(r.area)  # Outputs: 12.0
## 12.0
# Try to modify attributes (should fail)
with Catch():
    # 'Rectangle' object attribute 'width' is read-only:
    # r.width = 5.0
    r.__dict__["width"] = 5.0  # Cheat to change
```

As expected, printing `r.area` gives 12.0, which means our `__post_init__` successfully set the value.
And attempting to assign `r.width` after creation raises an error, confirming the instance is immutable.
We have effectively created an immutable data object with some logic in its initialization.

A word of caution: using `object.__setattr__` is a bit of a loophole--it's meant to be used only during object initialization.
You wouldn't normally call `object.__setattr__` on a frozen instance outside of `__init__`/`__post_init__` because that would defeat the point of immutability.
(If someone is determined to bypass immutability, they can, but that's not normal usage.)
If you find yourself needing to change a frozen object after creation via such tricks, it may be a sign that the design should be reconsidered (maybe that piece of data shouldn't be frozen).
Generally, use this technique only to set up derived fields or cached values at construction time.

## NamedTuple

In many cases, a `NamedTuple` can be used in lieu of a frozen `dataclass`.
A `NamedTuple` combines `tuple` immutability with type annotations and named fields:

```python
# named_tuple.py
from typing import NamedTuple


class Coordinates(NamedTuple):
    latitude: float
    longitude: float


coords = Coordinates(51.5074, -0.1278)
print(coords)
## Coordinates(latitude=51.5074,
## longitude=-0.1278)
print(coords.latitude)
## 51.5074
# coords.latitude = 123.4567 # Runtime error
```

`NamedTuple` provides clarity, immutability, and easy unpacking, ideal for structured data.
Their simplicity makes them ideal for simple, lightweight, immutable record types.
For brevity and cleanliness, this book will use `NamedTuple`s instead of frozen `dataclass`es whenever possible.

Both `NamedTuple` and `dataclass` automate the creation of common methods
(such as constructors, `repr`, equality, and sometimes hash methods),
but they do so in different ways and with different design goals in mind.

Rather than generating an `__init__`,
a `NamedTuple` is a subclass of `tuple` and uses a generated `new` method to create instances.
Customization of construction logic is limited because you cannot define an init
(instead, you override new if needed, which is more cumbersome).
`NamedTuple` instances are immutable since they are `tuple` subclasses, so you cannot assign to their fields after creation.
A `NamedTuple` automatically generates a `repr` that prints the field names along with their values
(e.g., Point(x=1, y=2)) in a manner similar to a standard `tuple` representation.
An `__eq__` is generated based on the `tuple`’s content,
and `__hash__` is automatically defined (since `tuple`s are immutable).
`NamedTuple`s inherit `tuple` ordering (lexicographical order) by default.
`NamedTuple` is a subclass of `tuple`, which means all `tuple` operations (indexing, iteration, etc.) work as expected.
Since a `NamedTuple` is implemented as a `tuple` (with immutability and slots by default), it is memory efficient.

A `dataclass` generates an `__init__` that assigns the provided arguments to instance attributes.
By default, `dataclass` instances are mutable; however, you can set `frozen=True` to make them immutable.
This causes the generated `__init__` to assign to immutable fields.
The `repr` method is automatically generated to include the field names and their current values.
It is highly customizable via the `repr` parameter on fields.
By default, `dataclass` automatically generates an eq method that compares instances based on their fields.
If the `dataclass` is mutable (`frozen=False`, which is default), no hash is generated by default
(unless you specifically use `unsafe_hash=True`).
Mutable objects of any kind should generally not be hashed because the hash can change from one access to another.
If the `dataclass` is frozen (immutable), then a hash method is automatically provided.
You can add ordering methods (e.g., lt, le, etc.) by setting `order=True` when declaring the `dataclass`.
Otherwise, no ordering is generated.
Dataclasses provide a post_init method that runs immediately after the generated init method.
This is a convenient place for additional initialization or validation.
Dataclasses offer per-field customization (default values, default_factory, comparison options, etc.)
that allows fine-tuning of instances behavior.

Python's approach to immutability is a mix of convention, static assurance, and runtime enforcement:

- Use `Final` (and `@final`) to convey and enforce via static analysis that certain variables or attributes shouldn't change or be overridden.
- Use `@dataclass(frozen=True)` (or other techniques like `NamedTuple`s or custom `__setattr__` overrides) to actually prevent changes to object state at runtime.

With immutability, you get clarity, safety, and bug prevention--while still working within Python's flexible and dynamic nature.
Immutability in Python is ultimately a matter of developer intent supported by language features that make it easier to achieve and maintain.
With `Final` and frozen dataclasses, we now have the means to clearly communicate and enforce that intent, leading to more robust and maintainable codebases.

## References

1. [Mimicking Immutability in Python with Type Hints | Justin Austin](https://justincaustin.com/blog/mimicking-immutability-python-type-hints/)
2. [dataclasses--Data Classes--Python 3.13.3 documentation](https://docs.python.org/3/library/dataclasses.html)
3. [PEP 8--Style Guide for Python Code | peps.python.org](https://peps.python.org/pep-0008/)
4. [PEP 591](https://peps.python.org/pep-0591/)
5. [Type qualifiers--typing documentation](https://typing.python.org/en/latest/spec/qualifiers.html)
6. [typing--Support for type hints--Python 3.13.3 documentation](https://docs.python.org/3/library/typing.html)
7. [Customizing dataclass initialization--Python Morsels](https://www.pythonmorsels.com/customizing-dataclass-initialization/)
8. [python--How to set the value of dataclass field in post_init when frozen=True?--Stack Overflow](https://stackoverflow.com/questions/53756788/how-to-set-the-value-of-dataclass-field-in-post-init-when-frozen-true)
