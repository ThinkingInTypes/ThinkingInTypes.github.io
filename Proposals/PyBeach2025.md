Title: Types and Dataclasses and Enums, Oh My!

Blurb:
Python type annotations enable rapid system construction by seamlessly connecting classes and functions.
Mistakes are revealed the moment they happen, without extensive hand-coded testing to verify correctness.
Dataclasses and enums quickly generate custom types to produce clear, robust designs.
This example-based presentation shows you how to use types to design and build stubbornly resilient systems that immediately tell you when something is wrong.
Such systems save significant time and money during development and maintenance.

Lengthy Description:

As libraries grow in quantity and power, more of our job becomes connecting the interfaces of pre-existing pieces.
With a dynamically typed language, you must unravel connection problems at runtime.
Python's type annotations discover problems *while you type your code*.
They:

- Produce airtight connections to functions and methods
- Specify and validate acceptable values
- Enable dot-completion
- Quickly detect a significant class of problems without hand-coded tests
- Help you design code
- Show others what it does

Dataclasses and Enumerations are tools for generating custom types.

**Dataclasses**

- Automatically create a constructor and standard class methods
- Can self-validate
- Can be immutable

**Enumerations**

- A constrained set of instances
- Enum values can be any kind of object (not just integers), enabling elegant designs
- Exhaustiveness checking with Enums

Type annotations dramatically increase productivity and simplify your life.

All examples and explanations are available in a free online book (under development).

1. Discover problems sooner.
2. Eliminate duplicate validation checks and their associated maintenance.
3. Share custom type benefits across all functions that use those types.
4. Localize validation to a single point, making changes much easier.
5. Eliminate the need for techniques such as Design By Contract (DBC).
6. Enable more focused testing with finer granularity.
7. Clarify the meaning of your code.

This example-based presentation shows different approaches to creating custom types to produce clear and robust software.

1. Type-driven development for greater productivity.
3. Type annotations provide both constraints and documentation.
5. Immediate feedback from your IDE.
7. Make illegal states unrepresentable with custom types.
9. Easier refactoring.

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