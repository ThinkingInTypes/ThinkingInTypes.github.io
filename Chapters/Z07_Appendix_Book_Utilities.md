# Appendix: Book Utilities

These are incorporated into book examples to make them easier to read and to reduce code duplication.
They are placed in a subdirectory off the root of the project, named `book_utils`.
Because the book examples are extracted into a flat layout in the examples repository, you can import directly from `book_utils`.

## Exception Catcher

When a function call is known to succeed, the ordinary `print()` can be used.
If a function call can fail with an exception, `Catch` used as a context manager will catch and display the error.

```python
# book_utils/exception_catcher.py
"""
Context manager that catches exceptions and prints their error messages,
and can be used as a callable via its __call__ method.

When used as a callable, argument evaluation must be delayed until inside
the context manager in case argument evaluation raises an exception.
To do this the function should be provided as a zero-argument callable.
If the function takes arguments, it must be wrapped in a lambda to delay evaluation.
"""

from typing import Any, Callable, TypeVar

R = TypeVar("R")


class Catch:
    def __enter__(self) -> "Catch":
        return self

    def __exit__(
            self, exc_type: Any, exc_value: Any, traceback: Any
    ) -> bool:
        # Only called if an exception escapes the block.
        if exc_type is not None:
            print(f"Error: {exc_value}")
        return True

    def __call__(self, func: Callable[[], R]) -> R | None:
        """
        Execute a zero-argument callable, catching and
        printing errors so that subsequent calls run.
        """
        try:
            result = func()
            if result is not None:
                print(result)
            return result
        except Exception as e:
            print(f"Error: {e}")
            return None
```

The `Catch` class serves two roles:

1. **Context Manager** (`__enter__` and `__exit__` methods)
2. **Callable Object** (`__call__` method)

This combination allows it to handle exceptions and display meaningful error messages without stopping program execution.

### Context Manager

A context manager in Python is used with the `with` statement, typically to set up and tear down resources or to catch exceptions.
The `Catch` class implements this using:

- **`__enter__(self)`**\
  When the context is entered, it returns the instance (`self`), making the methods of the class accessible within the block.

- **`__exit__(self, exc_type, exc_value, traceback)`**\
  Automatically called when the context manager block (`with` statement) finishes execution.
  It receives details about any exception raised inside the block:

    - `exc_type`: the type of exception raised (e.g., `ValueError`)
    - `exc_value`: the actual exception object containing the message
    - `traceback`: the traceback object detailing where the exception occurred

  If an exception occurs (`exc_type is not None`), the `Catch` class prints the error message and returns `True` to indicate that the exception has been handled and should not propagate further.

Example usage as a context manager:

```python
# simple_form.py
from book_utils import Catch

with Catch():
    _ = 1 / 0
## Error: division by zero
```

### Callable Interface (`__call__` method)

The `Catch` class also defines a `__call__` method, allowing its instances to be called as functions.
This lets you explicitly wrap a callable (like a lambda or zero-argument function) inside its own try-except block, capturing and handling exceptions raised during both argument evaluation and function execution.

In the `__call__` method signature, `func` is a zero-argument callable.
It executes this callable within a try-except block:

- If the callable succeeds, it prints and returns the result (if not `None`).
- If an exception is raised, it prints the error and returns `None`.

Here's an example showing callables within a context manager:

```python
# simple_lambda_form.py
from book_utils import Catch

with Catch() as catch:
    catch(lambda: 1 / 0)
    catch(lambda: 1 / 0)
    catch(lambda: 1 / 0)
    print("No lambda aborts the context:")
    _ = 1 / 0
    print("This doesn't run:")
    catch(lambda: 1 / 0)
## Error: division by zero
## Error: division by zero
## Error: division by zero
## No lambda aborts the context:
## Error: division by zero
```

Using lambdas here is essential because it delays the evaluation of arguments until inside the `Catch` context, ensuring that errors raised during argument construction are caught properly.
Here's a more complex example with argument construction that throws exceptions:

```python
# demo_exception_checker.py
from dataclasses import dataclass

from book_utils import Catch


@dataclass
class Fob:
    x: int

    def __post_init__(self) -> None:
        if self.x < 0:
            raise ValueError(
                f"Fob arg {self.x} must be positive"
            )


def foo(a: int, b: Fob) -> str:
    if a < 0:
        raise ValueError(f"foo arg {a} must be positive")
    return f"foo({a}, {b}) succeeded"


# If you know it succeeds you can just run it without a context:
print(foo(0, Fob(0)))
## foo(0, Fob(x=0)) succeeded
with Catch():  # Single-failure form
    foo(1, Fob(-1))
## Error: Fob arg -1 must be positive

# In the form, success does NOT automatically display the result:
with Catch():
    print(foo(42, Fob(42)))  # Must explicitly print
## foo(42, Fob(x=42)) succeeded

# Lambda form displays successful result:
with Catch() as catch:
    catch(lambda: foo(42, Fob(42)))
## foo(42, Fob(x=42)) succeeded

# Multi-failure block requires lambda form:
with Catch() as catch:
    catch(lambda: foo(1, Fob(1)))
    catch(lambda: foo(0, Fob(0)))
    catch(lambda: foo(-1, Fob(1)))
    catch(lambda: foo(1, Fob(-1)))
    catch(lambda: foo(-1, Fob(-1)))
    catch(lambda: foo(10, Fob(11)))
## foo(1, Fob(x=1)) succeeded
## foo(0, Fob(x=0)) succeeded
## Error: foo arg -1 must be positive
## Error: Fob arg -1 must be positive
## Error: Fob arg -1 must be positive
## foo(10, Fob(x=11)) succeeded
```

## Book Utilities `__init__.py`

To allow these utilities to be easily imported using `from book_utils`, we must set up the `__init__.py`:

```python
# book_utils/__init__.py
from .exception_catcher import Catch

__all__ = ["Catch"]
```
