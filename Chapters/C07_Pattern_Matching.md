# Pattern Matching

Python 3.10 added _structural pattern matching_ via the `match...case` statement.
Pattern matching compares a value (the _subject_) against a series of _patterns_, and executes code based on the pattern that fits.
Unlike a simple switch on a single value, structural pattern matching lets you destructure complex data and test for conditions in one expressive syntax.

A `match` statement looks similar to a **switch**/**case** from other languages, but Python's patterns can match structure (like the shape of a sequence or the attributes of an object) and bind variables.
Python tries each `case` in order and executes the first one that matches, with a wildcard `_` as a catch-all default.
Patterns can include literals, names, and even nested sub-patterns to unpack data.
We will cover each pattern type in detail, with examples and tips on how they interact with Python's type system and static analysis.

## Literal Patterns

A _literal pattern_ specifies a concrete value that the subject must equal.
These are most akin to classic switch-case constants.
Literal patterns can be numbers, strings, booleans, `None`, or even singleton objects.
The pattern matches if the subject is equal to that value (using `==` comparison for most types).
For example, consider matching an HTTP status code to a message:

```python
# example_1.py
status = 404
match status:
    case 200:
        result = "OK"
    case 404:
        result = "Not Found"
    case _:
        result = "Unknown status"
```

The cases `200` and `404` are literal patterns.
The `match` compares `status` against each literal in turn.
Because `status == 404`, the second case matches and `result` becomes `"Not Found"`.
If `status` had been something else, the wildcard `_` (covered later) would catch it as a default.

**How literal matching works:** Most literal constants match by equality.
However, Python's three singletons--`True`, `False`, and `None`--are matched by identity (i.e., the subject _is_ that object).
This distinction rarely matters in practice (since there's only one `True` etc.), but it's a defined part of the rules.
You can also combine multiple literals in one pattern using the OR operator `|` (described in the OR Patterns section) to match any of several constants (e.g., `case 401 | 403 | 404:` to handle multiple error codes in one branch).

**Named constants in patterns:** A common desire is to match against a constant defined elsewhere (like an enumeration member or a module-level constant).
In pattern matching, a bare name is treated as a capture variable (see _Capture Patterns_ below), not a constant.
To use a named value as a literal pattern, you must qualify it so that it's not seen as a new variable.
The rule is that named constants must appear as dotted names (or attributes) in patterns.
For example, to match an `Enum` member:

```python
# colors.py
from enum import Enum


class Color(Enum):
    RED = 1
    GREEN = 2
    BLUE = 3
```

```python
# color_demo.py
from colors import Color

color = Color.GREEN
match color:
    case Color.RED:
        print("It's red!")
    case Color.GREEN:
        print("It's green!")
    case Color.BLUE:
        print("It's blue!")
## It's green!
```

Here `Color.RED` etc.
are dotted names, so the pattern treats them as specific constant values rather than capturing new variables named `RED`, `GREEN`, `BLUE`.
This will correctly match the enum value in `color`.
(If you had written just `RED` as a pattern, it would be a capture pattern instead, which is likely not what you want.)

**Static analysis angle:** Literal patterns work great with type hints for `Literal` types and Enums.
If a variable is annotated with a union of literal values or an `Enum` type, a series of literal `case` clauses can cover all possibilities.
Modern static type checkers (like mypy or PyRight) can perform _exhaustiveness checking_ on `match` statements.
This means if you forget to handle one of the specified values, the type checker can warn you.
For instance, if `status` was of type `Literal[200, 404]`, the checker would expect all those values to be matched.
Similarly, with the `Color` enum above, a checker knows there are three members; if you omit a case for one of them, it could flag it.
This benefit ensures your pattern matching stays in sync with your data definitions, making your code more robust.

## Capture Patterns

A _capture pattern_ is simply a name (identifier) used in a pattern, which will "capture" the value from the subject if that pattern position matches.
Instead of testing for a specific value, a capture pattern matches anything and binds a variable to the subject (or subcomponent of the subject).
Capture patterns let you extract pieces of data for use in the body of the case.

**Syntax:** Writing a bare name in a pattern creates a capture.
For example, `case x:` will match any subject value and assign it to the variable `x`.
Capture patterns can also appear inside compound patterns (like inside a sequence or mapping), where they bind a part of the structure.

**Important:** `_` (underscore) is not a capture; it's a special wildcard pattern that discards the value.
Any other name will be treated as a capture.
If the name wasn't already defined in the surrounding scope, it will be a new variable set in that case.
(If it was defined outside, pattern matching will not automatically compare against it--it still creates a new binding shadowing the outer variable.
As mentioned, to match an existing variable's value, use a literal or value pattern with a dotted name.)

Consider this simple use of capture patterns:

```python
# example_3.py
command = "hello"
match command:
    case "quit":
        print("Quitting...")
    case other:
        print(f"Received unknown command: {other!r}")
## Received unknown command: 'hello'
```

Here the second case uses `other` as a capture pattern.
If the first case (`"quit"`) doesn't match, the second case will match anything.
The subject `"hello"` is not `"quit"`, so it falls to `case other:`.
This pattern matches unconditionally and binds the name `other` to the value of `command` (which is `"hello"`).
The result is that it prints: `Received unknown command: 'hello'`.
Essentially, `other` serves as a catch-all variable for "anything else."
In this role, a capture is similar to the wildcard `_` (which also matches anything) except that we can use the captured value in the code.

Capture patterns are extremely useful when you need to extract parts of a structure.
For example, matching a tuple `case (x, y):` uses two capture sub-patterns `x` and `y` to pull out the elements of the tuple.
Similarly, `case {"user": name, "id": id}:` on a dictionary captures the values of the `"user"` and `"id"` keys into the variables `name` and `id` respectively.
We will show more of these in Sequence and Mapping patterns.

**Irrefutable patterns:** A capture pattern (on its own) always matches because it imposes no conditions on the value.
Patterns that always succeed are called _irrefutable_.
If an irrefutable pattern is used as a top-level case (like `case x:` at the same indent as case), it matches everything and typically must be the last case (otherwise it would prevent any subsequent cases from ever running).
Using a capture as the last case is one way to handle "default" scenarios while still naming the value.
Often, though, a simple wildcard `_` is used for a default case when the value itself doesn't need to be referenced.

## Wildcard Patterns (`_`)

The _wildcard pattern_ is written as a single underscore `_`.
It matches anything, just like a capture pattern does, but it does not bind any variable.
It means, "I don't care what's here."
It's typically used to ignore certain values or as a catch-all default case.
Since `_` is not a valid variable name (in pattern context it's special-cased), you can use it freely without worrying about collisions or overwriting.

Common uses of the wildcard pattern include:

- The final case of a match (default case) to catch all situations not handled by earlier cases:

```python
# wildcard_final_case.py
def wildcard(status):
    match status:
        case 200:
            message = "OK"
        case 404:
            message = "Not Found"
        case _:
            message = "Unknown"  # `_` matches anything not matched above
```

- Ignoring one or more elements in a sequence pattern:

```python
# wildcard_ignore_elements.py
from typing import Any


def wildcard_ignore(
    point: tuple[float, Any, Any],
) -> None:
    match point:
        case (x, _, _):
            print(f"x-coordinate is {x}")
```

The pattern `(x, _, _)` binds the first element to `x` and ignores the second and third elements.
The underscores indicate we do not need those values.
(If the sequence had a different length or structure, this pattern would fail to match.)

- Ignoring a value in a class or mapping pattern:

```python
# wildcard_ignore_value.py
from typing import NamedTuple


class Player(NamedTuple):
    name: str
    score: int


def player_score(player: Player):
    match player:
        case Player(name=_, score=s):
            print(f"Player has score {s}")
```

This matches a `Player` object of any name, capturing only the `score` attribute into `s`.
The name attribute is ignored.

You can use multiple wildcards in a single pattern if needed (each `_` is independent and just means "ignore this part").
Under the hood, all `_` in a pattern are effectively the same anonymous throwaway--none of them create variables.
This makes `_` safe to use in any number of places in the pattern.

In summary, wildcard patterns are a convenient way to say "match anything here, and I don't intend to use it."
They improve readability by explicitly marking unneeded parts of the structure and are essential for default cases.
Every `match` statement should usually end with either a wildcard case or otherwise guarantee that all possibilities are handled (to avoid falling through with no match).

## Sequence Patterns

_Sequence patterns_ let you match sequence types (like lists, tuples, etc.) by their contents.
They look much like unpacking assignments.
By placing subpatterns in square brackets `[...]` or parentheses `(...)`, you can match on the length of the sequence and the patterns of each element.
This is a powerful way to destructure sequence data.

Suppose we want to categorize a 2D point given as a tuple `(x, y)`:

```python
# example_7.py
point = (0, 5)
match point:
    case (0, 0):
        print("Origin")
    case (0, y):
        print(f"On the Y-axis at y={y}")
    case (x, 0):
        print(f"On the X-axis at x={x}")
    case (x, y):
        print(f"Point at ({x}, {y})")
## On the Y-axis at y=5
```

This match has four sequence patterns, each a tuple of two elements:

- `(0, 0)` is a sequence pattern of two literals, matching only the point `(0, 0)` exactly.
- `(0, y)` matches any 2-tuple whose first element is 0 and captures the second element as `y`.
  So `(0, 5)` fits here, and `y` would be 5, resulting in `On the Y-axis at y=5`.
- `(x, 0)` matches any 2-tuple with second element 0, capturing the first element as `x`.
- `(x, y)` (the most general) matches any 2-tuple, capturing both elements.

Only one case will run: the first one that matches in order.
In our example, `point = (0, 5)` matches the second pattern `(0, y)` because the first element is 0 (literal match) and it binds `y = 5`.
The remaining cases are skipped.

### Details

- **Types that qualify:** Sequence patterns work on any iterable that is sequence-like.
  This generally means instances of `collections.abc.Sequence` (such as list, tuple, range, str) except that mappings (dicts) are treated by the mapping pattern instead (covered in next section).
  For built-in sequences like `list` or `tuple`, the match will check the length and elements.
  For custom sequence classes, Python uses the sequence protocol (`__len__` and `__getitem__`) to attempt a match.
  Strings are considered sequences of characters, so be cautious: a pattern like `case ['H','i']:` would match the string `"Hi"` (as a sequence of two chars) as well as a list `['H','i']`.
  If you specifically want to match a `list` and not a `tuple` or other sequence, you can use a class pattern like `case list([...])` as described below.

- **Length matching:** The number of subpatterns in brackets must match the length of the sequence (unless you use a starred pattern for variable length).
  If the lengths differ, the pattern fails.
  In the example above, each pattern has 2 elements, so only sequences of length 2 can match any of those.
  If `point` were a 3-tuple, none of those cases would match (unless we added a case for 3-length).

- **Element matching:** Each position in the pattern can be any kind of subpattern (literal, capture, wildcard, even another nested pattern).
  All subpatterns must match their corresponding element for the whole pattern to succeed.
  In `(0, y)`, the first subpattern `0` must equal the first element and the second subpattern `y` will always succeed (capturing that element).
  If any subpattern fails, the whole pattern fails, and the next case is tried.

- **Starred subpattern (`*`):** Sequence patterns support a "rest" pattern using `*`.
  This is similar to unpacking with a star in assignments.
  You can write one subpattern as `*name` (or `*_` to ignore) to soak up the remaining elements of a sequence.
  For example:

```python
# example_8.py
def rest_pattern(*values):
    match values:
        case [first, second, *rest]:
            print(f"{first = }, {second = }, {rest = }")


rest_pattern(10, 20, 30, 40)
## first = 10, second = 20, rest = [30, 40]
rest_pattern("a", "b", "c", "d")
## first = 'a', second = 'b', rest = ['c', 'd']
```

This pattern matches any sequence of length `>= 2`.
The first element is bound to `first`, second to `second`, and the rest of the sequence (which could be zero-length if there were exactly two) is bound as a list to `rest`.
If `values` is `[10, 20, 30, 40]`, the output would be "First=10, second=20, rest=[30, 40]".
If `values` is `[10, 20]`, then `rest` would be an empty list `[]`.
Using `*rest` makes the length flexible.
You can only use one starred subpattern in a sequence pattern.
Also note that `*rest` will always be a list, even if the original sequence is a tuple (Python creates a new list for the remaining elements when matching).

The pattern matching syntax (the structure you write after `case`) is not designed to include inline type hints.
Thus, you cannot write something like:
`case [first: int, second: int, *rest: list[int]]:`
However, we can put an annotation on the argument passed to the `match` expression, which is `values`:

```python
# subject_annotations.py
from typing import Tuple


def subject_annotation(*values: int) -> None:
    match values:
        case [first, second, *rest]:
            # Here the type checker infers:
            # --first: int
            # --second: int
            # --rest: list[int]
            print(f"{first = }, {second = }, {rest = }")


subject_annotation(10, 20, 30, 40)
## first = 10, second = 20, rest = [30, 40]
# rest_pattern("a", "b", "c", "d")  # Disallowed
```

**Nested patterns:** You can nest sequence patterns within sequences for multidimensional data.:

```python
# nested_patterns.py
from typing import cast


def nested_pattern(*values: int) -> None:
    match values:
        case [first, second, *rest]:
            # Here the type checker infers:
            # --first: int
            # --second: int
            # --rest: list[int]
            print(f"{first = }, {second = }, {rest = }")

        case [(x, y), *rest]:
            # Known pattern matching limitation in mypy:
            x, y = cast(tuple[int, int], rest)
            print(f"({x=}, {y=}), *{rest}")


nested_pattern(10, 20, 30, 40)
## first = 10, second = 20, rest = [30, 40]
# Type checkers haven't caught up:
nested_pattern((50, 60), 70, 80)  # type: ignore
## first = (50, 60), second = 70, rest = [80]
```

The first element, a 2-tuple, is matched by the subpattern `(x, y)`.
The remaining elements go into `rest`.
This destructures a complex list-of-tuples or tuple-of-tuples structures in a single pattern.

Sequence patterns basically generalize what you might do with a series of `isinstance` checks and tuple unpacking.
They make the code for handling sequences declarative.
Instead of writing length checks and index accesses, you describe the shape of the data you expect.
This can be both clearer and less error-prone.

**Type hints and static analysis:** If a variable is annotated with a sequence type with a fixed length (e.g.
`tuple[int, int, int]` for a triple), a corresponding sequence pattern (like `[x, y, z]`) naturally fits that structure.
Static type checkers can verify that your patterns make sense given the declared types.
For example, if a function parameter is `coords: tuple[int, int]`, then a pattern with two elements will always match, whereas a pattern with three would be flagged as possibly unreachable (since a tuple[int,int] can't have length 3).
Additionally, the types of captured variables can be inferred: if `coords` is `tuple[int,int]`, then in `case (x, y):` the checker knows `x` and `y` are `int`.
This synergy makes pattern matching with sequences both convenient and type-safe in well-typed code.

## Mapping Patterns

Mapping patterns are designed to match dictionary-like objects by their keys and values.
They use a `{...}` pattern syntax that resembles a dictionary literal,
but in a `case` pattern it means "match a mapping with these keys and corresponding value patterns."
This is useful for working with JSON-like data or configuration dictionaries.

For example, imagine we receive event data as dictionaries, and we want to handle different event types:

```python
# example_9.py
event = {"type": "keypress", "key": "Enter"}
match event:
    case {"type": "keypress", "key": k}:
        print(f"Key pressed: {k}")
    case {"type": "mousemove", "x": x, "y": y}:
        print(f"Mouse moved to ({x}, {y})")
    case _:
        print("Unknown event")
## Key pressed: Enter
```

In this match:

- The first case `{"type": "keypress", "key": k}` matches any mapping that has at least the keys `"type"` and `"key"`, with the `"type"` value equal to the string `"keypress"`, and it captures the `"key"` value into variable `k`.
  For our `event`, this matches (since `event["type"] == "keypress"`), so it would print `Key pressed: Enter`.
- The second case looks for a `"type"` of `"mousemove"` and keys `"x"` and `"y"` present, capturing their values into `x` and `y`.
- The default case `_` handles any other shape of event (or if an expected key is missing).

Key rules and features of mapping patterns:

- **Required keys:** All keys listed in the pattern must be present in the subject mapping for a match.
  If any of those keys are missing in the dict, the pattern fails.
  In the example, if `event` lacked an `"x"` key, it wouldn't match the second pattern.

- **Literal keys:** The keys in the pattern are taken as literal constants (not variables).
  Typically, they will be quoted strings (as above) or other hashable constants (like numbers or enum values).
  You cannot use a capture for a key name--that wouldn't make sense because a capture binds to a value, not a key.
  (If you need to iterate or check arbitrary keys, pattern matching isn't the tool; you'd use normal dict methods in that case.)

- **Value subpatterns:** For each key in the pattern, you provide a subpattern that will be matched against the value for that key.
  In `{"key": k}`, the subpattern is the capture `k` which matches any value and binds it.
  In `{"type": "keypress"}`, the subpattern is the literal `"keypress"`, so that requires the subject's `"type"` value to equal that string.
  You can nest deeper patterns too; e.g., `case {"pos": (x, y)}` would require a `"pos"` key whose value is a sequence of length 2 (tuple/list) matching the subpattern `(x, y)`.

- **Extra keys:** By default, a mapping pattern does not require that the subject has no other keys besides the ones listed.
  It only insists those specified keys exist with matching values.
  Additional keys in the dictionary are ignored (they don't make the match fail).
  In our example, if `event` had other keys (like `"time": 12345`), the first pattern could still match as long as `"type"` and `"key"` were there and correct.
  If you want to ensure no extra keys, you can use the double-star wildcard.
  For example, `case {"type": t, \*\*rest}:` will match and capture all other keys and values into a new dict `rest`.
  Conversely, `case {"type": t} if len(event) == 1:` could be used with a guard to ensure only that key is present, but `\*\*rest` is the idiomatic way to capture "the rest" of a mapping.

- **Mapping type:** By default, the mapping pattern works on `dict` and other `Mapping` implementations (it checks for the presence of a mapping interface).
  If the subject is not a mapping, the pattern will fail.
  If you specifically want to narrow the type (say you only want to match actual `dict` objects), you could combine a class pattern with a mapping pattern using the syntax `case dict({...})` similarly to how we did `list([...])` for sequences.
  This would first check `isinstance(subject, dict)` then apply the mapping subpattern.

```python
# double_star_wildcard.py
user_info = {
    "name": "Alice",
    "age": 30,
    "country": "US",
}

match user_info:
    case {"name": name, **rest}:
        print(f"Name: {name}, info: {rest}")
## Name: Alice, info: {'age': 30, 'country': 'US'}
```

This pattern looks for a `"name"` key and captures its value into `name`.
The `**rest` in the pattern captures any remaining key-value pairs into the dictionary `rest`.
So for the given `user_info`, it would print something like: "Name is Alice, other info: {'age': 30, 'country': 'US'}".
If `user_info` had only a `"name"` key, then `rest` would be an empty dict.
If it had no `"name"` key, the pattern would not match at all.

**Static analysis and mappings:** For dicts, static type checking is less precise than with sequences because the set of keys is not always known through type hints (unless using `TypedDict` or specific `Literal` keys).
However, if you use something like `TypedDict` or `Mapping[str, X]`, a type checker can ensure the values you capture are of the expected type `X`.
Pattern matching shines in expressiveness rather than static type rigor for mappings.
If you have a fixed schema for a dict, pattern matching can clearly express the shape, and a tool like mypy can check that you at least treat captured values consistently with their annotated types.
(For truly fixed keys, a dataclass or custom class might be a better fit, which leads us to class patterns.)

## Class Patterns

Class patterns match objects of a specific class and extract their attributes.
They use a syntax reminiscent of calling a constructor, but no object is created in a case pattern--instead, Python checks the subject is an instance of that class and then pulls out specified attributes.
This is a form of _structured binding_ or deconstruction for user-defined types.

The basic form is `ClassName(attr1=subpattern1, attr2=subpattern2, ...)`.
You list the class to match and the attributes you want to check or capture.
For example, suppose we have a simple data class representing a user:

```python
# example_10.py
from dataclasses import dataclass


@dataclass
class User:
    name: str
    age: int


user = User("Carol", 25)

match user:
    case User(name="Alice", age=age):
        print(f"Found Alice, age {age}")
    case User(name=name, age=age):
        print(f"User {name} is {age} years old")
    case _:
        print("Not a User instance")
## User Carol is 25 years old
```

What happens here:

- `case User(name="Alice", age=age)`: This matches if `user` is an instance of `User` and its `name` attribute equals `"Alice"`.
  If so, it captures the `age` attribute into the variable `age`.
  In our example `user.name` is `Carol`, not `Alice`, so this case fails.
- `case User(name=name, age=age)`: This matches any `User` instance (since no literal value restrictions now, just captures).
  It will bind `name = user.name` and `age = user.age`.
  For our `User("Carol", 25)`, this matches, setting `name = "Carol"` and `age = 25`, and prints "User Carol is 25 years old."
- `case _`: If `user` wasn't a `User` at all (say it was an int or some other type), the first two patterns would fail and the wildcard would catch it.
  Here we put a message for non-User instances.

So effectively, `User(name=X, age=Y)` in a pattern means "is the subject a `User`?
If yes, let `X = subject.name` and `Y = subject.age`, and proceed; otherwise this pattern fails."
The class pattern is doing an `isinstance(subject, User)` check and attribute lookups under the hood.

### Details

- **Type check**: When you use a class in a pattern, Python will call `isinstance(subject, ClassName)`.
  If that fails, the pattern doesn't match, period.
  This means class patterns naturally filter by type.
  This is great for branching logic based on object type without manually calling `isinstance` in your code.
- **Attribute matching**: By specifying `attr=...` in the pattern, Python will retrieve that attribute from the object and attempt to match it to the given subpattern.
  All specified attributes must exist, and all their subpatterns must match for the class pattern to succeed.
  In the `User(name=name, age=age)` case, it checks that `user.name` exists (it does) and binds it, and `user.age` exists and binds it.
  You can also put literal patterns for attributes (like the `"Alice"` literal for `name` in the first case), requiring that attribute to equal a specific value.
- **Positional parameters and `__match_args__`:** The example above used `name=` and `age=` as keyword patterns.
  Python's pattern matching also allows _positional_ subpatterns in class patterns, which are matched against attributes defined by the class's `__match_args__`.
  By default, dataclasses and normal classes don't set `__match_args__` automatically (it's an attribute you can define as a tuple of attribute names).
  For example, if `User.__match_args__ = ("name", "age")`, then you could write `case User("Alice", age)` as shorthand for the same pattern.
  In the absence of `__match_args__`, you must use keyword `attr=value` form to match attributes.
  Using positional patterns on a class without `__match_args__` will result in a MatchError at runtime.
  For clarity, many developers prefer the keyword form even if `__match_args__` is set, because it's explicit about which attribute is matched.
- **Multiple class patterns and inheritance:** If you have a class hierarchy, a class pattern will match subclasses as well (since it's based on `isinstance`).
  If you need to differentiate subclasses, you can use different class patterns or guards.
  Class patterns can also be combined with OR patterns to accept an object of one of several classes.
  For example, `case Cat(name=n) | Dog(name=n): ...` could match either a `Cat` or `Dog` instance and capture a `name` attribute from either.

One subtle aspect to remember is that writing something like `case User("Bob")` in a pattern does not call the `User` constructor.
It might look like a construction, but in a `case` context it's pattern syntax.
Whatever appears after `case` is interpreted purely as a pattern, not normal executable code.
If `User` were a dataclass with a `__post_init__` that prints when an object is created,
a subject expression of `match User("Alice"):` creates a `User("Alice")` instance as an expression to match.
But `case User("Bob"):` does not create a new user; it just means "match a User with some attribute equal to Bob."
This distinction is important.
In summary: class patterns let you destructure objects, not create them.

**Customizing class matching:** If you are designing your own classes to be matched frequently, you might consider adding a `__match_args__` for convenience, or even defining a special `__match_repr__` (in Python 3.11+, some classes can control matching via `__match_args__` and
`__match_self__`, but that's beyond the scope of this chapter).
For most uses, using keyword patterns as shown is sufficient.

**Static analysis benefits:** Class patterns go hand-in-hand with type hints.
If a variable is annotated as a base class or a union of classes, a match statement with class patterns can effectively act as a type-safe downcast.
For example, if a function parameter `shape: Shape` where `Shape` is a union of `Circle | Square`, you might do:

```python
# example_11.py
from typing_extensions import NamedTuple


class Circle(NamedTuple):
    radius: float


class Square(NamedTuple):
    side: float


def shape_area(shape: Circle | Square) -> float:
    match shape:
        case Circle(radius=r):
            # Here shape is type Circle:
            return 3.14 * r**2
        case Square(side=s):
            # Here shape is type Square:
            return s**2
        case _:
            raise ValueError("Unsupported shape")
```

Within each case, static type checkers know `shape` (or the captured attributes) have the specific class type, so you get auto-completion and type checking on those attributes.
Furthermore, like with enums, a checker can warn if your match isn't exhaustive over all possible classes in the union.
Class patterns thus enable a form of _type narrowing_ similar to `isinstance` checks, but often more cleanly.

## OR Patterns (`|`)

An _OR pattern_ (also called alternative pattern) allows one case to match multiple different patterns.
You use the vertical bar `|` to separate two or more subpatterns.
The whole pattern matches if any one of the subpatterns matches.
OR patterns are quite flexible--the subpatterns can be of completely different shapes or types.
This is useful to avoid repetition when the action for multiple cases would be the same.

A simple example of OR patterns is handling multiple literals in one go.
For instance, if you want to check if some input is an affirmative "yes" in various forms:

```python
# example_12.py
user_input = "y"
match user_input.lower:
    case "yes" | "y" | "yeah":
        print("User said yes")
    case "no" | "n" | "nope":
        print("User said no")
    case _:
        print("Unrecognized response")
## Unrecognized response
```

Here `"yes" | "y" | "yeah"` is a single pattern that will match the subject if it equals any of those three strings.
The first case will trigger for `"yes"`, `"Y"`, `"yeah"`, etc.
(we lowercased the input to handle capital letters).
Similarly, for the negative responses.
This is more concise than writing separate cases for each variant, and it keeps logically related alternatives together.

OR patterns are not limited to literals; you can alternate between any pattern types.
For example:

- `case 0 | 1 | 2:` would match if the subject is 0, 1, or 2.
- `case (0, 0) | (0, y) | (x, 0):` could combine some of the tuple patterns from earlier into one case (though you might separate for clarity, it's possible to combine).
- `case User(name="Alice") | User(name="Bob"):` could run the same block for either Alice or Bob, if that's the logic needed.

Each alternative pattern is tried in order (left to right) as part of the same case.
If anyone succeeds, the whole OR pattern succeeds and that case executes.
If an OR pattern is complex, be mindful that all subpatterns should make sense in the same context because they share the same action block.
Also, variables bound in an `OR` pattern must be bound in all alternatives to be usable in the block (otherwise it'd be ambiguous which value they have).
For instance, `case ("a", x) | ("b", x):` is valid because either way an `x` will be bound (if the tuple second element,
whether the pattern matches "a" or "b" as first element).
But `case ("a", x) | "foo":` is tricky--in the first alternative `x` would be bound, but in the second alternative (just the string "foo"), there's no `x`.
In such cases, the capture `x` is not allowed because it wouldn't always have a value.
You'd need to restructure the patterns (perhaps use two separate cases in that scenario).

OR patterns are great for merging cases that result in the same outcome, but if each alternative needs a very different explanation, separate cases might be clearer.
However, for things like multiple literal aliases (as shown with "yes"/"y"/"yeah"), OR patterns keep the code succinct.

**Type checking with OR patterns:** If your patterns correspond to different types, a static type checker will infer the subject is one of those types after the match.
For example, if you do:

```python
# example_13.py
def type_narrowing(data: int | float | str):
    match data:
        case int(x) | float(x):
            ...
            # handle as numeric (x will be int or float here)
        case str(s):
            ...
            # handle as string
```

Here `int(x) | float(x)` uses two class patterns in an OR.
In the action block, `x` is either int or float.
Some type checkers might narrow it to a common supertype (like `x: float` if float and int are both numbers--int is subtype of float in the type system).
If you need to handle each type differently, it's better to split into separate cases.
But if the handling is the same (say you treat int and float uniformly as "number"), OR is perfect.
For literal OR patterns, as mentioned, exhaustiveness can be checked.
Ensure you cover the necessary types for class OR patterns.

Generally, OR patterns complement union types in annotations: if a variable is `X | Y`, a match with `case X(...)|Y(...):` will cover those.
Remember that the action block sees the union of the possibilities.

## AS Patterns

An _AS pattern_ allows you to capture a matched value under a name while still enforcing a subpattern on it.
It uses the syntax `<pattern> as <variable>`.
This is extremely handy when you want to both check a complex pattern and keep a reference to the whole thing (or a large part of it) for use in the code.

A simple scenario: matching a sequence but also retaining it:

```python
# example_14.py
pair = [4, 5]
match pair:
    case [first, second] as full_pair:
        print(
            f"First element: {first}, second: {second}, pair: {full_pair}"
        )
## First element: 4, second: 5, pair: [4, 5]
```

This will match if `pair` is a sequence of length 2 (since the subpattern is `[first, second]`).
If it matches, it binds `first = 4`, `second = 5`, and additionally `full_pair = pair` (i.e., the entire list `[4, 5]`).
The output here would be: "First element: 4, second: 5, pair: [4, 5]".
The `as` keyword effectively gives a name to the value that the preceding subpattern matched.

Another use case: suppose you have nested structures and want to both break them down and keep some part intact.
For instance, consider parsing a nested coordinate:

```python
# example_15.py
data = {"coords": [7, 3]}
match data:
    case {"coords": [x, y] as point}:
        print(f"Point {point} has x={x}, y={y}")
## Point [7, 3] has x=7, y=3
```

This pattern checks that `data` is a mapping with a `"coords"` key whose value is a sequence of two elements.
If that matches, it captures `x` and `y` from the sequence, and also captures the entire sequence as `point`.
In our example, it would print: `Point [7, 3] has x=7, y=3`.
We got to both validate the structure (`"coords"` exists, has two elements) and keep the list `[7,3]` intact in `point` for convenient use (perhaps to pass it somewhere as a whole).

Key points for `as` patterns:

- The subpattern before `as` is fully matched first.
  Only if it succeeds will the `as` binding happen.
  If the subpattern fails, the whole pattern fails (and nothing is bound).
- The name after `as` will be bound to the exact value that the subpattern matched.
  If the subpattern spans multiple elements (like `[x, y]` matching a list), the name gets the entire matched object (the list).
  If the subpattern is just part of the structure, you essentially get a reference to that part.
- You can use `as` after any complex pattern, not just sequences.
  For example: `case User(name=n, age=a) as u:` would match a `User` into `n` and `a` and also bind `u` to the whole User object.
  This might seem redundant (since you already have the object in the variable being matched, e.g., `user`), but it becomes useful in OR patterns or nested patterns where you don't have a simple name for the whole thing in that scope.
- Only one `as` is allowed at the same pattern level (you can't do `A as x as y`).
  However, you can nest them in different parts of a pattern if needed.

**Why use `as`?** Sometimes after matching a structure, you need the whole object for something (like logging it, or passing it to another function), and reconstructing it from parts would be inconvenient.
`as` provides a shorthand to avoid repeated computation.
It also improves clarity when you want to refer to "the thing we just matched" without losing the context after destructuring it.

One common pattern is using `as` in the default case to bind the unmatched value for error reporting or assertion.
For example:

```python
# example_16.py
from colors import Color


def handle_color(color: Color):
    match color:
        case Color.RED | Color.GREEN | Color.BLUE:
            ...  # handle known colors
        case _ as unknown:
            raise ValueError(f"Unknown color: {unknown}")
```

Here, `_ as unknown` catches anything not handled and gives it the name `unknown` so we can include it in the error message.
This is clearer than just `_` and then using the original variable (especially if the original variable might not be directly accessible, or you want to emphasize the unmatched value).

**Relation to static analysis:** The `as` pattern doesn't change what types are matched; it just introduces an extra name.
Static checkers will give that name the type of the subpattern's value.
In the example with `{"coords": [x,y] as point}`, if `data` is of type `dict[str, list[int]]`, then `point` is inferred as `list[int]` (same type as `data["coords"]`), while `x` and `y` are `int`.
It's mainly a convenience; the presence of `as` doesn't affect whether a pattern matches or not, so it doesn't factor into exhaustiveness or type narrowing decisions beyond providing a new symbol.

## Guard Patterns (Pattern Guards)

Sometimes a pattern needs an additional condition beyond just structural matching.
A _Guard_ specifies an `if <condition>` at the end of a case pattern, making the case only match if the pattern succeeds and the condition is true.
This is useful for imposing value constraints that can't be expressed by the pattern alone.

The syntax is: `case <pattern> if <boolean expression>:`.
The guard expression can use the variables bound by the pattern (as well as any other in-scope names) to decide whether to accept the match.

For example, suppose we want to match a pair of numbers but only if they satisfy some relationship:

```python
# example_17.py
pair = (5, 5)
match pair:
    case (x, y) if x == y:
        print("The two values are equal.")
    case (x, y):
        print("The values are different.")
## The two values are equal.
```

Here the first case is a sequence pattern `(x, y)` with a guard `if x == y`.
This will match any 2-tuple (binding `x` and `y`), then check the guard condition.
If `x == y`, then and only then does the case succeed.
In our example, `pair` is `(5,5)`, so it matches `(x,y)` with `x=5, y=5`, then the guard `5 == 5` is true, so it prints "The two values are equal." If `pair` were `(5, 7)`, the first pattern would match structurally (`x=5,y=7`), but the guard
`5 == 7` would be false, causing that case to fail overall and move to the next case.
The second case has no guard and would then match by default, printing "The values are different."

Guards effectively let you refine a pattern match with arbitrary logic:

- Use guards to check relationships between captured variables (like x == y, or one value greater than another, etc.).
- Use guards to call functions or methods for deeper checks (e.g., `case User(age=a) if a >= 18:` to only match adult users, or `case s if validate(s):` to apply an external predicate).
- Guards can also prevent a case from handling a scenario that should be passed to a later case.
  For instance, if you have overlapping patterns, a guard can differentiate them.

It's important to note that the guard is evaluated after the pattern matches.
If the pattern doesn't match, Python doesn't even evaluate the guard.
If the pattern matches but the guard is False, the overall result is as if the pattern didn't match at all, and the next case is tried.

One must be careful with guards: since they can run arbitrary code, they could have side effects or be slow.
Keep guards relatively simple and pure (avoid changing state in a guard).
They should ideally just inspect the bound variables or the subject.

Combining mapping patterns with guards can handle situations like "match a dict with a key and then check something about the value":

```python
# example_18.py
from typing import Any, cast

request = {"method": "POST", "payload": {"id": 42}}

match request:
    case {"method": m, "payload": data} if (
        m == "POST" and "id" in data
    ):
        data = cast(dict[str, Any], data)
        print(f"POST request with id {data['id']}")

    case {"method": m}:
        print(f"Other request method: {m}")
## POST request with id 42
```

In the first case, the pattern `{"method": m, "payload": data}` extracts `m` and `data`.
The guard then checks that `m` is "POST" and that the dictionary `data` has an `"id"` key.
Only if both are true does the case run.
Otherwise, it falls through to perhaps a more general case (second one handles any other method).

**Guard vs multiple patterns:** Sometimes you can express the same logic with either a more complex pattern or a guard.
For example, `case (x, y) if x == y:` could also be expressed by a single pattern if Python allowed something like `(x, x)` (which it currently does not--you can't repeat the same capture name in one pattern, since that would be ambiguous).
In this case, the guard was necessary to enforce equality.
In other situations, you might have the choice: e.g., `case [*_] if len(some_list) > 5:` versus `case [_, _, _, _, _, *_]:` to check "at least 6 elements."
The latter uses a pattern with star to check length in structure, the former uses a guard with a length check.
Both work; using patterns for structural conditions and guards for non-structural conditions is a good guideline.

**Static analysis:** Guards are essentially runtime checks, and static type checkers typically don't reason about them much.
However, if a guard uses an `isinstance` or similar, a smart type checker might narrow types in the true branch.
For example:

```python
# example_19.py


def narrow(obj):
    match obj:
        case list as lst if all(isinstance(x, int) for x in lst):
            # Here, lst is a list and we asserted all elements are int.
            total: int = sum(lst)
```

In this contrived example, the guard ensures every element in the list is int, so inside the case it might be safe to treat it as `list[int]`.
Type checkers are not guaranteed to catch that nuance, but you as the programmer know it.
More commonly, you'd have already annotated or known types.
Guards are mainly for logic, not for static type discrimination (that's what class patterns are for).

## Pattern Matching vs.

Inheritance

## Conclusion

Structural pattern matching can be composed in various ways--you can nest patterns arbitrarily, use OR inside sequence patterns, add guards to class patterns, and so on, to model the logic you need.

When used thoughtfully, pattern matching can make code more readable by aligning it closely with the structure of the data it's handling.
It can reduce boilerplate (no more long chains of `isinstance` and indexing) and help catch errors (exhaustiveness checks with static typing, for example).
Your code will be more readable and maintainable if you do not overcomplicate patterns--strive for clarity.
Often a straightforward series of cases is better than one mega-pattern that is hard to understand.

With practice, you'll find pattern matching to be a natural extension of Python's ethos of readable and expressive code.
It brings Python closer to languages like Scala or Haskell in this regard, but in a Pythonic way.
Use the references and examples in this chapter as a guide to the various forms, and happy matching!

## References

1. [Structural pattern matching in Python 3.10](https://benhoyt.com/writings/python-pattern-matching/)
2. [What's New In Python 3.10--Python 3.13.3 documentation](https://docs.python.org/3/whatsnew/3.10.html)
3. [Literal types and Enums--mypy 1.15.0 documentation](https://mypy.readthedocs.io/en/stable/literal_types.html)
4. [Structural Pattern Matching in Python--Real Python](https://realpython.com/structural-pattern-matching/)
