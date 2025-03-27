from typing import Callable, Generic, NamedTuple, ParamSpec, TypeVar

T = TypeVar("T")
P = ParamSpec("P")


class CaptureResult(NamedTuple, Generic[T]):
    result: T | None
    error: str | None = None

    def __str__(self) -> str:
        if self.error:
            return f"Error: {self.error}"
        return f"Result: {self.result!r}"


def capture(fn: Callable[P, T], *args: P.args, **kwargs: P.kwargs) -> CaptureResult[T]:
    """
    Safely call a function and return a CaptureResult containing either the result or an error message.
    """
    try:
        return CaptureResult(result=fn(*args, **kwargs))
    except Exception as e:
        return CaptureResult(result=None, error=str(e))


def risky_divide(a: int, b: int) -> float:
    return a / b


print(capture(risky_divide, 10, 2))
print(capture(risky_divide, 10, 0))
