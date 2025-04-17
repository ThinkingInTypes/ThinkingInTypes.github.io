# Foundations

[Primarily notes at this point; I find that the introduction doesn't usually emerge until later in the book writing process]

## The Evolution of Complex Systems

Starting with assembly language.
Subroutines to save space, no intrinsic arguments and returns.
C was more than high-level assembly because it automated function arguments and returns.

"Goto Considered Harmful" and the transition to functions as independent packages of code.

Other code management developments: scoping in general, namespaces, exceptions.

### Object-Oriented Programming

User-defined types plus the huge distraction of inheritance.
GoF was so popular because it finally showed people what to _do_ with inheritance, although most cases were rather specialized solutions to non-mainstream problems.
Ultimately, inheritance creates more problems than solutions; it is occasionally helpful but usually not more than one level; deeper inheritance designs are challenging to use and maintain, and rarely provide enough benefits to justify their use.

Domain-Driven Design was an early step away from inheritance and towards types, but it has been a slow process.

Objects are useful as, to quote Stroustrup, "user-defined types," but as the GoF say in their introduction, "prefer composition to inheritance."
In this book, Python's Objects will be used as types and not base classes.
Anything that looks like inheritance will only be to create a type of something.
For example, the syntax of creating an enumeration looks like inheritance:

```python
# enumeration_definition.py
print("Can you inherit from an Enum?")
```

A NamedTuple is also defined in a way that looks like inheritance (other examples).

## The Wall We Keep Hitting

Putting small pieces together into larger pieces.
Sticking lumps of modeling clay together vs. assembling Legos.

## "Strong Typing vs. Strong Testing"

What is strong typing?

## Scalability

The Scala language: a research project into type systems.
Scala: "Scalability"
It seems like Python's type system is primarily inspired by Scala.
Scala leverages the JVM, which was a smart way to rapidly create an implementation of a language.
Being backwards compatible with Java, however, constrained Scala's design.
As strange as it sounds, Python doesn't have those constraints because its type system is optional.
Because of this optionality, Python's type system can effectively start from nothing and go anywhere it needs to, unhindered by the constraints of compatibility with an existing language.

## Who This Book Is For

Assumptions I make about your Python & programming knowledge.

### Your Python Knowledge

- You have intermediate-level understanding of the language, including a reasonable grasp of classes
- You understand core language features and know how to look up and learn features you haven't seen
- I will explain things I think are outside the core

### This book uses

- Version control with GitHub
- Project management with uv
- Testing with Pytest (noting that there are valid reasons to use other systems)
- Project organization (flat directory for examples distro)
- Standard tools for code consistency, such as `ruff`

### Programming Philosophy

- Build up from small testable pieces, balanced with simplicity and clarity.
- Use the most modern/elegant coding mechanisms available (latest Python)
- Classes are for creating types.
  As much as possible, pretend inheritance doesn't exist.
- Performance issues can be solved (sometimes by converting types or functions to Rust)
- Minimize Hungarian notation: a typed identifier name does not need to include the type information in its name.

### Examples

- Each example has a "slug line" which is the name of the file in a single-line comment as line one of the example.
- That example is in the GitHub repository in a subdirectory named for the chapter.
- The examples do not have `__main__`s; everything is at the top level.
- If a top-level-statement (TLS) produces output, that output will appear on the following line(s), commented with `##`.
- Lines to be called out in text are marked with comments
- Black for consistent formatting
- Listings 47 Characters wide: readable on a phone
