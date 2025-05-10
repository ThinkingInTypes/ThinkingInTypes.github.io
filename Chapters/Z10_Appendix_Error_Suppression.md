# Appendix: Error Suppression

| Tool    | `# type: ignore`                                         |
|---------|----------------------------------------------------------|
| Mypy    | Fully supported; can specify codes like `[arg-type]`     |
| Pyright | Fully supported via PEP 484                              |
| Pyre    | Supported but prefers `# pyre-ignore`                    |
| Pytype  | Supported but prefers `# pytype: disable=...`            |
| Flake8  | Unsupported; Linter only, does not process type comments |
| Ruff    | Unsupported; Same as Flake8                              |

| Tool    | Custom Directive                                                          |
|---------|---------------------------------------------------------------------------|
| Pyright | `# pyright: ignore`: Allows granular control; can target error categories |
| Pyre    | `# pyre-ignore`: Suppresses one error line; can include code              |
| Pytype  | `# pytype: disable=`: Disables specific checks; re-enable with `enable=`  |

| Directive            | Tool   | Notes                                                      |
|----------------------|--------|------------------------------------------------------------|
| `# noqa`             | Flake8 | Suppresses all lint warnings on the line                   |
|                      | Ruff   | Fully compatible                                           |
| `# ruff: noqa`       | Ruff   | File-level suppression                                     |
| `# flake8: noqa`     | Flake8 | File-level suppression                                     |
| `# pylint: disable=` | Pylint | Pylint-specific suppression (not related to type checking) |

Python's static checkers (like Mypy or Pyright) and linters (like Flake8 or Ruff) respect special end-of-line comments that disable error reporting.
The most common is `# type: ignore`, which tells type checkers to ignore all type errors on that line.
For example:

```python
# example_1.py
from book_utils import Catch


def add(x: int, y: int) -> int:
    return x + y


# Without ignore, this produces a type error (int vs. str):
with Catch():
    result = add(5, "7")  # type: ignore
```

Here the `# type: ignore` comment silences the mismatch.
Mypy's documentation explicitly notes that you can add `# type: ignore` to silence the checker on a particular line.

Mypy (and other checkers) also allow a more precise form: you can write `# type: ignore[code]` to ignore only specific error codes on that line, preventing you from accidentally hiding other issues.
For example, `# type: ignore[attr-defined]` ignores just that one error.  
Pyright and other tools likewise recognize `# type: ignore`.
In Pyright you can also use tool-specific variants like `# pyright: ignore`, which we discuss below.

## `# noqa`

Flake8 and Ruff (and many linters) use the `# noqa` comment to suppress lint errors on a line.
By default `# noqa` with no code ignores all warnings on that line.
For example:

```python
# example_2.py
from math import *  # type: ignore  # noqa
```

Without `# noqa`, a linter like Flake8 would warn about the wildcard import.
You can also target specific rule codes.
For instance, to silence Flake8's error code `E731` ("do not assign lambda"), you can write:

```python
# example_3.py
square = lambda x: x * x  # noqa: E731
```

This line reports no `E731` error, but any other code issues would still be shown.
Ruff is mostly Flake8-compatible: it recognizes `# noqa` (and even a file-level `# flake8: noqa` or `# ruff: noqa` to disable the whole file).
In short, use `# noqa` to silence specific linter errors on a line (or none after the colon), and `# flake8: noqa` or `# ruff: noqa` at file top to skip an entire file.

## Combining Directives

Sometimes you need to silence both a type checker and a linter on one line.
In that case you can chain the comments.
For example, to please both Mypy and Ruff, do:

```python
# example_4.py
from book_utils import *  # type: ignore  # noqa
```

The order matters: put `# type: ignore` before `# noqa` (with at least two spaces) so each tool recognizes its part.
Mypy scans the line first and stops, then Ruff/Flake8 reads `# noqa`.
Without careful ordering, you might accidentally hide errors from one tool or the other.

## Tool-Specific Suppression Comments

Beyond `# type: ignore` and `# noqa`, some checkers support their own suppressors:

