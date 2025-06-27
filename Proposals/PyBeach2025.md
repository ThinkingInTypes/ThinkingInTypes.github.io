Title: Types and Dataclasses and Enums, Oh My!

Blurb:
The Python type annotation system enables rapid system construction by seamlessly connecting classes and functions.
Mistakes are revealed the moment they happen, without extensive hand-coded testing to verify correctness.
Dataclasses and enums quickly generate custom types to produce clear, robust designs.
This example-based presentation shows you how to use types to design and build stubbornly resilient systems that immediately tell you when something is wrong.
Such systems can save significant time and money during development and maintenance.

Lengthy Description:

As libraries grow in quantity and power, more of our job becomes connecting the interfaces of pre-existing pieces.
With a dynamically typed language, you must unravel connection problems at runtime.
Python's type annotation system discovers problems *while you type your code*. They:

- Produce airtight connections to functions and methods
- Specify and validate acceptable values
- Quickly illuminate a significant class of problems without hand-coded tests
- Help you design code
- Show others what it does

Type annotations dramatically increase productivity and simplify your life.
All examples and explanations are available in a free online book (under development).

Dataclasses and Enums are tools for generating custom types.

1. Enum values can be any kind of object (not just integers), enabling elegant designs
2. Exhaustiveness checking with Enums
3. Dot completion in editing environments speeds development
4. Creating self-validating data classes

1. Discover problems sooner.
2. Eliminate duplicate validation checks and their associated maintenance.
3. Share custom type benefits across all functions that use those types.
4. Localize validation to a single point, making changes much easier.
5. Eliminate the need for techniques such as Design By Contract (DBC).
6. Enable more focused testing with finer granularity.
7. Clarify the meaning of your code.

This example-based presentation shows different approaches to creating custom types to produce clear and robust software.

1. Type-driven development for greater productivity.
2. A type is a set of values.
3. Type annotations provide both constraints and documentation.
4. The execution path problem: Why testing doesn't solve it.
5. Immediate feedback from your IDE.
6. Use constants for robust and debuggable code.
7. Make illegal states unrepresentable with custom types.
8. Types solve Design-By-Contract (DBC) problems.
9. Easier refactoring.
10. Runtime type checking for annotations.
11. Easier Rust conversion.
12. The Failure of type systems with "holes."

Outline:

- Intro (7 Min)
    - A type is a set of values, producing constraints, documentation, and dot-completion
    - Discovering problems while writing code rather than runtime
    - Built-in types are too broad for most needs; custom types narrow to only what you use
    - Tools to create custom types: Alias, NewType, Literals, Dataclasses, Enums
- Dataclasses (5 min)
    - Correctly generating class methods you'd otherwise do by hand
    - Why to prefer frozen dataclasses
- Enums (5 min)
    - A constrained set of instances
    - Exhaustiveness checking
    - Type values can be anything, not just integers, producing elegant designs
- A Robust Date Type (8 Min)
    - `dataclass MonthValue`
    - `Enum Month`
    - `dataclass Year`
    - `dataclass Day`
    - `dataclass Date`
    - The types make illegal states unrepresentable