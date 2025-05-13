# Appendix: Book Notes

Resources and Ideas for eventual inclusion in the book.

- Walrus operator?

---

- <https://github.com/BruceEckel/RethinkingObjects> (code from Pycon presentation, youtube video is not comprehensible)
- <https://github.com/BruceEckel/RethinkingObjects-book>

---

- reveal_type/assert_type

---

# AI-Generated Topic List

Created by ChatGPT 4o.

## 📘 Part I: The Basics of Typing in Python

### Introduction to Static Typing

- Why type your code?
- Benefits of types in Python (readability, tooling, correctness)

### Basic Type Annotations

- Built-in types:
  `int`, `str`, `float`, `bool`
- Variable annotations
- Function argument and return types

### Optional and Union Types

- `Optional[T]` / `T | None`
- `Union` / `T1 | T2`
- When and why to use

### Any and NoReturn

- When to use `Any`
- Risks of `Any`
- Meaning and use of `NoReturn`

### Type Aliases

- Creating and using `type MyAlias = ...`
- Organizing complex types

## 📘 Part II: Collections and Generics

### Typing Built-in Collections

- `List`, `Dict`, `Tuple`, `Set`
- Homogeneous vs heterogeneous types
- Variadic tuples

### Generic Types

- Understanding `TypeVar` and generic functions
- Creating generic classes

### Callable and Lambdas

- Typing functions as values
- Callable signatures

### Iterables and Iterators

- `Iterable`, `Iterator`, `Generator`
- Typing generators and coroutines

### Literal Types

- Restricting to fixed string or numeric values
- Using `Literal` for flags and enums

## 📘 Part III: Advanced Concepts

### Protocols and Structural Typing

- Introduction to duck typing
- `Protocol` classes and `@runtime_checkable`

### New in Python 10+

- `|` syntax for unions
- `match` statement and typing with pattern matching
- `ParamSpec` and `Concatenate`

### Annotated and Metadata Types

- Using `Annotated` for richer metadata
- Use in CLI tools, validation, etc.

### Self Type and Recursive Types

- Typing methods that return `self`
- Recursive types like nested JSON

### Dataclasses and Typing

- Typing fields with and without defaults
- `InitVar`, `field`, `kw_only`, etc.

## 📘 Part IV: Runtime Typing and Validation

### Type Checking at Runtime

- `isinstance` and `typing.get_type_hints()`
- Runtime enforcement libraries (e.g. Pydantic, Enforce)

### Validating with Decorators

- Type validation decorators
- Enforcing types in dynamic code

### TypedDict and JSON-like Structures

- Using `TypedDict` for structured data
- Migration from `dict[str, Any]`

### Enums and Custom Types

- Strongly typed enums
- Creating domain-specific types

### Dynamic Typing Interop

- Working with untyped or partially typed code
- Handling `Any` gracefully

## 📘 Part V: Tooling and Practices

### Static Type Checkers

- Using `mypy`, `pyright`, `pyre`, `pytype`
- Configuration and workflows

### IDE and Editor Support

- VS Code, PyCharm, etc.
- Type hinting with LSPs and plugins

### Refactoring with Types

- Incremental typing strategies
- Using types to guide refactoring

### Testing and Typing

- Typing test code
- Type-aware mocking and fixtures

### Types in Documentation

- Sphinx and autodoc with type hints
- Docstrings vs annotations

## 📘 Part VI: Real-World Applications

### Typing APIs and Libraries

- Public API surfaces
- Library development with types

### Using Types in Frameworks

- Django/Pydantic/FastAPI with typing
- Typing decorators and middleware

### Typing Concurrency

- `async def`, `Awaitable`, `Coroutine`
- `Thread`, `Process`, `Queue`

### Cross-Version Compatibility

- Using `typing_extensions`
- Supporting older Python versions

### Common Pitfalls and Anti-Patterns

- Misusing `Any`
- Over-annotating
- Annotations that hinder readability