### Pyright

In addition to `# type: ignore`, Pyright supports `# pyright: ignore` to mute only Pyright's diagnostics.
You can even specify particular rule names.
For example:

```python
# example_5.py
foo: int = "123"  # pyright: ignore # noqa
bar: int = "123"  # pyright: ignore [reportGeneralTypeIssues] # type: ignore # noqa
```

The first comment silences all Pyright errors on that line, the second suppresses only the named category.
Pyright prefers its own `# pyright: ignore` (it validates rule names) to avoid over-suppressing compared to the blanket `# type: ignore`.

### Pyre

The Pyre type checker (by Facebook) uses `# pyre-ignore` and `# pyre-ignore-all-errors`.
A comment like `# pyre-ignore[CODE]` tells Pyre to skip that error on the line (you omit the code to ignore all Pyre errors on that line).
For example:

```python
# example_6.py
def f(x: int) -> str:
    return x  # type: ignore      # This mismatches return type
    # pyre-ignore-all-errors[7]  # ignore "incompatible return type" for file
```

Pyre's docs explain that `# pyre-ignore` means "there's an issue with the type checker or code… we have decided not to fix this".
You can also put `# pyre-ignore-all-errors` (optionally with codes) at the top of a file to silence types across the whole module.

### Pytype

Google's Pytype supports `# pytype: disable=ERROR` (and `# pytype: enable=ERROR`) to turn off specific checks.
For instance:

```python
# example_7.py
class Server:
    def accept(self):
        self.socket = object()  # imagine this is set in listen()
        return self.socket.recv()  # pytype: disable=attribute-error # type: ignore # noqa
```

Here we disable the "attribute-error" warning that `socket` might not have `recv` yet.
You can disable warnings per-line or even for the rest of the file by writing a `disable` comment on its own.
The Pytype guide notes that this is preferred over a generic `# type: ignore`, since it documents exactly which error is expected.

### Pylint

Although not a type checker, Pylint is a common static analyzer that uses comments like `# pylint: disable=no-member` to suppress its own messages.
(This is analogous to `noqa` for Pylint-specific checks.)  
If you use Pylint in a typed codebase, you can mix these with the other directives,
but be aware Pylint does not understand `# type: ignore` or `# noqa`--it only looks for its own annotations.

## Recommendations

### Prefer Specificity

Rather than blanket ignoring all errors, target a specific code or rule if possible.
Mypy recommends `# type: ignore[<code>]` over plain `# type: ignore` to avoid hiding unrelated problems.
Similarly, specify Flake8 codes after `# noqa:` (e.g. `# noqa: E731`) instead of
`# noqa` alone, so you don't accidentally silence other issues.
(Some teams even use plugins to forbid bare `# noqa` or `# type: ignore`.)

### Use Ignores Sparingly

Treat these comments as a last resort when you truly cannot fix the error (e.g.
missing stubs, dynamic patterns, legacy code).
Overuse can mask bugs.
Some linters can flag "unused" ignores or warn when an ignore comment covers no actual error
(e.g., Pyright's `reportUnnecessaryTypeIgnoreComment`).
It's good practice to document why you're ignoring: a short trailing comment can explain the rationale.

### Fix Code When Feasible

Often a better solution is to tweak the code or annotations.
For example, instead of ignoring a missing attribute, consider adding a proper type annotation or refactoring.
Tools like `typing.cast()` or the
`Optional` type can sometimes eliminate the need for an ignore.
Remember, `# type: ignore` essentially reverts that expression to type `Any`, so you lose static checks there.

### Note Tooling Differences

If your project uses multiple tools, be aware of interactions.
As shown above, ordering matters (`# type: ignore` then `# noqa`).
Check each tool's docs: Pyright (for instance) only recognizes `# pyright: ignore`, not Mypy's style, and vice versa.
Conversely, most type checkers do understand `# type: ignore` thanks to PEP 484.

Using targeted ignores, documenting them, and preferring code fixes keeps your codebase clean while silencing the "false positives" or acceptable warnings that inevitably arise in static analysis.