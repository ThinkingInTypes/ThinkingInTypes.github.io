from typing import Callable, ParamSpec, TypeVar

T = TypeVar("T")
P = ParamSpec("P")


def capture(fn: Callable[P, T], *args: P.args, **kwargs: P.kwargs) -> T | None:
    """
    Call the given function and catch exceptions.
    Returns the function result, or None if an error occurs.
    """
    try:
        return fn(*args, **kwargs)
    except Exception as e:
        print(f"Error: {e}")
        return None


def risky_divide(a: int, b: int) -> float:
    return a / b


print(capture(risky_divide, 10, 2))  # → 5.0
print(capture(risky_divide, 10, 0))  # → Error: division by zero
# → None
