# Immutability

## Why Immutability Matters

Immutability—the inability to change an object or variable after its creation—offers several key benefits in software design.
By making data immutable, we greatly simplify the mental model needed to understand program state.
In particular, immutability makes programs easier to reason about by eliminating the possibility of unexpected changes to data ([ Mimicking Immutability in Python with Type Hints | Justin Austin](https://justincaustin.com/blog/mimicking-immutability-python-type-hints/#:~:text=Immutability%20makes%20our%20programs%20easier,our%20worries%20is%20always%20welcome)).
This reduction in "the realm of possibility" for how data can evolve means fewer potential bugs and side effects in our code ([ Mimicking Immutability in Python with Type Hints | Justin Austin](https://justincaustin.com/blog/mimicking-immutability-python-type-hints/#:~:text=Immutability%20makes%20our%20programs%20easier,our%20worries%20is%20always%20welcome)).
An immutable variable gives us one less thing to worry about when tracing through a program's logic, because once it's set, it won't arbitrarily change under us.

Another major benefit is safety in concurrent contexts.
In multithreaded code, shared mutable state is a common source of issues like data races.
Immutability helps prevent these by ensuring that once a shared object is created, threads can read it without needing locks or fear of one thread modifying it out from under another ([ Mimicking Immutability in Python with Type Hints | Justin Austin](https://justincaustin.com/blog/mimicking-immutability-python-type-hints/#:~:text=While%20these%20benefits%20are%20particularly,identify%20and%20fix%20the%20bug)).
Even in single-threaded programs, immutability prevents accidental modifications that could lead to corrupted state.
With mutable state, a stray assignment or method call can silently alter data and introduce bugs that are hard to track down ([ Mimicking Immutability in Python with Type Hints | Justin Austin](https://justincaustin.com/blog/mimicking-immutability-python-type-hints/#:~:text=Unfortunately%2C%20another%20likely%20outcome%20is,corruption%20causes%20the%20state%20to)).
In contrast, if you attempt to modify an immutable piece of state, it will typically fail fast--either with a clear error at runtime or (ideally) an error caught by a static analysis tool before the code even runs ([ Mimicking Immutability in Python with Type Hints | Justin Austin](https://justincaustin.com/blog/mimicking-immutability-python-type-hints/#:~:text=,at%20runtime)) ([ Mimicking Immutability in Python with Type Hints | Justin Austin](https://justincaustin.com/blog/mimicking-immutability-python-type-hints/#:~:text=,like%20mypy)).
This fail-fast behavior makes bugs much easier to detect and fix.

Some concrete advantages of embracing immutability:

- **Easier Reasoning:** You can trust that values won't change unexpectedly, making functions behave more predictably ([ Mimicking Immutability in Python with Type Hints | Justin Austin](https://justincaustin.com/blog/mimicking-immutability-python-type-hints/#:~:text=Immutability%20makes%20our%20programs%20easier,our%20worries%20is%20always%20welcome)).
- **Thread-Safety:** Immutable objects can be freely shared between threads without synchronization, since no thread can alter them and cause race conditions ([ Mimicking Immutability in Python with Type Hints | Justin Austin](https://justincaustin.com/blog/mimicking-immutability-python-type-hints/#:~:text=While%20these%20benefits%20are%20particularly,identify%20and%20fix%20the%20bug)).
- **Avoiding Bugs:** Accidental mutations are caught early--either by a runtime exception or by a type checker--instead of corrupting state silently ([ Mimicking Immutability in Python with Type Hints | Justin Austin](https://justincaustin.com/blog/mimicking-immutability-python-type-hints/#:~:text=Unfortunately%2C%20another%20likely%20outcome%20is,corruption%20causes%20the%20state%20to)) ([ Mimicking Immutability in Python with Type Hints | Justin Austin](https://justincaustin.com/blog/mimicking-immutability-python-type-hints/#:~:text=,at%20runtime)).
- **Safe Sharing and Caching:** You can safely reuse or cache immutable objects (even as keys in dictionaries or members of sets) since their hash or contents won't change after creation.
  This aligns with Python's rule that objects used as dictionary keys must be immutable (e.g., using a tuple instead of a list for a key).

In summary, designing with immutability leads to code that is safer, more robust in concurrent environments, and easier to understand.
Python, as a dynamic language, doesn't enforce immutability by default, but it provides patterns and tools to achieve immutable-like behavior where beneficial.
Next, we'll explore how Python historically handles immutability through convention, and then dive into modern features for enforcing immutability via typing and dataclasses.

## Immutability by Convention in Python

Python does not have a built-in `const` declaration to make a variable truly immutable, nor does it allow truly unchangeable user-defined objects in all cases ([dataclasses--Data Classes--Python 3.13.3 documentation](https://docs.python.org/3/library/dataclasses.html#:~:text=It%20is%20not%20possible%20to,will%20raise%20a%20FrozenInstanceError%20when)).
Instead, Python developers have traditionally relied on conventions and certain immutable built-in types to signal that something should not be changed.

One common convention is the use of ALL_CAPS names for constants.
According to PEP 8 (Python's style guide),
"constants are usually defined on a module level and written in all capital letters with underscores separating words" ([PEP 8--Style Guide for Python Code | peps.python.org](https://peps.python.org/pep-0008/#:~:text=Constants%20are%20usually%20defined%20on,TOTAL)).
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

Python 3.8 introduced the `Final` qualifier in the `typing` module (as described in [PEP 591](https://peps.python.org/pep-0591/)).
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
If later in the code you attempt to do `PI = 3.14` (reassigning the constant), the type checker will emit an error, e.g. "Error: can't assign to final attribute" ([Type qualifiers--typing documentation](https://typing.python.org/en/latest/spec/qualifiers.html#:~:text=RATE%3A%20Final%20%3D%203000)).
The same goes for changing `MAX_CONNECTIONS`.
The Python interpreter itself will not stop you from doing this reassignment, but using `Final` elevates the constant from a mere convention to something that static analysis tools can verify.

According to the Python typing documentation, _"Final names cannot be reassigned in any scope.
Final names declared in class scopes cannot be overridden in subclasses."_ ([typing--Support for type hints--Python 3.13.3 documentation](https://docs.python.org/3/library/typing.html#:~:text=Special%20typing%20construct%20to%20indicate,final%20names%20to%20type%20checkers)).
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
If somewhere else we had `RATE = 2500`, a tool like mypy would report an error ("can't assign to final name ‘RATE'").
Similarly, `BaseConfig.TIMEOUT` is a constant class attribute; attempting to override it in `SubConfig` would be flagged ("can't override a final attribute") ([Type qualifiers--typing documentation](https://typing.python.org/en/latest/spec/qualifiers.html#:~:text=from%20typing%20import%20Final)).
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
For instance, if you declare `numbers: Final[list[int]] = [1, 2, 3]`, you are not supposed to reassign `numbers` to a new list, but you _can still mutate the list itself_ (e.g. `numbers.append(4)` will succeed) because the list object is still mutable.
The type checker might warn you if the type is `Final[Sequence[int]]` instead (since `Sequence` has no `append` method), but with `Final[list[int]]` the list methods are available.
In short, marking something `Final` guarantees that the _name_ won't be re-bound to a different object, but it does not magically make the object's contents immutable ([Type qualifiers--typing documentation](https://typing.python.org/en/latest/spec/qualifiers.html#:~:text=Note%20that%20declaring%20a%20name,to%20prevent%20mutating%20such%20values)) ([Type qualifiers--typing documentation](https://typing.python.org/en/latest/spec/qualifiers.html#:~:text=x%3A%20Final%20%3D%20,OK)).
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

In the above, `data1.append(4)` is allowed by the type system (though `data1` name can't be re-bound), whereas `data2.append(4)` would be rejected by a type checker because a `Sequence[int]` is assumed to be immutable (it lacks an `append` method) ([ Mimicking Immutability in Python with Type Hints | Justin Austin](https://justincaustin.com/blog/mimicking-immutability-python-type-hints/#:~:text=Here%27s%20an%20example%20of%20what,I%20mean)) ([ Mimicking Immutability in Python with Type Hints | Justin Austin](https://justincaustin.com/blog/mimicking-immutability-python-type-hints/#:~:text=,delitem)).
This demonstrates the difference between preventing reassignment of a variable and ensuring true immutability of the object.

Finally, note that Python also provides a `@final` decorator in `typing` which can be applied to classes or methods.
This is related to immutability in the sense of preventing changes in inheritance.
Decorating a class with `@final` means you intend it not to be subclassed, and a type checker will flag any subclass attempt as an error ([Type qualifiers--typing documentation](https://typing.python.org/en/latest/spec/qualifiers.html#:~:text=The%20,use%20of%20inheritance%20and%20overriding)) ([Type qualifiers--typing documentation](https://typing.python.org/en/latest/spec/qualifiers.html#:~:text=from%20typing%20import%20final)).
Similarly, marking a method with `@final` means it should not be overridden in any subclass ([Type qualifiers--typing documentation](https://typing.python.org/en/latest/spec/qualifiers.html#:~:text=A%20type%20checker%20should%20prohibit,methods%2C%20static%20methods%2C%20and%20properties)) ([Type qualifiers--typing documentation](https://typing.python.org/en/latest/spec/qualifiers.html#:~:text=class%20Base%3A%20%40final%20def%20foo,None%3A)).
This is more about preventing _behavioral modification_ via inheritance rather than value mutation.
It can be useful in design to ensure certain classes remain closed for extension (similar to `final` classes in Java).
At runtime, as of Python 3.11, the `@final` decorator sets a `__final__ = True` attribute on the class or function to help introspection ([typing--Support for type hints--Python 3.13.3 documentation](https://docs.python.org/3/library/typing.html#:~:text=Changed%20in%20version%203,object%20does%20not%20support%20setting)), but it doesn't enforce anything on its own.
Like the `Final` annotation, `@final` is a tool for communicating intent and catching errors early with the help of static analysis.

In summary, `Final` in Python typing is a lightweight way to get some of the benefits of immutability by preventing reassignments.
It formalizes the "ALL_CAPS means constant" convention into something a type checker can understand.
Combined with immutable types or interfaces, it can help you create APIs that promise not to mutate state.
However, for more complex state (especially when you want to bundle multiple values), Python's dataclasses offer another approach to enforce immutability at runtime.

## Immutability with Frozen Dataclasses

Python's `dataclass` decorator (introduced in Python 3.7) provides an easy way to create classes that bundle multiple attributes.
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
    p.x = 5  # noqa
## Error: cannot assign to field 'x'

p.__dict__["x"] = 5  # Bypassing 'frozen'
```

Running this code will result in a runtime error at the line `p.x = 5`.
Specifically, Python will raise a `dataclasses.FrozenInstanceError` with the message "cannot assign to field 'x'" ([ Mimicking Immutability in Python with Type Hints | Justin Austin](https://justincaustin.com/blog/mimicking-immutability-python-type-hints/#:~:text=state)).
The dataclass machinery has made the `Point` class's instances immutable by overriding the attribute-setting behavior: any attempt to set an attribute on a frozen instance triggers that exception.

Under the hood, when you use `@dataclass(frozen=True)`, Python generates an `__setattr__` method (and a `__delattr__` method) for your class that intercepts all attempts to set or delete attributes and immediately throws a `FrozenInstanceError` ([dataclasses--Data Classes--Python 3.13.3 documentation](https://docs.python.org/3/library/dataclasses.html#:~:text=It%20is%20not%20possible%20to,will%20raise%20a%20FrozenInstanceError%20when)).
This effectively locks down the instance after `__init__` finishes.
The exception `FrozenInstanceError` is a subclass of `AttributeError` ([dataclasses--Data Classes--Python 3.13.3 documentation](https://docs.python.org/3/library/dataclasses.html#:~:text=called%20on%20a%20dataclass%20which,is%20a%20subclass%20of%20AttributeError)), which is consistent with what Python normally throws if you try to assign to a read-only attribute.

Because of this, frozen dataclasses give you actual runtime enforcement of immutability.
Unlike the `Final` type hint, which is only checked by static analyzers, a frozen dataclass will actively prevent mutation in a running program.
This can be a powerful tool for ensuring certain objects remain constant.
It's especially handy for value objects (like points, coordinates, config objects, etc.) where you want to make sure their state doesn't change once created.

### Example: Frozen Dataclass in Action

Let's illustrate with a more detailed example and show what happens if we attempt mutation:

```python
# example_7.py
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
    person.age = 31  # noqa
## Error: cannot assign to field 'age'

person.__dict__["age"] = 31  # Disable 'frozen'
```

If you run this, you will get a traceback similar to:

```
Traceback (most recent call last):
  File "...", line 8, in <module>
    person.age = 31
  File "<string>", line 4, in __setattr__
dataclasses.FrozenInstanceError: cannot assign to field 'age'
```

The line `File "<string>", line 4, in __setattr__` is pointing to the auto-generated `__setattr__` method of the dataclass, which raised the error.
This demonstrates that our `Person` instance is effectively read-only.

It's worth noting that true immutability in Python can't be absolutely enforced in all cases--a determined developer could still bypass these restrictions (for instance, by using `object.__setattr__` to poke at the object, or by manipulating `person.__dict__`).
Python trusts the programmer; if you go out of your way to subvert immutability, you can.
The goal of frozen dataclasses is to protect against _accidental or careless_ mutations, not to provide an unbreakable security boundary ([dataclasses--Data Classes--Python 3.13.3 documentation](https://docs.python.org/3/library/dataclasses.html#:~:text=It%20is%20not%20possible%20to,will%20raise%20a%20FrozenInstanceError%20when)).
In normal usage, you would treat the frozen instance as completely immutable.

Because instances of frozen dataclasses are immutable (by design and by behavior), they are also hashable by default, provided the class is comparable.
The dataclass decorator, by default, will generate an `__eq__` method for you (unless you opt out).
If you set `frozen=True` (and do not disable equality), it will also generate a `__hash__` method so that instances can be used in sets or as dictionary keys.
Specifically, if `eq=True` and `frozen=True`, Python will automatically add a `__hash__` method for the class based on its fields ([dataclasses--Data Classes--Python 3.13.3 documentation](https://docs.python.org/3/library/dataclasses.html#:~:text=If%20eq%20and%20frozen%20are,based%20hashing)).
This makes sense: an object that is equal based on its field values and cannot change those values can safely be hashed.
Conversely, a mutable dataclass (eq=True, frozen=False) gets a `__hash__ = None` by default, marking it as unhashable (since its hash could change if fields changed) ([dataclasses--Data Classes--Python 3.13.3 documentation](https://docs.python.org/3/library/dataclasses.html#:~:text=If%20eq%20and%20frozen%20are,based%20hashing)).
This is an example of how immutability (or lack thereof) interacts with Python's runtime behavior.

### Using `__post_init__` in Frozen Dataclasses

One challenge with frozen dataclasses is that you cannot assign to fields outside the initializer--but what if you need to compute one field based on others? In a regular (mutable) dataclass, it's common to use a `__post_init__` method to perform additional initialization or validation after the auto-generated `__init__` has run.
With frozen dataclasses, however, you must be careful: by the time `__post_init__` executes, the `__setattr__` override that enforces immutability is already in place.
Any attempt to do `self.field = value` in `__post_init__` will trigger a `FrozenInstanceError` just like an outside assignment would ([Customizing dataclass initialization--Python Morsels](https://www.pythonmorsels.com/customizing-dataclass-initialization/#:~:text=This%20might%20seem%20like%20a,dataclass%2C%20we%27ll%20see%20an%20exception)) ([Customizing dataclass initialization--Python Morsels](https://www.pythonmorsels.com/customizing-dataclass-initialization/#:~:text=This%20exception%20is%20raised%20by,setattr__%20method%20on%20our%20dataclass)) (because internally it uses the same attribute-setting mechanism).

So how can we set up derived fields or perform adjustments in `__post_init__` for a frozen class? The answer is to bypass the frozen `__setattr__` using the base class (`object`) method.
Python lets us call the underlying `object.__setattr__` method directly, which will ignore our dataclass's override and actually set the attribute.
This is exactly how dataclasses themselves initialize fields for frozen instances.
The dataclass documentation notes: _"There is a tiny performance penalty when using `frozen=True`: `__init__()` cannot use assignment to initialize fields, and must use `object.__setattr__()`."_ ([dataclasses--Data Classes--Python 3.13.3 documentation](https://docs.python.org/3/library/dataclasses.html#:~:text=There%20is%20a%20tiny%20performance,object.__setattr)).
The dataclass-generated `__init__` knows to do this for the fields that are set in the constructor.
We can apply the same technique in `__post_init__`.

**Correct approach:** Use `object.__setattr__(self, 'field_name', value)` in your `__post_init__` for any field that needs to be set on a frozen dataclass.
This calls the built-in `object` class's `__setattr__` implementation, which actually writes to the instance's `__dict__` (bypassing our dataclass's restriction) ([python--How to set the value of dataclass field in post_init when frozen=True?--Stack Overflow](https://stackoverflow.com/questions/53756788/how-to-set-the-value-of-dataclass-field-in-post-init-when-frozen-true#:~:text=164)) ([Customizing dataclass initialization--Python Morsels](https://www.pythonmorsels.com/customizing-dataclass-initialization/#:~:text=def%20__post_init__%28self%29%3A%20super%28%29.__setattr__%28%27area%27%2C%20self.width%20,height)).

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
We could also use `super().setattr('area', self.width _ self.height)`--since the immediate base class is`object`, this has the same effect ([Customizing dataclass initialization--Python Morsels](https://www.pythonmorsels.com/customizing-dataclass-initialization/#:~:text=def%20__post_init__%28self%29%3A%20super%28%29.__setattr__%28%27area%27%2C%20self.width%20,height)).
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
You wouldn't normally call `object.__setattr__` on a frozen instance outside of `__init__`/`__post_init__` because that would defeat the point of immutability. (If someone is determined to bypass immutability, they can, but that's not normal usage.)
If you find yourself needing to change a frozen object after creation via such tricks, it may be a sign that the design should be reconsidered (maybe that piece of data shouldn't be frozen).
Generally, use this technique only to set up derived fields or cached values at construction time.

## Under the Hood: How `Final` and `frozen` Work

It's helpful to understand how these features are implemented, to fully appreciate their guarantees and limitations:

- **`Final`:** This is entirely a compile-time (static) concept.
  When you declare a variable or attribute with `Final`, the Python interpreter records that in the `__annotations__` of the module or class, but it does not prevent assignments at runtime.
  The enforcement comes from type checkers.
  Tools like mypy will scan your code and, if you try to reassign a `Final` variable, they will emit an error and refuse to consider the code type-safe ([Type qualifiers--typing documentation](https://typing.python.org/en/latest/spec/qualifiers.html#:~:text=RATE%3A%20Final%20%3D%203000)).
  As of Python 3.11, marking classes or methods with the `@final` decorator will set a `__final__ = True` attribute on the object ([typing--Support for type hints--Python 3.13.3 documentation](https://docs.python.org/3/library/typing.html#:~:text=Changed%20in%20version%203,object%20does%20not%20support%20setting)), which is mostly for introspection or tooling--Python won't stop you from subclassing a `@final` class or overriding a `@final` method at runtime, but doing so would likely cause your type checker to complain or your linter to warn you.
  One key thing to remember is that `Final` is about the name binding, not the object's mutability: a `Final` list can still be changed in content, and `Final` doesn't make a dataclass frozen or anything of that sort ([Type qualifiers--typing documentation](https://typing.python.org/en/latest/spec/qualifiers.html#:~:text=Note%20that%20declaring%20a%20name,to%20prevent%20mutating%20such%20values)).
  It's a tool for design-by-contract: signaling intent and catching mistakes early.

- **Frozen dataclass:** This provides _runtime_ enforcement by generating code.
  When you use `frozen=True`, the dataclass decorator modifies your class definition.
  It creates a custom `__setattr__` and `__delattr__` on the class that will raise `FrozenInstanceError` whenever someone tries to set or delete an attribute on an instance ([dataclasses--Data Classes--Python 3.13.3 documentation](https://docs.python.org/3/library/dataclasses.html#:~:text=It%20is%20not%20possible%20to,will%20raise%20a%20FrozenInstanceError%20when)).
  During object creation, the dataclass-generated `__init__` uses `object.__setattr__` internally for each field to bypass the restriction while initializing values ([dataclasses--Data Classes--Python 3.13.3 documentation](https://docs.python.org/3/library/dataclasses.html#:~:text=There%20is%20a%20tiny%20performance,object.__setattr)).
  Once construction is done, any further attribute setting goes through the overridden `__setattr__` and is blocked.
  Because this is done in pure Python, it's not absolutely unbreakable (a savvy user could call `object.__setattr__` themselves, or manipulate low-level object state), but it is more than sufficient for ensuring standard use of the class remains immutable.
  The design principle is that _"It is not possible to create truly immutable Python objects.
  However, by using `frozen=True` you can emulate immutability."_ ([dataclasses--Data Classes--Python 3.13.3 documentation](https://docs.python.org/3/library/dataclasses.html#:~:text=It%20is%20not%20possible%20to,will%20raise%20a%20FrozenInstanceError%20when)) In day-to-day practice, a frozen dataclass is as good as immutable.

- **Performance considerations:** The convenience of frozen dataclasses comes with a minor cost.
  As noted, setting attributes in `__init__` uses a slightly slower path (calling `object.__setattr__` for each field) ([dataclasses--Data Classes--Python 3.13.3 documentation](https://docs.python.org/3/library/dataclasses.html#:~:text=There%20is%20a%20tiny%20performance,object.__setattr)).
  In the vast majority of cases this overhead is negligible (a few extra function calls during object creation).
  It's rare to create so many objects that this becomes a bottleneck, but it's something to be aware of.
  Accessing attributes and all other operations on a frozen dataclass are just as fast as on a regular class; it's only the initialization that's marginally slower.
  For `Final` type hints, there is virtually no runtime cost at all, since it doesn't inject any checking--it's purely a compile-time concept.

- **Combining `Final` and frozen dataclasses:** You might wonder whether to use `Final` annotations inside a frozen dataclass.
  Generally, you do not need to.
  If a dataclass is frozen, all its fields are effectively final by design (you can't rebind them on the instance after construction).
  Type checkers are aware of frozen dataclasses in this regard.
  For example, if you have `@dataclass(frozen=True) class C: x: int`, mypy will treat `c.x` as a read-only property (assignments to it will be errors like "Property ‘x' is read-only").
  The typing spec even notes that in a dataclass, a bare `x: Final[int] = 3` is considered an instance field default ([Type qualifiers--typing documentation](https://typing.python.org/en/latest/spec/qualifiers.html#:~:text=Type%20checkers%20should%20infer%20a,or%20error%20on%20the%20redundancy)), whereas normally a `Final` at class level means a class variable.
  So you can use `Final` if you want to indicate a class-level constant inside a dataclass, but you wouldn't put `Final` on the fields meant to be instance attributes (the `frozen=True` already covers that usage).

To summarize, Python's approach to immutability is a mix of convention, static assurance, and runtime enforcement:

- Use `Final` (and `@final`) to convey and enforce via static analysis that certain variables or attributes shouldn't change or be overridden.
- Use `@dataclass(frozen=True)` (or other techniques like `NamedTuple`s or custom `__setattr__` overrides) to actually prevent changes to object state at runtime.

With immutability, you get clarity, safety, and bug prevention—while still working within Python's flexible and dynamic nature.
Immutability in Python is ultimately a matter of developer intent supported by language features that make it easier to achieve and maintain.
With `Final` and frozen dataclasses, we now have the means to clearly communicate and enforce that intent, leading to more robust and maintainable codebases.

## References

1. Justin Austin, _Mimicking Immutability in Python with Type Hints_ ([ Mimicking Immutability in Python with Type Hints | Justin Austin](https://justincaustin.com/blog/mimicking-immutability-python-type-hints/#:~:text=Immutability%20makes%20our%20programs%20easier,our%20worries%20is%20always%20welcome)) ([ Mimicking Immutability in Python with Type Hints | Justin Austin](https://justincaustin.com/blog/mimicking-immutability-python-type-hints/#:~:text=While%20these%20benefits%20are%20particularly,identify%20and%20fix%20the%20bug)) ([ Mimicking Immutability in Python with Type Hints | Justin Austin](https://justincaustin.com/blog/mimicking-immutability-python-type-hints/#:~:text=,at%20runtime)) ([ Mimicking Immutability in Python with Type Hints | Justin Austin](https://justincaustin.com/blog/mimicking-immutability-python-type-hints/#:~:text=,like%20mypy))
2. PEP 8 _Style Guide for Python Code_ (Constants Naming) ([PEP 8--Style Guide for Python Code | peps.python.org](https://peps.python.org/pep-0008/#:~:text=Constants%20are%20usually%20defined%20on,TOTAL))
3. Python Documentation, _typing.Final_ (Final names cannot be reassigned or overridden) ([typing--Support for type hints--Python 3.13.3 documentation](https://docs.python.org/3/library/typing.html#:~:text=Special%20typing%20construct%20to%20indicate,final%20names%20to%20type%20checkers)) ([Type qualifiers--typing documentation](https://typing.python.org/en/latest/spec/qualifiers.html#:~:text=RATE%3A%20Final%20%3D%203000)) ([Type qualifiers--typing documentation](https://typing.python.org/en/latest/spec/qualifiers.html#:~:text=from%20typing%20import%20Final)) ([Type qualifiers--typing documentation](https://typing.python.org/en/latest/spec/qualifiers.html#:~:text=Note%20that%20declaring%20a%20name,to%20prevent%20mutating%20such%20values))
4. Python Documentation, _dataclasses (frozen=True)_ ([dataclasses--Data Classes--Python 3.13.3 documentation](https://docs.python.org/3/library/dataclasses.html#:~:text=It%20is%20not%20possible%20to,will%20raise%20a%20FrozenInstanceError%20when)) ([dataclasses--Data Classes--Python 3.13.3 documentation](https://docs.python.org/3/library/dataclasses.html#:~:text=If%20eq%20and%20frozen%20are,based%20hashing)) (Frozen dataclass behavior and hashability)
5. Stack Overflow, _Setting value in `__post_init__` for frozen dataclass_ ([python--How to set the value of dataclass field in post_init when frozen=True?--Stack Overflow](https://stackoverflow.com/questions/53756788/how-to-set-the-value-of-dataclass-field-in-post-init-when-frozen-true#:~:text=164)) (Using `object.__setattr__` to set attributes in `__post_init__`)
6. Python Morsels, _Customizing dataclass initialization_ ([Customizing dataclass initialization--Python Morsels](https://www.pythonmorsels.com/customizing-dataclass-initialization/#:~:text=def%20__post_init__%28self%29%3A%20super%28%29.__setattr__%28%27area%27%2C%20self.width%20,height)) (Bypassing `__setattr__` in a frozen dataclass using `super().__setattr__`).
