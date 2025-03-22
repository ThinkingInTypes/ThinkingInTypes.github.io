# Book Notes

Resources and Ideas for eventual inclusion in the book

- <https://github.com/BruceEckel/RethinkingObjects> (code from Pycon presentation, youtube video is not comprehensible)
- <https://github.com/BruceEckel/RethinkingObjects-book>
- Will probably need to consider Pydantic

## AI-Generated Topic List

Created by ChatGPT 4o.

### 📘 **Part I: The Basics of Typing in Python**

1. **Introduction to Static Typing**
   - Why type your code?
   - Benefits of types in Python (readability, tooling, correctness)

2. **Basic Type Annotations**
   - Built-in types: `int`, `str`, `float`, `bool`
   - Variable annotations
   - Function argument and return types

3. **Optional and Union Types**
   - `Optional[T]` / `T | None`
   - `Union` / `T1 | T2`
   - When and why to use

4. **Any and NoReturn**
   - When to use `Any`
   - Risks of `Any`
   - Meaning and use of `NoReturn`

5. **Type Aliases**
   - Creating and using `type MyAlias = ...`
   - Organizing complex types

### 📘 **Part II: Collections and Generics**

6. **Typing Built-in Collections**
   - `List`, `Dict`, `Tuple`, `Set`
   - Homogeneous vs heterogeneous types
   - Variadic tuples

7. **Generic Types**
   - Understanding `TypeVar` and generic functions
   - Creating generic classes

8. **Callable and Lambdas**
   - Typing functions as values
   - Callable signatures

9. **Iterables and Iterators**
   - `Iterable`, `Iterator`, `Generator`
   - Typing generators and coroutines

10. **Literal Types**
    - Restricting to fixed string or numeric values
    - Using `Literal` for flags and enums

### 📘 **Part III: Advanced Concepts**

11. **Protocols and Structural Typing**
    - Introduction to duck typing
    - `Protocol` classes and `@runtime_checkable`

12. **New in Python 3.10+**
    - `|` syntax for unions
    - `match` statement and typing with pattern matching
    - `ParamSpec` and `Concatenate`

13. **Annotated and Metadata Types**
    - Using `Annotated` for richer metadata
    - Use in CLI tools, validation, etc.

14. **Self Type and Recursive Types**
    - Typing methods that return `self`
    - Recursive types like nested JSON

15. **Dataclasses and Typing**
    - Typing fields with and without defaults
    - `InitVar`, `field`, `kw_only`, etc.

### 📘 **Part IV: Runtime Typing and Validation**

16. **Type Checking at Runtime**
    - `isinstance` and `typing.get_type_hints()`
    - Runtime enforcement libraries (e.g. Pydantic, Enforce)

17. **Validating with Decorators**
    - Type validation decorators
    - Enforcing types in dynamic code

18. **TypedDict and JSON-like Structures**
    - Using `TypedDict` for structured data
    - Migration from `dict[str, Any]`

19. **Enums and Custom Types**
    - Strongly typed enums
    - Creating domain-specific types

20. **Dynamic Typing Interop**
    - Working with untyped or partially typed code
    - Handling `Any` gracefully

### 📘 **Part V: Tooling and Practices**

21. **Static Type Checkers**
    - Using `mypy`, `pyright`, `pyre`, `pytype`
    - Configuration and workflows

22. **IDE and Editor Support**
    - VS Code, PyCharm, etc.
    - Type hinting with LSPs and plugins

23. **Refactoring with Types**
    - Incremental typing strategies
    - Using types to guide refactoring

24. **Testing and Typing**
    - Typing test code
    - Type-aware mocking and fixtures

25. **Types in Documentation**
    - Sphinx and autodoc with type hints
    - Docstrings vs annotations

### 📘 **Part VI: Real-World Applications**

26. **Typing APIs and Libraries**
    - Public API surfaces
    - Library development with types

27. **Using Types in Frameworks**
    - Django/Pydantic/FastAPI with typing
    - Typing decorators and middleware

28. **Typing Concurrency**
    - `async def`, `Awaitable`, `Coroutine`
    - `Thread`, `Process`, `Queue`

29. **Cross-Version Compatibility**
    - Using `typing_extensions`
    - Supporting older Python versions

30. **Common Pitfalls and Anti-Patterns**
    - Misusing `Any`
    - Over-annotating
    - Annotations that hinder readability
