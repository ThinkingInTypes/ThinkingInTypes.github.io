# What is a Type?

A _type_ is a set of values.
It classifies and categorizes data.
It can also define operations.

## Defining "Type" in Programming

For example, the integer type allows arithmetic operations like addition or subtraction, while a string type supports operations like concatenation.
The purpose of having types is to give meaning to data and to inform the program (and the programmer) what kinds of behavior are valid for that data.
If a piece of data is labeled as an integer type, the language knows it can perform numerical calculations on it; if it's a string type, it knows operations like splitting or joining make sense.

In Python, types are associated with values, not with variables.
You don't explicitly declare variable types; instead, any variable can reference any object, and that object carries its type with it.
In Python, an object knows its type.
You can always check that type at runtime using the built-in `type()` function or `isinstance()` function:

```python
# example_1.py
print(type(42))
## <class 'int'>
print(type("Hello"))
## <class 'str'>
print(isinstance(42, int))
## True
print(isinstance("Hello", int))
## False
```

The calls to `isinstance` confirm that 42 is indeed an `int` and that the string `"Hello"` is not an `int`.
Types determine what operations are allowed; for instance, you can multiply integers, but multiplying two strings is not defined (except by repeating the string, which is a different operation in Python).

Types act as a contract or promise about data.
If a function expects a certain type, providing data of the wrong type can lead to errors.
For example, giving a text string to a mathematical formula that expects a number will cause problems.
In short, a type defines both a set of values and the permitted operations on those values, setting the stage for how data is used in a program.

Python comes with a rich set of built-in types (numbers, strings, lists, dictionaries, etc.).
You can also define custom types (classes) for more complex data.
This chapter focuses on what a "type" means and how Python's approach to types influences how we write and maintain code.

## Dynamic vs. Static Typing

One of the core distinctions in programming language type systems is dynamic typing vs.
static typing.
Python is a _dynamically typed_ language, whereas languages like C++ or Java are typically _statically typed_.
Let's unpack what that means and the pros and cons of each approach.

