# Foundations

Assumptions I make about your Python & programming knowledge.

## Your Python Knowledge

- You have intermediate-level understanding of the language, including a reasonable grasp of classes
- You understand core language features and know how to look up and learn features you haven't seen
- I will explain things I think are outside the core

## This book uses

- Version control with GitHub
- Project management with uv
- Testing with Pytest (noting that there are valid reasons to use other systems)
- Project organization (src directory)

## Programming Philosophy

- Build up from small testable pieces, balanced with simplicity and clarity.
- Use the most modern/elegant coding mechanisms available (latest Python)
- Classes are for creating types.
  As much as possible, pretend inheritance doesn't exist.
- Performance issues can be solved (sometimes by converting types or functions to Rust)
- Minimize Hungarian notation: a typed identifier name does not need to include the type information in its name.

## Examples

- Each example has a "slug line" which is the name of the file in a single-line comment as line one of the example.
- That example is in the GitHub repository in a subdirectory named for the chapter.
- The examples do not have `__main__`s; everything is at the top level.
- If a top-level-statement (TLS) produces output, that output will appear on the following line(s), commented with `##`.
- Lines to be called out in text are marked with comments
- Black for consistent formatting
- Listings 47 Characters wide: readable on a phone
