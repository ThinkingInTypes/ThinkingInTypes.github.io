# Uncategorized Topics

These need to appear somewhere...

## `Annotated` for Metadata

Demonstration using Cyclopts

`Annotated` provides metadata for types, useful in documentation, validation, or frameworks:

```python
# example_2.py
from typing import Annotated

UserID = Annotated[int, "Database primary key"]


def fetch_user(user_id: UserID) -> dict:
    return {"id": user_id, "name": "Alice"}
```

Metadata within `Annotated` helps convey additional context beyond type hints.

## Type Narrowing

Perhaps a short chapter?

Type narrowing refines a variable's type within conditional checks:

### Using `isinstance`

```python
# example_4.py
from typing import Union


def process(value: Union[int, str]) -> None:
    if isinstance(value, int):
        print(value + 1)
    else:
        print(value.upper())
```

### Using assertions

```python
# example_5.py
from typing import Optional


def greet(name: Optional[str]) -> None:
    assert name is not None, "Name cannot be None"
    print(f"Hello, {name}")
```

Type narrowing helps write precise, safe, and understandable code.

## Type Guards (`isinstance`, custom type guards, assertions)

Custom type guards offer explicit ways to narrow types more clearly:

### Custom type guard functions (Python 3.10+)

```python
# example_6.py
from typing import TypeGuard


class Cat:
    def meow(self):
        print("Meow!")


def is_cat(animal: object) -> TypeGuard[Cat]:
    return hasattr(animal, "meow")


animal = Cat()
if is_cat(animal):
    animal.meow()  # Safe to call
## Meow!
```

Type guards enhance type narrowing accuracy, making code safer and cleaner.
