Title: Types and Dataclasses and Enums, Oh My!

Blurb:
The Python type system enables rapid system construction by seamlessly connecting classes and functions.
Mistakes are revealed the moment they happen, without extensive testing—testing that might not happen.
Combining this with the power of dataclasses and the flexibility of Enums produce clear, robust designs that are quickly implemented.
This example-based presentation shows you how to design and build stubbornly resilient systems that immediately tell you when something is wrong.
Such systems can save significant time and money during development and maintenance.

Lengthy Description:

1. Enum values can be any kind of object (not just ints), enabling
2. Exhaustiveness checking with Enums
3. Dot completion in editing environments speeds development

1. Discover problems sooner.
2. Eliminate duplicate validation checks and their associated maintenance.
3. Share custom type benefits across all functions that use those types.
4. Localize validation to a single point, making changes much easier.
5. Eliminate the need for techniques such as Design By Contract (DBC).
6. Enable more focused testing with finer granularity.
7. Clarify the meaning of your code.

As libraries grow in quantity and power, more of our job becomes connecting the interfaces of pre-existing pieces.
With a dynamically-typed language, you must unravel connection problems at runtime.
Python's type annotations discover problems *while you type your code*. They:

- Produce airtight connections to functions and methods
- Quickly illuminate a significant class of problems without requiring hand-coded testing.
- Help design your code
- Show others what it does

Type annotations dramatically increase productivity and simplify your life.

This example-based presentation covers:

1. Type-driven development for greater productivity.
2. A type is a set of values.
3. Type annotations provide both constraints and documentation.
4. The execution path problem: Why testing doesn't solve it.
5. Immediate feedback from your IDE.
6. Use constants for robust & debuggable code.
7. Make illegal states unrepresentable with custom types.
8. Types solve Design-By-Contract (DBC) problems.
9. Easier refactoring.
10. Runtime type checking for annotations.
11. Easier Rust conversion.
12. The Failure of type systems with "holes."

Outline:

- Intro (3 Min)
  - 
