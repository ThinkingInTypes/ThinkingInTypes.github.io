# Callables

> ChatGPT 4.5 generated this placeholder text.
> It will be significantly rewritten as the book is developed.
> You can add comments to either <https://bsky.app/bruceeckel> or [GitHub Issues](https://github.com/ThinkingInTypes/ThinkingInTypes.github.io/issues).

## Annotating Functions and Lambdas

Clearly annotating functions and lambda expressions improves readability and type safety:

### Function Annotations

```python
# example_1.py
def add(x: int, y: int) -> int:
    return x + y
```

### Lambda Annotations

Annotating lambdas directly isn't supported; however, annotations can be implied:

```python
# example_2.py
# ruff: noqa: E731
from typing import Callable

adder: Callable[[int, int], int] = lambda x, y: x + y  # type: ignore
```

This explicit approach ensures that lambda behavior is type-checked properly.

## Using `Callable` for Higher-Order Functions

The `Callable` type is essential for annotating functions that accept or return other functions:

```python
# example_3.py
from typing import Callable


def operate(
    a: int, b: int, func: Callable[[int, int], int]
) -> int:
    return func(a, b)


result = operate(5, 3, lambda x, y: x * y)  # returns 15
```

Using `Callable` clearly defines expected function signatures, enhancing maintainability and correctness.

## Advanced Function Annotations with Parameter Specifications

Introduced in Python 3.10, parameter specifications allow annotating decorators and generic functions while preserving original function signatures:

```python
# example_4.py
from typing import Callable


def logging_decorator[**P, R](
    func: Callable[P, R],
) -> Callable[P, R]:
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        print(
            f"Calling {func.__name__} with {args} and {kwargs}"
        )
        return func(*args, **kwargs)

    return wrapper


@logging_decorator
def multiply(a: int, b: int) -> int:
    return a * b


multiply(2, 3)
## Calling multiply with (2, 3) and {}
```

Parameter specifications help decorators maintain accurate type information for wrapped functions.

## Implementing Function Overloading with `@overload`

Python allows specifying multiple function signatures through the `@overload` decorator for better static type checking:

```python
# example_5.py
from typing import overload


@overload
def double(value: int) -> int: ...


@overload
def double(value: str) -> str: ...


def double(value: int | str) -> int | str:
    if isinstance(value, int):
        return value * 2
    return value + value


print(double(4))  # Output: 8
## 8
print(double("Hi"))  # Output: HiHi
## HiHi
```

`@overload` clearly defines each acceptable signature, providing strong typing and preventing misuse.

## Annotation Strategies for APIs and Libraries

Clear annotations greatly enhance public API usability and reliability.
Strategies include:

### Explicit and Detailed Annotations

- Clearly annotate all public API interfaces and return types.
- Avoid overly broad types like `Any` unless necessary.

### Using Type Aliases for Complex Signatures

```python
# example_6.py
from typing import Callable, TypeAlias

RequestHandler: TypeAlias = Callable[[str, dict], dict]


def handle_request(path: str, handler: RequestHandler) -> dict:
    response = handler(path, {})
    return response
```

### Consistent Annotation Patterns

- Follow consistent patterns for similar methods or functions within an API.

### Leveraging Protocols and Callables

Using `Protocol` for clearly defined callable behaviors:

```python
# example_7.py
from typing import Protocol


class Handler(Protocol):
    def __call__(self, request: dict) -> dict: ...


def process_request(handler: Handler, request: dict) -> dict:
    return handler(request)
```

Following these strategies ensures type-safe, clear, and developer-friendly APIs and libraries.
