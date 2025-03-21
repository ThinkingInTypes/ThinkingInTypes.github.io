# Errors As Values

(Adapted from Pycon 2024 presentation <https://www.youtube.com/watch?v=4ANRgTDtuXk&ab_channel=PyConUS>)
<https://github.com/BruceEckel/functional_error_handling>

Error handling has had a messy history. Initially, programmers used languages close to hardware, such as assembly, or higher-level languages like COBOL or Fortran, where errors were typically presented as output from batch processing—a stack of punch cards passed to an operator, eventually returning error messages. Until interactive real-time operating systems became commonplace, software engineers didn't frequently consider the question, "How should we recover from an error?"

## Historical Context of Error Handling

Originally, the approach to handling errors was global—using global flags, setting signals, or similar global mechanisms. Unfortunately, this often resulted in race conditions, where one part of a program could easily overwrite an error indicator that another part needed to read. This made error handling an impediment to composability.

Initially, developers experimented with placing error handling responsibility in the operating system, alongside mechanisms like resumption. With resumption, you would register an error handler, potentially fix the issue in your handler, then resume execution right where the error occurred. Unfortunately, this approach failed and was eventually abandoned.

## Introducing Exceptions

The next step was moving error handling responsibility into the programming language itself. Languages introduced exceptions, providing a standardized error-reporting mechanism integrated closely with the program's domain logic. Exceptions addressed two main concerns:

- **Standardized error reporting**: Ensured consistent error notification across programs.
- **Enforced error visibility:** Exceptions generally couldn't be ignored as easily as global flags or signals.

Initially, exceptions seemed promising—especially in simple examples. But as we scaled applications and attempted deeper composability, problems emerged.

### Problems with Exceptions

**1. Exceptions aren't part of the type system.**  
With exceptions, a function call doesn't indicate clearly what kinds of errors it might raise. There's no compile-time notification if new exceptions emerge. Early attempts in languages like C++ and Java, which tried to include "exception specifications," failed. Java still retains its checked exceptions (often considered problematic by programmers), but C++ eventually deprecated them, shifting to approaches more aligned with functional error handling.

**2. Conflation of error categories.**  
Exceptions group recoverable errors (like transient database errors) together with unrecoverable "panic" conditions (like internal program logic errors). Treating both in the same way is confusing and leads to poor error handling practices.

**3. Exceptions discard partial calculations.**  
When an exception occurs within a large calculation (like a list comprehension), you lose all partial calculations made so far. This is inefficient and complicates debugging.

### A Functional Programming Approach

In functional programming, a more elegant solution has evolved: Instead of throwing exceptions, you return a structured type explicitly containing either a successful result or an error.

Initially, we might represent results as a type union (sum type). For example:

```python
# example_1.py
def calculate(value: int) -> int | str:
    if value == 1:
        return "Invalid argument"
    return value * 2
```

This works but isn't ideal, because we're overloading primitive types (like `int` and `str`) for error signaling, which isn't clear.

### Explicit Result Types with Data Classes

Instead, we create a custom `Result` type:

```python
# example_2.py
from dataclasses import dataclass
from typing import Generic, TypeVar

A = TypeVar('A')  # Successful result type
E = TypeVar('E')  # Error type

@dataclass(frozen=True)
class Result(Generic[A, E]):
    pass

@dataclass(frozen=True)
class Success(Result[A, E]):
    answer: A

    def unwrap(self) -> A:
        return self.answer

@dataclass(frozen=True)
class Failure(Result[A, E]):
    error: E
```

In this approach:

- If a function completes successfully, return a `Success(answer)`.
- If an error occurs, return a `Failure` object containing detailed error information.
- These two cases are distinct, clearly encoded by types.

Example usage:

```python
# example_3.py
def calculate(value: int) -> Result[int, str]:
    if value == 1:
        return Failure("Invalid argument")
    return Success(value * 2)
```

Using this approach with a sequence of calculations, you explicitly handle each result to determine success or failure, making error handling clearer and preventing partial results from getting lost.

### Composition with Functional Error Handling

With explicit `Result` types, we can elegantly compose functions, propagating errors easily:

```python
# example_4.py
result = calculate(value).bind(process).bind(next_step)
```

Each step checks internally: if the previous call returned a failure, subsequent calls are skipped, immediately propagating the failure outward. This style leads to robust, composable, and clear error handling.

### Leveraging Libraries

For a richer implementation, libraries such as Python's `returns` package streamline this functional error-handling pattern. The `returns` library provides decorators to transform regular functions into functions returning result types, handles exception catching cleanly, and includes helper methods such as `bind`.

An example using the `returns` library decorator:

```python
# example_5.py
from returns.result import Result, Success, Failure, safe

@safe
def divide(a: int, b: int) -> float:
    return a / b
```

Here, exceptions like division by zero are automatically captured, transformed into structured result objects.

### Composability in Action

Consider a scenario where several smaller functions combine into a larger workflow:

```python
# example_6.py
from returns.result import Result, Success, Failure

def func_a(val: int) -> Result[int, str]:
    if val == 1:
        return Failure("Cannot handle 1")
    return Success(val * 10)

def func_b(val: int) -> Result[int, str]:
    if val == 3:
        return Failure("Division by zero risk")
    return Success(val - 1)

def workflow(x: int) -> Result[int, str]:
    return calculate(x).bind(func_b).bind(func_c)
```

With this chaining pattern, errors propagate automatically. The first failure encountered halts further processing, immediately surfacing the error clearly to the caller, maintaining data integrity and simplifying debugging.

### Functional Error Handling in Other Languages

These patterns originated from functional languages, but increasingly influence modern mainstream languages:

- **Rust:** Built-in comprehensive result/error types (`Result`, `Option`).
- **Kotlin:** Lightweight built-in functional error handling.
- **C++:** Deprecated exception specifications and shifting towards return-value-based error handling.

Python, while historically leaning heavily on exceptions, can benefit greatly from adopting these functional-style techniques. Libraries like `returns` or `pydantic`, and the introduction of modern Python idioms (such as type annotations and dataclasses), facilitate safer, clearer, and more composable code.

### Conclusion

Shifting from exceptions towards structured error handling improves composability, readability, and robustness. This approach:

- Clearly defines possible error scenarios.
- Makes code composable and explicit about errors.
- Reduces complexity by removing hidden error states.
- Supports easier debugging and maintainability.

Embracing these functional principles can significantly improve your Python codebases, reducing unexpected errors and improving readability and clarity.