- **Statically Typed Languages:** In a statically typed language, the type of each variable and expression is determined at compile time (before the program runs).
  You usually must declare the types of your variables (e.g., in Java: `int count = 5;`).
  The compiler uses these declarations to verify that you are using variables in a type-safe way.
  If you attempt an invalid operation, like adding a number to a string, a compile-time error is raised and the program won't run until the error is fixed.
  In short, static type checking finds type errors by analyzing the program's source code before execution.
  This early detection can prevent many runtime errors.
  Static typing can also enable performance optimizations, since knowing the types in advance allows the compiler to produce more efficient machine code (for example, it doesn't need to check types during each operation at runtime).

- **Dynamically Typed Languages:** In a dynamically typed language, the variable type is allowed to change over its lifetime, and type checks are done at runtime.
  You do not have to declare types explicitly.
  For example, in Python you can do:

```python
# example_2.py
x = 10  # x is an int
# Reassign to a different type:
x = "hello"  # now x is a str
print(x)  # Output: hello
## hello
```

Python will infer the type of `x` from whatever value it's holding at the moment.
Here `x` started as an integer and later became a string.
This is perfectly valid in Python.
The flexibility of dynamic typing makes it easy to write quick scripts and prototypes because you don't have to constantly specify types--the interpreter figures it out as the program runs.

The example above shows Python's dynamic nature: you can assign a value of any type to `x`, and later even assign a value of a different type to the same `x`.
However, this flexibility comes at a price.
Because type checks are done as the code runs, if you perform an operation that the data type doesn't support, you'll only find out at runtime (perhaps causing your program to crash if not handled).
For instance:

```python
# example_3.py
from book_utils import Catch

x = 10
with Catch():
    # Can't add a str to an int:
    result = x + "world"  # type: ignore
## Error: unsupported operand type(s) for +: 'int'
## and 'str'
```

We attempted to "add" a string `"world"` to `x`, which is an integer.
Python only discovers the problem while running the line: realizing it can't add an `int` and `str`, it throws a `TypeError` exception.
In a statically typed language, such an error would be caught before running the program (the code wouldn't compile).

To summarize the difference:

- In static typing, type errors are caught early--before the program runs--which can make debugging easier and programs more reliable.
  You also get better documentation from explicit type annotations in code.
  But static typing requires more upfront work: declaring types and sometimes contending with more rigid code, which can slow down initial development or make code less flexible to change.
- In dynamic typing, you get more flexibility--you can write code faster without specifying types everywhere, and the same variable can hold different types of data over its lifetime.
  This is great for quick iterations and when you want to write generic code.
  The downside is that type-related mistakes are only caught when that line of code runs, which might be far into a program's execution.
  This can lead to runtime errors and sometimes makes large codebases harder to reason about (you have to remember or check what type a variable might be at a given point).

It's important to note that dynamic vs.
static is about when type checking happens (at runtime vs.
compile time).
It's independent of another concept often mentioned: strong vs.
weak typing, which is about how strictly types are treated.
Python, for example, is strongly typed--it won't implicitly convert types for you in unchecked ways.
Trying to add a number to a string, as we saw, is not allowed (Python won't guess that maybe you meant `"10" + "world"` or something--it errors out).
In Python, values have a definite type, and you can't treat a value as a different type without an explicit conversion.
Many static languages are also strongly typed, but some languages are _weakly typed_ (they might, for instance, automatically convert strings to numbers in certain contexts, which can lead to subtle bugs).
The key takeaway is that Python is dynamically and strongly typed: type checks happen at runtime, and the interpreter will raise an error if you attempt an operation on incompatible types.

## Duck Typing in Python

Python's dynamic typing is closely related to the idea of duck typing.
The name comes from the phrase "If it looks like a duck and quacks like a duck, it must be a duck."
In programming, duck typing means that an object's suitability for an operation is determined by the presence of certain methods or properties, rather than the actual type of the object itself.
In other words, "an object is considered compatible with a given type if it has all the methods and attributes that the type requires."
The actual class or inheritance of the object is less important than whether it implements the interface.
This is a very Pythonic idea: "don't check an object's type to determine if it has the right interface; just try to use it, and it will either work or fail."

Duck typing means you often write functions that work on any object that supports the operations you need, rather than only working on specific classes.
For example, consider a function that makes an object quack:

```python
# example_4.py
class Duck:
    def quack(self):
        print("Quack!")


class Car:
    def quack(self):
        print("I can quack, too!")


def quacks(entity):
    entity.quack()


donald = Duck()
studebaker = Car()
quacks(donald)
## Quack!
quacks(studebaker)
## I can quack, too!
```

`Duck` and `Car` each have a `quack()` method.
The function `quacks(entity)` calls `entity.quack()` without caring what type `entity` is.
Thanks to duck typing, both a `Duck` instance and a `Car` instance can be passed to `quacks` and it will work, as long as they implement `quack()`.
The `quacks(donald)` call prints "Quack!", and `quacks(studebaker)` prints "I can quack, too!", even though `studebaker` is not a Duck--it's a Car that happens to know how to quack.
The function didn't check types; it just invoked the method.

But what if we call `quacks(42)` (an integer)?
An int has no `quack()` method, so Python will raise an `AttributeError` at runtime (e.g., "`'int' object has no attribute 'quack'`").
This demonstrates duck typing's approach: "it's better to ask for forgiveness than permission."
We just try to use the object in a duck-like way.
If it quacks, great.
If not, Python throws an error, and we handle that (or let it propagate).
In code, you might handle this with try/except:

```python
# example_5.py
from example_4 import quacks

## Quack!
## I can quack, too!

try:
    quacks(42)
except AttributeError as e:
    print(f"Oops: {e = }")
## Oops: e = AttributeError("'int' object has no
## attribute 'quack'")
```

In Python, it's idiomatic to write code that assumes objects have the right methods (duck typing) and deal with exceptions if they don't, rather than explicitly checking types upfront.

Duck-typed functions are extremely flexible.
Many Python libraries and built-in functions use duck typing so that they can work with a variety of object types as long as those objects support the expected interface.
For example, Python's file-handling functions don't require an object to be a specific "File" class--they just require an object that implements the file interface (methods like `.read()` or `.write()`).
As long as the object passed in has those methods, the function will work.

However, duck typing can sometimes make it harder to reason about code in large projects--because any object with a `quack` method will do, you might accidentally pass the wrong object to a function and only find out at runtime.
This is where the balance between flexibility and safety comes into play, which leads us to the evolution of Python's type system in recent years.

## From Duck Typing to Type Hints

Historically, Python has been a dynamically typed language.
The language didn't have a way to explicitly declare the type of variable or function parameter in code.
Developers used documentation or naming conventions to indicate expected types (for example, a comment like `# param x is an int`), but these were not enforced.
As codebases grew, this lack of explicit type information started to become a pain point for some projects.
It's easy to lose track of what types are flowing through the code, which can lead to bugs or make the code harder to maintain.

Python 3.5 introduced optional syntax for adding type hints to your code.
These are optional annotations that you can add to function definitions, variables, and class attributes to declare what type they are supposed to be.
Crucially, these type hints do not change how the code runs; Python remains dynamically typed at runtime.
The hints are mainly for the benefit of the developers and tooling.

For example, here's a function without type hints, and then with type hints:

```python
# example_6.py
# Without type hints:
def greet1(name):
    return "Hello, " + name


# With type hints:
def greet2(name: str) -> str:
    return "Hello, " + name
```

In the second version, the `str` in `name: str` and `-> str` is a type annotation.
It indicates that `name` should be a string, and that the function returns a string.
If you run this code, Python will not enforce that `name` is a string--if you pass an integer, it will still run, and likely error out only when it tries to do `"Hello, " + 5`.
In other words, type hints don't make Python statically typed.
They are metadata attached to the functions and variables.
The official Python documentation makes this clear: the Python runtime does not enforce function and variable type annotations; they are meant to be used by third-party tools (like type checkers, IDEs, linters).

The benefits of type hints are seen during development: they serve as documentation and enable static analysis tools to catch errors before running the code.
By reading the annotated `greet` function, a developer (or an IDE) immediately knows that `name` is expected to be a string, which improves readability.
If somewhere else in the code we call `greet(123)`, a type-checking tool can warn us that we're calling `greet` with the wrong type of argument.

A type checker will catch this:

```python
# example_7.py
from book_utils import Catch


def add(a: int, b: int) -> int:
    return a + b


print(add(10, 5))
## 15
with Catch():
    add(10, "5")  # type: ignore
## Error: unsupported operand type(s) for +: 'int'
## and 'str'
```

The second call `add(10, "5")` is a mistake: we intended both arguments to be `int`s.
Running this code would produce a runtime error when trying to add an integer to a string (`TypeError: unsupported operand type(s) for +: 'int' and 'str'`).
A static type checker, however, would catch this before running the program.
For instance, Mypy (one of the most popular Python type checkers) would emit an error like: `error: Argument 2 to "add" has incompatible type "str"; expected "int"`.
This early detection of the bug can save you from having to debug a runtime crash.

Python's adoption of type hints has been gradual and very much optional.
You can start adding types to a few functions, or even one variable at a time.
This approach is sometimes called gradual typing or optional static typing.
The designers of Mypy describe it as an attempt to "combine the benefits of dynamic (or 'duck') typing and static typing."
You don't have to choose one or the other for the whole program; you can get the flexibility of dynamic typing where needed, and the safety/net of static typing where it helps.
Python will happily run code with or without type annotations, and you can mix annotated and unannotated code freely.
This means you can adopt type hints in a legacy codebase incrementally or use them only for the trickiest parts of a new project.

Over the past several Python releases (3.5 through 3.13), the type hinting syntax and capabilities have expanded significantly.
For instance, you can annotate variables (since Python 3.6) in addition to function params and returns:

```python
# example_8.py
count: int = 0
# list[str] instead of typing.List:
texts: list[str] = ["hello", "world"]
```

You can use union types with nice shorthand.
Python 3.10 introduced the `|` operator for types, so instead of writing `typing.Union[str, bytes]` you can just write `str | bytes`:

```python
# example_9.py
from pathlib import Path

from book_utils import Catch


def is_file(file: str | Path) -> bool:
    # Converts string or Path to a Path object:
    p = Path(file)
    return p.exists() and p.is_file()


# Works with a string path:
print(is_file("nonexistent.txt"))
## False
# Works with a Path object:
print(is_file(Path("nonexistent.txt")))
## False
with Catch():
    # Raises TypeError, static checker flags it:
    is_file(12345)  # type: ignore
## Error: argument should be a str or an
## os.PathLike object where __fspath__ returns a
## str, not 'int'
```

The function `is_file` can accept either a file path as a normal string or a `Path` object (from the `pathlib` module)--thanks to the union type `str | Path`.
Inside the function we convert whatever it is to a `Path` for uniform processing.
Passing an integer produces an error when trying to make a `Path(12345)`, because an `int` isn't a valid path.
The type checker tells us about this right away, and very specifically.
Waiting until runtime produces errors that take time and effort to untangle.

The standard library `typing` module provides many advanced types and constructs, which we cover in later chapters:

- Generics (like `list[int]` or `dict[str, int]`)
- `Optional[X]` (which is just shorthand for `X | None` in newer Python versions)
- `Literal` types (specific allowed values)
- `TypedDict` (dicts with specific shape)
- _protocols_ (PEP 544) which are basically static duck typing (you can define an interface that says "this type must have methods X, Y, Z" without caring about inheritance).

## Typing is Optional

Python's type hints are optional and ignored at runtime.
They are a developer tool.
The interpreter will not refuse to run your program if the types don't match:

```python
# example_10.py
value: float = 3.14159
# Reassign to str:
value = "Pi"  # type: ignore
print(value)
## Pi
```

We annotated `value` as a float, but then assigned a string to it.
Python does not enforce the annotation--the code runs and `value` ends up as `"Pi"`.
A type checker warns about that reassignment, but Python itself doesn't mind.
Adding type hints doesn't change Python's runtime behavior unless you use additional frameworks or decorators to enforce types at runtime.

## Why Use Type Annotations?

If type hints are optional, why bother with them?
They produce significant benefits, especially for larger projects:

- Clarity and Readability: Type hints serve as documentation.
  When you see a function signature `def process(data: list[str]) -> bool`, it's immediately clear what is expected: a list of strings goes in, and a boolean comes out.
  You don't have to read through the function body or comments to guess the types.
  This makes it easier for others (and yourself, in the future) to understand the code's intent.
  Type annotations are a form of documentation.

- Early Error Detection: Perhaps the biggest practical advantage is catching bugs before running the code.
  Type checkers catch mistakes while you're coding.
  This is especially useful in large codebases where you might change something in one module and inadvertently break an assumption in another.
  A type checker can often catch such issues at build time or in your editor, rather than letting them slip into runtime.
  This early detection of type errors significantly improves code reliability.

- **Better IDE/Editor Support:** Modern editors and IDEs (like VSCode, PyCharm, etc.) use type information to provide features like autocompletion, jump-to-definition, and inline error highlighting.
  If you declare types, the IDE can help you more.
  For instance, if a function returns an `Employee` object, and you've annotated that, the IDE can auto-suggest `employee.` methods and attributes when you use the result, because it knows the type.
  It can also immediately warn you if you try to call a list method on something that's annotated as a string, for example.
  Type information makes tooling smarter and developer experience better.

- **Refactoring and Maintenance:** When you or someone else needs to modify code, type hints act as a safety net.
  They make it harder to misuse a function or variable inadvertently.
  If you change a function's expected types, all the callers that pass the wrong type will light up in your type checker.
  This makes large-scale refactoring more manageable--you can confidently change the internals of a function or module and rely on the type system to tell you if something incompatible is being done somewhere else.
  This leads to more maintainable code in the long run.

- **Communication of Intent:** Sometimes you might intentionally allow multiple types (using a union) or a very generic type (like `Any` or a base class).
  Other times you expect a very specific protocol.
  Writing that down in code via annotations communicates your intent to anyone reading it.
  It also communicates to static analysis: "I intend this to be of type X," so if later the code violates that intent, it can be flagged.

That said, there are some downsides or challenges with type annotations to be aware of:

- **Initial Overhead:** Writing annotations means more typing (pun intended).
  It can slow down the speed of writing code, especially for quick scripts or one-off tasks where the overhead might not be worth it.
  However, many find that for anything beyond small scripts, the time spent adding type hints is paid back in time saved debugging.

- **Learning Curve:** Python's typing system has grown quite rich, with generics, protocols, type variables, etc.
  Using these effectively may require learning new concepts.
  For intermediate Python programmers, there's a learning curve to understanding things like `Optional`, `Union`, or generics.
  The good news is you can start annotating basic types and only delve into advanced typing features as needed.

- **Runtime Overhead:** By default, there is virtually no runtime overhead for having type annotations (since Python ignores them at runtime).
  However, if you use certain libraries or decorators to enforce type checking at runtime, those will add overhead.
  Also, importing the `typing` module historically had some minor import-time cost (which has been reduced in recent Python versions), but generally this is not a big issue.

- **False Sense of Security:** It's worth remembering that type hints are not a cure-all.
  You can annotate everything and have a clean bill of health from the type checker, and your program can still have bugs (logic errors, runtime issues unrelated to types, etc.).
  Also, if you're interfacing with dynamic parts of Python (like using `hasattr` or doing dynamic attribute setting, or dealing with JSON data), the type checker might not catch misuse because you might be using `Any` or ignoring types in those spots.
  So, use type hints as a helpful tool but still test and validate your code.

Overall, the Python community has increasingly embraced type hints because the benefits (especially for larger projects) have proven valuable: fewer bugs, easier collaboration, improved code quality.
It's a way to get some advantages of statically typed languages without giving up Python's dynamic flexibility entirely.

## Static Type Checkers: `mypy`, `pyright`, and Friends

Type hints by themselves do nothing unless you use a tool to check those hints against your code.
While you might visually inspect code and spot a type mismatch, it's much more reliable to use automated tools.
Two of the most popular type checking tools for Python are mypy and pyright.

- **Mypy:** Mypy has been around since the early days of Python's gradual typing experiment (it was developed alongside PEP 484).
  It's a command-line tool (and a library) that you run on your Python code (or integrate into your editor/IDE) to static-check the types.
  Mypy reads your `.py` files, interprets the type hints, and reports any inconsistencies or errors.
  For example, if you have `def func(x: int) -> None:` and somewhere you call `func("hello")`, mypy will catch that and report an error.
  Mypy aims to be strict and thorough, catching subtle issues (it even tries to infer types of variables where possible and can warn if you, say, add a string and int without any hints given, etc.).
  The philosophy of mypy is to let you start with little to no annotations and gradually add them--it will treat unannotated code as basically `Any` types by default (which don't produce errors), and as you add annotations, it will enforce them.
  As the official mypy documentation states, it "is an optional static type checker for Python that aims to combine the benefits of dynamic (or 'duck') typing and static typing."
  You can run mypy as part of your development or CI (Continuous Integration) to prevent type regressions in a codebase.

- **Pyright:** Pyright is a newer type checker, open-sourced by Microsoft.
  It is known for speed and is designed to handle large projects efficiently.
  Pyright powers the Python type checking in Microsoft's VSCode editor (the Pylance extension).
  Pyright is written in TypeScript (running on Node.js), which might sound unusual, but it means it's optimized for speed and can do things like watch files and re-check only what changed, etc.
  Pyright is also fully aware of all the latest PEPs and typing features.
  According to its documentation, "Pyright is a full-featured, standards-based static type checker for Python.
  It is designed for high performance and can be used with large Python source bases."
  Many developers use Pyright via their editor for instant feedback as they code (and/or in CI as well).
  For instance, as you're coding, Pyright can underline an inconsistent call in red immediately.
  Pyright is also available as a command-line tool (via npm) if you prefer that route.
  One of its selling points is performance--it's been noted to be much faster than mypy on large codebases, though for small-to-medium projects both tools run quickly enough.

Both mypy and pyright adhere to Python's typing rules (PEP 484 and successors) pretty closely.
There are some minor differences and configuration options (for example, how strict they are about certain default behaviors, or handling of untyped code).
Some teams use one, some use the other, and some even use both (one as an editor linter for speed, another as a final check in CI for thoroughness).
The good news is you don't need to lock yourself in--you can try them out and see which fits your workflow.

Aside from mypy and pyright, there are other tools worth mentioning:

- **PyCharm and Other IDEs:** PyCharm has its own built-in type checker that uses the same type hint information to warn about issues.
  It's not as configurable as mypy/pyright, but it often catches many of the same things in real-time.
- **Pylint and Flake8:** These are linters that primarily focus on code style issues, but they have basic type checking rules or plugins (e.g., Pylint can catch some obvious type errors, though it's not as comprehensive as a dedicated type checker).
- **Pyre:** A type checker from Facebook (written in OCaml).
  It's also fast and aimed at large applications.
  Its usage is less widespread in the community compared to mypy/pyright, but it's an alternative.
- **Typeguard, Enforce, etc.:** These are runtime type checking helpers.
  For example, `typeguard` is a library that can be used to enforce type hints at runtime by wrapping functions (so if someone calls `func("hello")` when it expects an int, it will raise an error at call time).
  These can be useful in specific scenarios, but generally static checkers are more common in Python since runtime checks negate some of the performance benefits of dynamic typing.

As an example of using a type checker, imagine we save the earlier `add` function example in a file and run a checker:

```python
# example_11.py
from book_utils import Catch


def add(a: int, b: int) -> int:
    return a + b


print(add(10, 5))
## 15
with Catch():
    # Second arg is not an int:
    add(10, "5")  # type: ignore
## Error: unsupported operand type(s) for +: 'int'
## and 'str'
```

If we run mypy on this file, we might get an output like:

```text
error: Argument 2 to "add" has incompatible type "str"; expected "int"
Found 1 error in 1 file (checked 1 source file)
```

This tells us exactly what and where the problem is.
We can then fix the code (e.g., by converting `"5"` to an integer, or by correcting the input).

The use of these tools ties back to the earlier benefits.
By acting as an automated guardrail, they produce overall code quality improvement through:

- maintainability
- readability
- safety
- early error detection
- enhanced tooling support
- better documentation

## Runtime vs. Static Type Checking

Let's clearly distinguish between runtime type checking and static type checking, because this is crucial to understanding Python's type system:

- **Runtime Type Checking:** This is what Python does natively.
  The interpreter checks types on the fly as operations are executed.
  If you try to do something invalid (like call a method that doesn't exist or use an operator on incompatible types), Python will raise an error at that moment.
  For example, if you do `3 + "3"`, Python immediately raises a `TypeError` when it hits that line, because it finds an integer and a string and doesn't know how to add them.
  Another example: calling `quacks(42)` in the earlier duck typing example raised an `AttributeError` at runtime, because 42 didn't have the required method.
  Runtime type checking is built into the language's operations.
  When you do something with an object, the object's type (or more precisely, its capabilities) determines what happens.
  Python will never silently do the wrong thing with a wrong type; it will error out (that's part of being strongly typed).
  But the key is, these errors happen during execution.

- **Static Type Checking:** This does not happen by default in Python--it's something you opt into by writing type annotations and using external tools.
  Static checking means examining the code without running it and ensuring that, according to the type hints and language rules, the operations make sense.
  It's like a dry run of the program in terms of types.
  If you say a function returns an `int` but you return a `str` somewhere, a static checker can catch that.
  If you pass the wrong type to a function, it's caught before running.
  This is what mypy, pyright, etc., do.
  They look at your code as data, not as a running program.
  The Python interpreter itself does not do static analysis--it doesn't look at annotations and refuses to run the program.
  You (or your development environment) have to invoke a tool to get static checking.
  This is why we call Python's type system "gradual" or "optional static typing"--the static part is bolted on by tools, not enforced by the language runtime.

One consequence of this design is that you can have a program that passes all static type checks but still crashes or behaves incorrectly at runtime if you made an assumption that wasn't guaranteed by the language.
Conversely, you might have a program that does something tricky that the static checker flags as a possible type issue, but at runtime it never fails because of the particular way you use it.
In those cases, you can often adjust your type hints or use casts/`# type: ignore` comments to tell the checker "trust me, I know what I'm doing here."
This disconnect between static analysis and actual running code is something to be aware of--it's the price of keeping the type system optional.
A quote from Python's documentation highlights this separation: \_"The Python runtime does not enforce function and variable type annotations.
They can be used by third party tools such as type checkers, IDEs, linters, etc."
In other words, if you want enforcement of those annotations, you need to use a tool (or implement your own checks).

Consider:

```python
# example_12.py
def f(x: int) -> int:
    return x * 2


print(f(5))  # Correct type
## 10
# Expected type 'int', got 'str' instead:
print(f("hi"))  # type: ignore
## hihi
# Strings can be "multiplied"
```

This example is a bit tricky--Python will not error on `f("hi")` because `"hi" * 2` in Python is valid (it repeats the string, resulting in `"hihi"`).
So our type annotation said `x` should be an int, but we passed a str, and Python didn't crash--it did something that perhaps we did not intend.
A static type checker would have warned us that `f("hi")` is not consistent with the annotation.
If this were a bug (say we truly only wanted numbers there), the static check catches it, whereas at runtime Python happily did something else.
If we had a case where passing a wrong type would crash (e.g., `f(None)` fails since `None * 2` is invalid), a static checker warns you.

Static type checks are a complement to Python's dynamic checks.
The dynamic runtime checks will catch issues when the code runs, but you want to catch as many issues as possible earlier.
Static typing tools help find mistakes without having to run every possible code path.

## The Benefits of Types

A type is a fundamental attribute of data that constrains what you can do with that data.
Python's is dynamically typed, meaning you don't have to declare types and can freely mix and change them at runtime.
This provides a lot of power and agility at the cost of potential runtime type errors.
Python emphasizes duck typing, relying on the actual capabilities of objects rather than explicit type declarations, which makes code very flexible and reusable.

Type annotations provide the best of both worlds: dynamic behavior plus tools to catch mistakes early.
Type hints improve code clarity and maintainability and act as a safety net, catching errors while coding.
This can dramatically increase confidence in code, especially as codebases grow.

The type system is there to help developers, not to make the language strict or verbose by force.
You can adopt it gradually and use it to the degree that it adds value for your projects.

Embracing Python's type system--both its dynamic nature and its optional static features--will make you a more effective Python programmer, writing code that is clear, correct, and robust.

## References

1. [Data type - Wikipedia](https://en.wikipedia.org/wiki/Data_type)
2. [Comparison of programming languages by type system--Wikipedia](https://en.wikipedia.org/wiki/Comparison_of_programming_languages_by_type_system)
3. [Precision Python](https://dzone.com/articles/typing-in-python)
4. [Static vs. Dynamic Typing: Pros, Cons, and Key Differences](https://www.netguru.com/blog/static-vs-dynamic-typing)
5. [Python's "Type Hints" are a bit of a disappointment to me](https://www.uninformativ.de/blog/postings/2022-04-21/0/POSTING-en.html)
6. [Duck Typing in Python: Writing Flexible and Decoupled Code--Real Python](https://realpython.com/duck-typing-python/)
7. [PEP 484](https://peps.python.org/pep-0484/)
8. [What Are Python Type-Hints and How to Use Them?--Andres Berejnoi](https://medium.com/@andresberejnoi/what-are-python-type-hints-and-how-to-use-them-andres-berejnoi-31835b92b038)
9. [mypy--Optional Static Typing for Python](https://mypy-lang.org/)
10. [microsoft/pyright: Static Type Checker for Python--GitHub](https://github.com/microsoft/pyright)
11. [Statically type checking Python code using Pyright--DEV Community](https://dev.to/saranshk/statically-type-checking-python-code-using-pyright-2p6p)
