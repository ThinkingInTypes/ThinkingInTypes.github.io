# Custom Types: Data Classes

Built-in types are extremely useful (I'm including all the types in the standard Python library),
but the real programming power comes by creating user-defined types, which we shall call _custom types_.
The remainder of this book will primarily focus on various ways to create and use custom types.

One of the biggest benefits of custom types is that they allow you to create types that reflect entities in your problem domain.
The book _Domain-Driven Design_ by Eric Evans explores problem-domain modeling to discover the types in your system.

## Ensuring Correctness

Imagine building a customer feedback system using a rating from one to ten stars.
Traditionally, Python programmers use an `int` to represent `stars`, checking arguments to ensure validity:

```python
# int_stars.py
# Using 1-10 stars for customer feedback.
from book_utils import Catch


def f1(stars: int) -> int:
    # Must check argument...
    assert 1 <= stars <= 10, f"f1: {stars}"
    return stars + 5


def f2(stars: int) -> int:
    # ...each place it is used.
    assert 1 <= stars <= 10, f"f2: {stars}"
    return stars * 5


stars1 = 6
print(stars1)
## 6
print(f1(stars1))
## 11
print(f2(stars1))
## 30
stars2 = 11
with Catch():
    print(f1(stars2))
## Error: f1: 11
stars3 = 99
with Catch():
    print(f2(stars3))
## Error: f2: 99
```

Each function that takes a `stars` must validate that argument, leading to duplicated logic, scattered validation, and potential mistakes.

## Traditional Object-Oriented Encapsulation

Object-oriented programming (OOP) suggests encapsulating validation within the class.
Python typically uses a private attribute (indicated with a single leading underscore) for encapsulation:

```python
# stars_class.py
from typing import Optional
from book_utils import Catch


class Stars:
    def __init__(self, n_stars: int):
        self._number = n_stars  # Private by convention
        self.validate()

    def validate(self, s: Optional[int] = None):
        if s:
            assert 1 <= s <= 10, f"{self}: {s}"
        else:
            assert 1 <= self._number <= 10, f"{self}"

    # Prevent external modification:
    @property
    def number(self):
        return self._number

    def __str__(self) -> str:
        return f"Stars({self._number})"

    # Every member function must validate the private variable:
    def f1(self, n_stars: int) -> int:
        self.validate(n_stars)  # Precondition
        self._number = n_stars + 5
        self.validate()  # Postcondition
        return self._number

    def f2(self, n_stars: int) -> int:
        self.validate(n_stars)  # Precondition
        self._number = n_stars * 5
        self.validate()  # Postcondition
        return self._number


stars1 = Stars(4)
print(stars1)
## Stars(4)
print(stars1.f1(3))
## 8
with Catch():
    print(stars1.f2(stars1.f1(3)))
## Error: Stars(40)
with Catch():
    stars2 = Stars(11)
## Error: Stars(11)
stars3 = Stars(5)
print(stars3.f1(4))
## 9
with Catch():
    print(stars3.f2(22))
## Error: Stars(9): 22
# @property without setter prevents mutation:
with Catch():
    stars1.number = 99  # type: ignore
```

This approach centralizes validation yet remains cumbersome.
Each method interacting with the attribute still requires pre-and post-condition checks,
cluttering the code and potentially introducing errors if a developer neglects these checks.

## Type Aliases & `NewType`

Suppose you have a `dict` with nested structures or a `tuple` with many elements.
Writing out these types every time is unwieldy.
Type aliases assign a name to a type to make annotations cleaner and more maintainable.

A type alias is a name assignment at the top level of your code.
We normally name type aliases with _CamelCase_ to indicate they are types:

```python
# simple_type_aliasing.py
from typing import get_type_hints, NewType

type Number = int | float | str
# Runtime-safe distinct type for measurement lists
Measurements = NewType("Measurements", list[Number])


def process(data: Measurements) -> None:
    print(get_type_hints(process))
    for n in data:
        print(f"{n = }, {type(n) = }")


process(Measurements([11, 3.14, "1.618"]))
## {'data': __main__.Measurements, 'return': <class 'NoneType'>}
## n = 11, type(n) = <class 'int'>
## n = 3.14, type(n) = <class 'float'>
## n = '1.618', type(n) = <class 'str'>
```

Using `Number` and `Measurements` is functionally identical to writing the annotation as `int | float` or `list[Number]`.
The aliases:

- Gives a meaningful name to the type, indicating what the `list` of `Number`s represents--in this case,
  a collection called `Measurements`.
- Avoids repeating a complex type annotation in multiple places.
- Improves readability by abstracting away the details of the type structure.
- If the definition of `Measurements` changes (if we use a different type to represent `Number`),
  we can update the alias in one place.

You can see from the output that type aliases do not create new types at runtime;
they are purely for the benefit of the type system and the developer.

### `NewType`

A type alias is a notational convenience, but it doesn't create a new type recognized by the type checker.
`NewType` creates a new, distinct type, preventing accidental misuse of similar underlying types.
You'll often want to use `NewType` instead of type aliasing:

```python
# new_type.py
from typing import NewType, get_type_hints

type Number = int | float | str  # Static union alias

# Runtime-safe distinct type:
Measurements = NewType("Measurements", list[Number])


def process(data: Measurements) -> None:
    print(get_type_hints(process))
    for n in data:
        print(f"{n = }, {type(n) = }")


process(Measurements([11, 3.14, "1.618"]))
## {'data': __main__.Measurements, 'return': <class 'NoneType'>}
## n = 11, type(n) = <class 'int'>
## n = 3.14, type(n) = <class 'float'>
## n = '1.618', type(n) = <class 'str'>
```

`get_type_hints` produces information about the function.

`NewType` is intended to create a distinct type based on another type.
Its primary goal is to help prevent the mixing of semantically different values that are represented by the same underlying type;
for example, differentiating `UserID` from `ProductID`, even though both are `int`s:

```python
# new_type_users.py
from typing import NewType

UserID = NewType("UserID", int)
ProductID = NewType("ProductID", int)
Users = NewType("Users", list[UserID])

users = Users([UserID(2), UserID(5), UserID(42)])


def increment(uid: UserID) -> UserID:
    # Transparently access underlying value:
    return UserID(uid + 1)


# increment(42)  # Type check error

# Access underlying list operation:
print(increment(users[-1]))
## 43


def increment_users(users: Users) -> Users:
    return Users([increment(uid) for uid in users])


print(increment_users(users))
## [3, 6, 43]
```

Notice that `Users` uses `UserID` in its definition.
The type checker requires `UserID` for `increment` and `Users` for `increment_users`,
even though we can transparently access the underlying elements of each type (`int` and `list[UserID]`).

### Creating a `NewType` from a `NewType`

You cannot subclass a `NewType`:

```python
# newtype_subtype.py
from typing import NewType

Stars = NewType("Stars", int)

# Fails type check and at runtime:
# class GasGiants(Stars): pass
```

However, it is possible to create a `NewType` _based_ on a `NewType`:

```python
# newtype_based_type.py
from typing import NewType

Stars = NewType("Stars", int)

GasGiants = NewType("GasGiants", Stars)
```

Typechecking for `GasGiants` works as expected.

### `NewType` Stars

`NewType` will provide some benefit to the `Stars` problem by going from an `int` to a specific type:

```python
# newtype_stars.py
from typing import NewType

Stars = NewType("Stars", int)


def f1(stars: Stars) -> Stars:
    assert 1 <= stars <= 10, f"f1: {stars}"
    return Stars(stars + 5)


def f2(stars: Stars) -> Stars:
    assert 1 <= stars <= 10, f"f2: {stars}"
    return Stars(stars * 5)
```

Now `f1` and `f2` will produce an error if you try to pass them an `int`; they only accept `Stars`.
Note that `NewType` generates a constructor for `Stars`, which we need to return `Stars` objects.
The validation code remains the same, because `Stars` _is_ an `int`.
However, we still need the validation code.
To improve the design, we require a more powerful technique.

## Data Classes

_Data classes_ provide a structured, concise way to define data-holding types.
Many languages have similar constructs under different names: Scala has `case class`, Kotlin has `data class`, Java has `record`, Rust has `struct`, etc.
Data classes streamline the process of creating types by generating essential methods automatically.

```python
# messenger.py
from dataclasses import dataclass, replace


@dataclass
class Messenger:
    name: str
    number: int
    depth: float = 0.0  # Default argument


x = Messenger(name="x", number=9, depth=2.0)
m = Messenger("foo", 12, 3.14)
print(m)
## Messenger(name='foo', number=12, depth=3.14)
print(m.name, m.number, m.depth)
## foo 12 3.14
mm = Messenger("xx", 1)  # Uses default argument
print(mm == Messenger("xx", 1))  # Generated __eq__()
## True
print(mm == Messenger("xx", 2))
## False

# Make a copy with a different depth:
mc = replace(m, depth=9.9)
print(m, mc)
## Messenger(name='foo', number=12, depth=3.14)
## Messenger(name='foo', number=12, depth=9.9)

# Mutable:
m.name = "bar"
print(m)
## Messenger(name='bar', number=12, depth=3.14)
# d = {m: "value"}
# TypeError: unhashable type: 'Messenger'
```

`Messenger` is defined with three fields: `name` and `number`, which are required, and `depth`, which has a default value of `0.0`.
The `@dataclass` decorator automatically generates an `__init__`, `__repr__`, `__eq__`, among others.
We see several ways to instantiate `Messenger` objects, demonstrating that the default for `depth` is used when not provided.
It also shows that two instances with the same field values are equal, and how to create a modified copy of an instance using `replace()`.
It highlights mutability: `Messenger` instances can be modified unless marked as `frozen=True` (a feature covered in [C06_Immutability]).
Finally, it demonstrates that `Messenger` instances cannot be used as dictionary keys by default because they are not hashable,
a feature that can be enabled via `@dataclass(unsafe_hash=True)` or by making the class immutable with `frozen=True`.

### Generated Methods

Using the standard library `inspect` module, we can display the type signatures of the methods in a class:

```python
# class_methods.py
import inspect


def show_methods(cls: type) -> None:
    print(f"class {cls.__name__}:")
    for name, member in cls.__dict__.items():
        if callable(member):
            sig = inspect.signature(member)
            print(f"  {name}{sig}")
```

The function iterates through the class dictionary and uses `inspect.signature()` to display the type signatures of callable members.
Here is `show_methods` applied to an ordinary class:

```python
# point_methods.py
from class_methods import show_methods


class Klass:
    def __init__(self, val: str):
        self.val = val


show_methods(Klass)
## class Klass:
##   __init__(self, val: str)
```

Here are different configurations of `@dataclass`:

```python
# point_dataclasses.py
from dataclasses import dataclass


@dataclass
class Point:
    x: int = 1
    y: int = 2


@dataclass(order=True)
class OrderedPoint:
    x: int = 1
    y: int = 2


@dataclass(frozen=True)
class FrozenPoint:
    x: int = 1
    y: int = 2


@dataclass(order=True, frozen=True)
class OrderedFrozenPoint:
    x: int = 1
    y: int = 2
```

Now we can see the methods generated by these variations:

```python
# dataclass_generated_methods.py
from point_dataclasses import (
    Point,
    OrderedPoint,
    FrozenPoint,
    OrderedFrozenPoint,
)
from class_methods import show_methods

show_methods(Point)
## class Point:
##   __annotate_func__(format, /)
##   __replace__(self, /, **changes)
##   __init__(self, x: int = 1, y: int = 2) -> None
##   __repr__(self)
##   __eq__(self, other)
show_methods(OrderedPoint)
## class OrderedPoint:
##   __annotate_func__(format, /)
##   __replace__(self, /, **changes)
##   __init__(self, x: int = 1, y: int = 2) -> None
##   __repr__(self)
##   __eq__(self, other)
##   __lt__(self, other)
##   __le__(self, other)
##   __gt__(self, other)
##   __ge__(self, other)
show_methods(FrozenPoint)
## class FrozenPoint:
##   __annotate_func__(format, /)
##   __replace__(self, /, **changes)
##   __hash__(self)
##   __init__(self, x: int = 1, y: int = 2) -> None
##   __repr__(self)
##   __eq__(self, other)
##   __setattr__(self, name, value)
##   __delattr__(self, name)
show_methods(OrderedFrozenPoint)
## class OrderedFrozenPoint:
##   __annotate_func__(format, /)
##   __replace__(self, /, **changes)
##   __hash__(self)
##   __init__(self, x: int = 1, y: int = 2) -> None
##   __repr__(self)
##   __eq__(self, other)
##   __lt__(self, other)
##   __le__(self, other)
##   __gt__(self, other)
##   __ge__(self, other)
##   __setattr__(self, name, value)
##   __delattr__(self, name)
```

The different forms of data class all have a set of methods in common:

- `__init__` constructs a new instance by initializing the instance attributes according to the defined class attributes.
- `__replace__` is used by the `replace()` function, shown earlier, to create a new instance from an existing instance, changing one or more attributes.
- `__repr__` creates a readable representation produced by `repr()` or any operation that needs a `str`.
- `__eq__` defines equivalence between two instances of the data class.
- `__annotate_func__` is a utility function used internally by the dataclass.

Adding `order=True` to the dataclass adds the full suite of comparison methods: `__lt__`, `__le__`, `__gt__`, and `__ge__`.

Adding `frozen=True` produces immutability by preventing instance mutation; this also enables hashability.
The definitions of `__setattr__` and `__delattr__` prevent modification at runtime.

Adding `order=True` together with `frozen=True` produces the sum of all generated methods.

### Sorting and Hashing

// Describe

```python
# sortable_points.py
from point_dataclasses import OrderedPoint

ordered_points: list[OrderedPoint] = [
    OrderedPoint(3, 5),
    OrderedPoint(3, 4),
    OrderedPoint(1, 9),
    OrderedPoint(1, 2),
]
print(sorted(ordered_points))
## [OrderedPoint(x=1, y=2), OrderedPoint(x=1, y=9),
## OrderedPoint(x=3, y=4), OrderedPoint(x=3, y=5)]
```

```python
# hashable_points.py
from point_dataclasses import FrozenPoint

point_set: set[FrozenPoint] = {
    FrozenPoint(1, 2),
    FrozenPoint(3, 4),
}
print(FrozenPoint(1, 2) in point_set)
## True
point_dict: dict[FrozenPoint, str] = {
    FrozenPoint(1, 2): "first",
    FrozenPoint(3, 4): "second",
}
print(point_dict[FrozenPoint(3, 4)])
## second
```

### Default Factories

A default factory is a function that creates a default value for a field.
Here, `next_ten` is a custom default factory; it's a function that produces a value:

```python
# default_factory.py
from dataclasses import dataclass, field
from typing import List, Dict

_n = 0


def next_ten() -> int:
    global _n
    _n += 10
    return _n


@dataclass
class UserProfile:
    username: str
    # Built-in factory: each instance gets a new empty list
    strlist: List[str] = field(default_factory=list)
    # Custom default factories:
    n1: int = field(default_factory=next_ten)
    data: Dict[str, str] = field(
        default_factory=lambda: {"A": "B"}
    )
    n2: int = field(default_factory=next_ten)


print(user1 := UserProfile("Alice"))
## UserProfile(username='Alice', strlist=[], n1=10, data={'A': 'B'},
## n2=20)
print(user2 := UserProfile("Bob"))
## UserProfile(username='Bob', strlist=[], n1=30, data={'A': 'B'},
## n2=40)

# Modify mutable fields to verify they don't share state
user1.strlist.append("dark_mode")
user2.strlist.append("notifications")
user2.data["C"] = "D"
print(f"{user1 = }")
## user1 = UserProfile(username='Alice', strlist=['dark_mode'],
## n1=10, data={'A': 'B'}, n2=20)
print(f"{user2 = }")
## user2 = UserProfile(username='Bob', strlist=['notifications'],
## n1=30, data={'A': 'B', 'C': 'D'}, n2=40)
```

// Describe

### Post-Initialization

In a typical data class, validation logic resides in the `__post_init__` method.
This is executed automatically after initialization.
With `__post_init__`, you can guarantee that only valid instances of your type can be created.
Here, `__post_init__` initializes the `area` attribute:

```python
# post_init.py
from dataclasses import dataclass
from math import pi


@dataclass
class Circle:
    radius: float
    area: float = 0.0

    def __post_init__(self):
        self.area = pi * self.radius**2


print(Circle(radius=5))
## Circle(radius=5, area=78.53981633974483)
```

Here's a slightly more complex example:

```python
# team_post_init.py
from dataclasses import dataclass, field
from typing import List


@dataclass
class Team:
    leader: str
    members: List[str] = field(default_factory=list)

    def __post_init__(self):
        self.leader = self.leader.capitalize()
        if self.leader not in self.members:
            self.members.insert(0, self.leader)


print(Team("alice", ["bob", "carol", "ted"]))
## Team(leader='Alice', members=['Alice', 'bob', 'carol', 'ted'])
```

We can use `__post_init__` to solve the `Stars` validation problem:

```python
# stars_dataclass.py
from dataclasses import dataclass

from book_utils import Catch


@dataclass
class Stars:
    number: int

    def __post_init__(self) -> None:
        assert 1 <= self.number <= 10, f"{self}"


def f1(stars: Stars) -> Stars:
    return Stars(stars.number + 5)


def f2(stars: Stars) -> Stars:
    return Stars(stars.number * 5)


stars1 = Stars(6)
print(stars1)
## Stars(number=6)
with Catch():
    print(f1(stars1))
## Error: Stars(number=11)
with Catch():
    print(f2(stars1))
## Error: Stars(number=30)
with Catch():
    print(f1(Stars(22)))
## Error: Stars(number=22)
with Catch():
    print(f2(Stars(99)))
## Error: Stars(number=99)
```

Now `f1` and `f2` no longer need to do any validation testing on `Stars`, because it is impossible to create an invalid `Stars` object.
Note that you can still take a `Stars` and modify it so it becomes invalid; we shall address this in the next chapter.

### Initializers

Normally you'll define a `__post_init__` to perform _validation_.
Sometimes, you'll need an `__init__` to customize the way fields are initialized.

A custom `__init__` makes sense primarily for different initialization logic than the field-based constructor allows.
You need a completely alternative interface, such as parsing inputs from a different format
(e.g., strings, dictionaries, files) and then assigning to fields.
For example, consider parsing two pieces of `float` data from a single `str` argument:

```python
# point.py
from dataclasses import dataclass


@dataclass
class Point:
    x: float
    y: float

    def __init__(self, coord: str):
        x_str, y_str = coord.split(",")
        self.x = float(x_str.strip())
        self.y = float(y_str.strip())
```

Notice the extra space in the string argument to `Point`:

```python
# point_demo.py
from point import Point

print(Point(" 10.5 , 20.3 "))
## Point(x=10.5, y=20.3)
```

Here, the custom `__init__` provides a simpler API.
You retain data class features like `__repr__`, `__eq__`, and automatic field handling.

Data classes auto-generate an `__init__` unless you explicitly define one.
If you provide a custom `__init__`, the automatic one is replaced.
You can still use `__post_init__`, but must call it explicitly from your custom `__init__`.

Prefer `__post_init__` for basic validation, transformation, or default adjustments after standard field initialization.
Use a custom `__init__` if you require fundamentally different or more complex input logic that's incompatible with the autogenerated initializer.

### Composing Data Classes

Composition creates complex data types from simpler ones.
Consider a `Person` object composed of `FullName`, `BirthDate`, and `Email` data classes:

```python
# dataclass_composition.py
from dataclasses import dataclass


@dataclass
class FullName:
    name: str

    def __post_init__(self) -> None:
        print(f"FullName checking {self.name}")
        assert len(self.name.split()) > 1, (
            f"'{self.name}' needs first and last names"
        )


@dataclass
class BirthDate:
    dob: str

    def __post_init__(self) -> None:
        print(f"BirthDate checking {self.dob}")


@dataclass
class EmailAddress:
    address: str

    def __post_init__(self) -> None:
        print(f"EmailAddress checking {self.address}")


@dataclass
class Person:
    name: FullName
    date_of_birth: BirthDate
    email: EmailAddress


person = Person(
    FullName("Bruce Eckel"),
    BirthDate("7/8/1957"),
    EmailAddress("mindviewinc@gmail.com"),
)
## FullName checking Bruce Eckel
## BirthDate checking 7/8/1957
## EmailAddress checking mindviewinc@gmail.com
print(person)
## Person(name=FullName(name='Bruce Eckel'),
## date_of_birth=BirthDate(dob='7/8/1957'),
## email=EmailAddress(address='mindviewinc@gmail.com'))
```

This hierarchical validation structure ensures correctness and clarity at every composition level.
Invalid data never propagates, vastly simplifying subsequent interactions.

### `InitVar`

`dataclasses.InitVar` allows you to define fields that are only used during initialization but are not stored as attributes of the data class object.
`InitVar` fields are passed as parameters to the `__init__` method and can be used within the `__post_init__` method for additional initialization logic.
They are not considered regular fields of the data class and are not included in the output of functions like `fields()`.

```python
# dataclass_initvar.py
from dataclasses import dataclass, InitVar


@dataclass
class Book:
    title: str
    author: str
    condition: InitVar[str]
    shelf_id: int | None = None

    def __post_init__(self, condition):
        if condition == "Unacceptable":
            self.shelf_id = None


b = Book("Emma", "Austen", "Good", 11)
print(b.__dict__)
## {'title': 'Emma', 'author': 'Austen', 'shelf_id': 11}
```

In this example, `condition` is an `InitVar`.
It is used to conditionally set the `shelf_id` in `__post_init__`,
but we can see from displaying the `__dict__` that it is not stored as an attribute of the `Book` instance.

### Dataclass as Dictionary

The `dataclasses.asdict` function can seem confusing at first:

```python
# dataclass_as_dict.py
from dataclasses import asdict
from point_dataclasses import Point

p = Point(7, 9)
print(asdict(p))
## {'x': 7, 'y': 9}
print(p.__dict__)
## {'x': 7, 'y': 9}
# Unpacking:
x, y = tuple(asdict(p).values())
print(x, y)
## 7 9
# Or:
x1, y1 = tuple(p.__dict__.values())
print(x1, y1)
## 7 9
```

The result of `asdict(p)` and `p.__dict__` appear to be the same.
To see the effect of `asdict()` we need a more complicated example:

```python
# asdict_behavior.py
from dataclasses import dataclass, asdict

from point_dataclasses import Point


@dataclass
class Line:
    p1: Point
    p2: Point


@dataclass
class Shape:
    lines: list[Line]


@dataclass
class Image:
    shapes: list[Shape]


shape1 = Shape(
    [
        Line(Point(0, 0), Point(10, 4)),
        Line(Point(10, 4), Point(16, 8)),
    ]
)

image = Image([shape1, shape1])
print(image.__dict__)
## {'shapes': [Shape(lines=[Line(p1=Point(x=0, y=0), p2=Point(x=10,
## y=4)), Line(p1=Point(x=10, y=4), p2=Point(x=16, y=8))]),
## Shape(lines=[Line(p1=Point(x=0, y=0), p2=Point(x=10, y=4)),
## Line(p1=Point(x=10, y=4), p2=Point(x=16, y=8))])]}
print(asdict(image))
## {'shapes': [{'lines': [{'p1': {'x': 0, 'y': 0}, 'p2': {'x': 10,
## 'y': 4}}, {'p1': {'x': 10, 'y': 4}, 'p2': {'x': 16, 'y': 8}}]},
## {'lines': [{'p1': {'x': 0, 'y': 0}, 'p2': {'x': 10, 'y': 4}},
## {'p1': {'x': 10, 'y': 4}, 'p2': {'x': 16, 'y': 8}}]}]}
```

Notice how easily we produce a sophisticated type like `Image`.
Now you can see the difference: `__dict__` recursively produces the `repr()`s of all the components,
while `asdict()` creates `dict`s and `list`s as you would need for a JSON representation.
In addition, `__dict__` shows you the dictionary for the object, while `asdict()` creates a new object.

## Class Attributes

Sometimes people get confused and mistakenly believe that a class attribute defines an instance attribute:

```python
# a_with_x.py
class A:
    # Does this create instance attributes?
    x: int = 1
    y: int = 2


a = A()
print(f"{a.x = }, {a.y = }")
## a.x = 1, a.y = 2
```

Creating `A()` _appears_ to automatically produce instance attributes `x` and `y`.
This happens because of the lookup rules: when `a.x` or `a.y` can't find an instance attribute, it looks for a class attribute with the same name.

The confusion is understandable because in languages like C++ and Java, similar class definitions _do_ produce instance attributes.

The key is to understand the difference between class attributes and instance attributes.
Both are stored in dictionaries; `show_dicts` compares the attributes in both dictionaries:

```python
# class_and_instance.py


def show_dicts(obj: object, obj_name: str):
    cls = obj.__class__
    cls_name = cls.__name__

    cls_dict = {
        k: v
        for k, v in cls.__dict__.items()
        if not k.startswith("__")
    }
    obj_dict = obj.__dict__

    print(f"{cls_name}.__dict__ (class attributes):")
    for attr in cls_dict.keys():
        value = cls_dict[attr]
        note = ""
        if attr in obj_dict and obj_dict[attr] != value:
            note = "  # Hidden by instance attribute"
        print(f"  {attr}: {value}{note}")

    print(f"{obj_name}.__dict__ (instance attributes):")
    for attr in cls_dict.keys():
        if attr in obj_dict:
            print(f"  {attr}: {obj_dict[attr]}")
        else:
            print(f"  {attr}: <not present>")

    for attr in cls_dict.keys():
        print(f"{obj_name}.{attr} is {getattr(obj, attr)}")
```

Python stores class attributes in the class `__dict__` and instance attributes in the instance `__dict__`.
When you access `a.x`, Python first looks in `a.__dict__`.
If the name isn't found there, it continues the search in `A.__dict__`.
This fallback behavior makes class attributes appear to be instance attributes, but they aren't.

`show_dicts` clarifies this by listing the class attributes, instance attributes,
and the result of accessing the attribute (`getattr(obj, attr)`), which follows Python's lookup rules.

Here's an example proving that class attributes do not create instance attributes:

```python
# class_attribute_proof.py
from class_and_instance import show_dicts


class A:
    x: int = 1
    y: int = 2


a = A()
show_dicts(a, "a")
## A.__dict__ (class attributes):
##   x: 1
##   y: 2
## a.__dict__ (instance attributes):
##   x: <not present>
##   y: <not present>
## a.x is 1
## a.y is 2
a.x = 99
show_dicts(a, "a")
## A.__dict__ (class attributes):
##   x: 1  # Hidden by instance attribute
##   y: 2
## a.__dict__ (instance attributes):
##   x: 99
##   y: <not present>
## a.x is 99
## a.y is 2
a.y = 111
show_dicts(a, "a")
## A.__dict__ (class attributes):
##   x: 1  # Hidden by instance attribute
##   y: 2  # Hidden by instance attribute
## a.__dict__ (instance attributes):
##   x: 99
##   y: 111
## a.x is 99
## a.y is 111
```

After creating `a`, we see class attribute of `x` and `y` with values `1` and `2`, respectively.
However, the instance dictionary is empty--there are no instance attributes.
Thus, when we access `a.x` and `b.x`, Python doesn't find those instance attributes and continues to search, displaying the class attributes instead.

The act of assigning `a.x = 99` and `a.y = 111` _creates_ new instance attributes `x` and `y`.
Note that the class attributes `A.x` and `A.y` remain unchanged.

Let's perform the same experiment with a data class:

```python
# dataclass_attribute.py
from dataclasses import dataclass
from class_and_instance import show_dicts


@dataclass
class D:
    x: int = 1
    y: int = 2


d = D()
show_dicts(d, "d")
## D.__dict__ (class attributes):
##   x: 1
##   y: 2
## d.__dict__ (instance attributes):
##   x: 1
##   y: 2
## d.x is 1
## d.y is 2
d.x = 99
show_dicts(d, "d")
## D.__dict__ (class attributes):
##   x: 1  # Hidden by instance attribute
##   y: 2
## d.__dict__ (instance attributes):
##   x: 99
##   y: 2
## d.x is 99
## d.y is 2
d.y = 111
show_dicts(d, "d")
## D.__dict__ (class attributes):
##   x: 1  # Hidden by instance attribute
##   y: 2  # Hidden by instance attribute
## d.__dict__ (instance attributes):
##   x: 99
##   y: 111
## d.x is 99
## d.y is 111
```

After initialization, there are **class** attributes `x` and `y`, _and_ **instance** attributes `x` and `y`.
The `@dataclass` decorator looks at the class attributes and generates an `__init__` that creates the corresponding instance attributes.
Note that after assigning to the instance attributes with `d.x = 99` and `d.y = 111`, the class attributes are unchanged.

What happens if you define your own `__init__` for a data class?

```python
# dataclass_with_init.py
from dataclasses import dataclass
from class_and_instance import show_dicts
from class_methods import show_methods


@dataclass
class DI:
    x: int = 1
    y: int = 2

    def __init__(self):
        pass


show_methods(DI)
## class DI:
##   __init__(self)
##   __annotate_func__(format, /)
##   __replace__(self, /, **changes)
##   __repr__(self)
##   __eq__(self, other)
di = DI()
show_dicts(di, "di")
## DI.__dict__ (class attributes):
##   x: 1
##   y: 2
## di.__dict__ (instance attributes):
##   x: <not present>
##   y: <not present>
## di.x is 1
## di.y is 2
di.x = 99
show_dicts(di, "di")
## DI.__dict__ (class attributes):
##   x: 1  # Hidden by instance attribute
##   y: 2
## di.__dict__ (instance attributes):
##   x: 99
##   y: <not present>
## di.x is 99
## di.y is 2
di.y = 111
show_dicts(di, "di")
## DI.__dict__ (class attributes):
##   x: 1  # Hidden by instance attribute
##   y: 2  # Hidden by instance attribute
## di.__dict__ (instance attributes):
##   x: 99
##   y: 111
## di.x is 99
## di.y is 111
```

The generated `__init__` is suppressed.
That means your `__init__` is responsible for setting up the instance attributes; if you don't, they won't be created.
As a result, even though `x` and `y` are still listed as data class attributes, the instance starts out with no `x` or `y` in its `__dict__`.
Accessing `di.x` and `di.y` falls back to the class attributes, just like in a regular class.
Only when you assign new values to `di.x` and `di.y` do they become instance attributes and override the class-level defaults.

## The Power of Custom Types

Creating custom types simplifies managing data integrity and composition,
reduces repetitive checks, and centralizes validation.
Combined with functional programming principles like immutability and type composition,
custom types significantly enhance the clarity, maintainability, and robustness of your code.
Once you adopt this approach, you'll find your development process smoother, more reliable, and far more enjoyable.

- Incorporate examples from https://github.com/BruceEckel/DataClassesAsTypes
