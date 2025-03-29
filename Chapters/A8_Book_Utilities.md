# Book Utilities

These are incorporated into book examples to make them easier to read and to reduce code duplication.
They are placed in a subdirectory off the root of the project, named `book_utils`.
Because the book examples are extracted into a flat layout in the examples repository, you can import directly from `book_utils`.

## Call and Print

When a function call is known to succeed, the ordinary `print()` can be used.
If a function call can fail with an exception, `call_and_print()` will catch and display the error.
In use, it is shortened to `cp` so it can also be used to make a code line a tiny bit shorter than `print()`.

```python
# book_utils/catch.py
from typing import Callable, ParamSpec, TypeVar

T = TypeVar("T")
P = ParamSpec("P")

def catch(fn: Callable[P, T], *args: P.args, **kwargs: P.kwargs) -> None:
    """
    Call a function and display either the result or the error message.
    """
    try:
        print(fn(*args, **kwargs))
    except Exception as e:
        print(f"Error: {e}")
```

The use of `ParamSpec` (`P`) captures the *actual* signature of the function `fn`.
That allows `*args` and `**kwargs` to match whatever positional and keyword argument types `fn` expects--even if they are mixed types.
`ParamSpec` produces variadic, type-preserving function calls.

```python
# book_utils/test_catch.py
from catch import catch

def test_catch() -> None:
    def risky_divide(a: int, b: int) -> float:
        return a / b
    catch(risky_divide, 10, 2)
    catch(risky_divide, 10, 0)
```

## Book Utilities `__init__.py`

```python
# book_utils/__init__.py
from .catch import catch
__all__ = ["catch"]
```
