# Errors as Values

> _Most of what we've been working towards in programming—whether we are aware of it or not—is composability._

Discovering the meaning of composability is part of this path--there are different definitions depending on the
programming language paradigm under scrutiny.
Here’s my definition:

> The ability to assemble bigger pieces from smaller pieces.

This is less precise than some definitions.
For example, composition in object-oriented programming means "putting objects inside other objects."
When dealing with functions, composability means "calling functions within other functions."
Both definitions fit my overall definition; they achieve the same goal but in different specific ways.

To enable the easy construction of programs, we need to be able to effortlessly assemble components in the same way that
a child assembles Legos—by sticking them together, without requiring extra activities.
On top of that, such assemblages become their own components that can be stuck together just as easily.
This composability scales up regardless of the size of the components.

Over the years, we have encountered numerous roadblocks to this goal.

## Goto Considered Harmful

[Dijkstra's 1968 note](https://homepages.cwi.nl/~storm/teaching/reader/Dijkstra68.pdf) had quite an impact on the
programming community,
which at the time consisted largely of assembly-language programmers.
For these, the goto statement was foundational, and denigrating it was a shock.
Although he never explicitly mentioned functions in his note, the effect was to push programmers towards functions.
[The creator of Structured Concurrency](https://vorpus.org/blog/notes-on-structured-concurrency-or-go-statement-considered-harmful/)
provides a clear description of this.

Rather than jumping about within a limited program, functions present the caller with a single entry and exit point.
This dramatically improves composability because you can no longer leave a section of code at any point using a goto.
Within a function scope you cannot know what’s outside that scope, thus you can’t jump somewhere because you don’t know
a destination to jump to.

My programming training was primarily as a computer engineer,
and I spent the first few years of my career programming in assembly.
Assembly supports subroutine calls and returns, but not the loading of arguments on the stack and passing results back
out—the programmer must write this error-prone code by hand.

Higher-level languages handle function arguments and returns for you, which made them a very desirable improvement as
the size and complexity of programs grew beyond what the assembly programmer was able to hold in their head.

## Modules

Tim Peters celebrated namespaces in [The Zen of Python](https://peps.python.org/pep-0020/).
This is the foundation for _modules_, found in more modern languages (for backwards compatibility, C++ was forced to use C’s messy system).
In Python, modules map nicely onto files.

It wasn’t always this way.
Breaking assembly-language programs into pieces was not easy, and early higher-level languages tended to be single-file
programs and did not consider modularity.
When the idea began to surface, it was incorporated as a main feature of the Modula-2 language (a descendant of Pascal).
The name tells you what a significant shift it was considered at the time.

Modula-2 and similar languages required an explicit declaration of a module:

```modula-2
MODULE Hello;
FROM STextIO IMPORT WriteString;
BEGIN
  WriteString("Hello World!")
END Hello.
```

This allowed complete granularity independent of file organization; perhaps this was because programmers were used to
thinking in terms of one big file-per-program.
Merging modules with files in Python makes more sense in hindsight and has the benefit of eliminating
the [(significant) extra verbiage](https://en.wikipedia.org/wiki/Modula-2), of which you only see a portion here.

The main benefit of modules is name control.
Each module creates a scope for names (a namespace) which allows programmers the freedom to choose any name at will within a module.
This prevents name collisions across a project and reduces the cognitive load on the programmer.
Prior to this, programs reached scaling limits as they grew larger.
Program size in assembly language programs was limited by many different factors, so the need for modules was not seen
until systems were able to grow larger because higher-level languages solved enough of these other factors.

In modern languages, modularity is part of the background of a language, and we can ignore it except when it reports errors.
At one time, however, the lack of modularity was a significant roadblock to code composability.

## Inheritance

Object-oriented programming has a bit of a tortured history.
Although the first OO language was Simula-67 (a compiled language), OO found its first real success with Smalltalk.
But Smalltalk might be the most dynamic language you’ll ever encounter—literally everything is evaluated at runtime.
This worked well for the kinds of problems Smalltalk was good at solving.
However, taking the ideas of Smalltalk and imprinting them into a statically typed language lost a _lot_ in translation.

## Error Handling

Error reporting and handling have been a significant impediment to composability.

### History

Original programs were small by present-day standards.
They were written in assembly language (machine code quickly became too unwieldy), and tightly coupled to the underlying hardware.
If something went wrong, the only way to report it was to change the output on a wire, to turn on a light or a buzzer.
If you had one, you put a message on the console, which might be a dot-matrix display.
Such an error message probably wasn’t friendly to the end-user of the system and usually required a tech support call to the manufacturer.

Two of my first jobs were building embedded systems that controlled hardware.
These systems had to work right.
There was no point in reporting most errors because an error normally meant the software was broken.

For business and scientific programming, Fortran and Cobol were batch processed on punch cards.
If something went wrong, either the compilation failed or the resulting data was bad.
No real-time error-handling was necessary because the program didn’t run in real time.

As time-sharing operating systems like Unix became a common way to distribute computing resources, program execution
became more immediate.
Users began to expect more interactive experiences, so programmers had to begin thinking about how to report and handle
errors during the execution of a program, and in ideal cases recovering from those errors so the program could continue
without shutting down.

Programmers produced a scattered collection of solutions to the reporting problem:

- Indicate failure by returning a special value from a function call.
  This only works when the special value doesn't occur from an ordinary call to that function.
  For example, if your function returns any `int`, you can't use `0` or `-1` to report an error.
  A bigger problem is that you rely on the client programmer to pay attention to the return value and know what to do
  about errors.

- Indicate failure by [setting a global flag](https://en.wikipedia.org/wiki/Errno.h).
  This is a single flag shared by all functions in the program.
  The client programmer must know to watch that flag.
  If the flag isn't checked right away, it might get overwritten by a different function call,
  in which case the error is lost.

- Use [signals](https://en.wikipedia.org/wiki/C_signal_handling) if the operating system supports it.

The operating system needed to be discovered.
Programmers found themselves rewriting the same basic code over and over again.
Much of that repeated code involved manipulating hardware.
It became clear that we needed a layer to eliminate this extra work--work that virtually all programs required.

A fundamental question that designers were trying to understand during this evolution was:

> _Who is responsible for error handling, the OS or the language?_

Since every program has the potential for errors, it initially seemed obvious that this activity should be the domain of
the operating system.
Some early operating systems allowed the program to invoke an error which would then jump to the operating system.
A few OSes even experimented with the ability to "resume" back to the point where the error occurred, so the handler
could fix the problem and continue processing.
Notably, these systems did not find success and resumption was removed.

Further experiments eventually made it clear that the language needed primary responsibility for error reporting and
handling (there are a few special cases, such as out-of-memory errors, which must still be handled by the OS).
This is because an OS is designed to be general purpose and thus cannot know the specific situation that caused an
error, whereas language code can be close to the problem.
Customization is normally the domain of the language.
You could imagine calling the OS to install custom error-handling routines, and you can also imagine how quickly that
would become overwhelmingly messy.

If errors are in the language domain, the next question is how to report and handle them.

## Exceptions

Unifying error reporting and recovery

There were different language implementations of exceptions:

- Lisp (was this the origin of language-based exceptions?).
  Possibly ironic as Lisp is the first functional language.
- BASIC had "On Error Go To" (and "resume"?)
- Pascal
- C++
- Java created checked exceptions, which must be explicitly dealt with in your code, and runtime exceptions, which could
  be ignored.
- Python has exceptions but doesn’t provide any type annotation or other mechanism to indicate what exceptions might
  emerge from a function call.

Exceptions seemed like a great idea:

1. A standardized way to correct problems so that an operation can recover and retry.
2. There's only one way to report errors.
3. Errors cannot be ignored—they flow upward until caught or displayed on the console with program termination.
4. Errors can be handled close to the origin or generalized by catching them "further out" so that multiple error
   sources can be managed with a single handler.
5. Exception hierarchies allow more general exception handlers to handle multiple exception subtypes.

To be clear, exceptions were a big improvement over all the previous (non) solutions to the error reporting problem.
Exceptions moved us forward for a while (and became entrenched in programming culture)
until folks started discovering pain points.
As is often the case, this happened as we tried to scale up to create larger and more complex systems.
And once again, the underlying issue was composability.

## Problems with Exceptions

In the small (and especially when teaching them), exceptions seem to work quite well.
It's hard to prove during language design; things work in the small but don't scale.
We only figure it out when scaling composability.

### 1. The Two Kinds of Errors are Conflated

Recoverable vs. panic (Recovering/Retrying requires programming) With exceptions, the two types are conflated.
One of the best explanations of this is by [Joe Duffy](https://joeduffyblog.com/2016/02/07/the-error-model/).

### 2. Not Part of the Type System

If the type system doesn’t include exceptions as part of a function signature, you can’t know what exceptions you must
handle when calling other functions (i.e.:
composing).
Even if you track down all the possible exceptions thrown explicitly in the code (by hunting for them in their source
code!), built-in exceptions can still happen without evidence in the code:
divide-by-zero is a great example of this.

You can be using a library and handling all the exceptions from it (or perhaps just the ones you found in the
documentation), and a newer version of that library can quietly add a new exception, and suddenly you are no longer
detecting and/or handling all the exceptions.
Even though you made no changes to your code.

Languages like C++ and Java attempted to solve this problem by adding _exception specifications,_ a notation that allows
you to add the exception types that may be thrown, as part of the function’s type signature.

Object-oriented languages that enforce exception specifications (C++, Java) and create exception hierarchies introduce
another problem.
Exception hierarchies allow the library programmer to use an exception base type in the exception specification.
This obscures important details; if the exception specification just uses a base type, there’s no way for the compiler
to enforce coverage of specific exceptions.

When errors are included in the type system, you can know all the errors that can occur just by looking at the type information.
If a library component adds a new error, then that must be reflected in that component’s type signature.
This means it no longer covers all error conditions and produces type errors until it is fixed.

### 3. Exception Specifications Create a "Shadow Type System"

Languages like C++ and Java attempted to add notation indicating the exceptions that might emerge from a function call.
This was well-intentioned and seems to produce the necessary information the client programmer needs to handle errors.
The fundamental problem was that this created an alternate or "shadow" type system that doesn’t follow the same rules as
the primary type system.
To make the shadow type system work, its rules were warped to the point where it became effectively useless (a discovery
that has taken years to realize).

C++ exception specifications were originally optional and not statically type-checked.
After many years these were deprecated in favor of the statically-typed [`expected` specification](https://en.cppreference.com/w/cpp/utility/expected) (which takes the functional approached
described in this chapter).

Java created checked exceptions, which must be explicitly dealt with in your code, and runtime exceptions, which could
be ignored.
Eventually, they added a feature that allows checked exceptions to be easily converted into runtime exceptions.
Java functions can always return `null` without any warning.

Both systems (the original C++ dynamic exception specifications and Java exception specifications) had too many holes,
and it was too difficult to effectively support both the main and shadow type systems.

### 4. Exceptions Destroy Partial Calculations

Let’s start with an example where we populate a `List` with the results from a sequence of calls to the function `fa`:

```python
# discarded_state.py
# Exception throws everything away
from book_utils import Catch


def fa(i: int) -> int:
    if i == 1:
        raise ValueError(f"fa({i})")
    return i


with Catch():
    result = [fa(i) for i in range(3)]
    print(result)
## Error: fa(1)
```

`fa` throws a `ValueError` if its argument is `1`.
The `range(3)` is 0, 1, and 2; only one of these values causes the exception.
So `result` contains only one problem; the other two values are fine.
However, we lose everything that we were calculating when the exception is thrown.
This:

1. Is computationally wasteful, especially with large calculations.
2. Makes debugging harder.
   It would be quite valuable to see in `result` the parts that succeeded and those that failed.

## The Functional Solution

Instead of creating a complex implementation to report and handle errors, the functional approach creates a "return
package" containing the answer along with the (potential) error information.
Instead of only returning the answer, we return this package from the function.

This package is a new type, with operations that prevent the programmer from plucking the result from the package
without dealing with error conditions (a failing of the Go language approach).

A first attempt uses _type unions_ to create a nameless return package:

```python
# return_union.py
# Type union aka Sum Type
# Success vs error is not clear


def fa(i: int) -> int | str:  # Sum type
    if i == 1:
        return f"fa({i})"
    return i


print(outputs := [(i, fa(i)) for i in range(5)])
## [(0, 0), (1, 'fa(1)'), (2, 2), (3, 3), (4,
## 4)]

for i, r in outputs:
    match r:
        case int(answer):
            print(f"{i}: {answer = }")
        case str(error):
            print(f"{i}: {error = }")
## 0: answer = 0
## 1: error = 'fa(1)'
## 2: answer = 2
## 3: answer = 3
## 4: answer = 4
```

`fa` returns a `str` to indicate an error, and an `int` answer if there is no error.
In the pattern match, we must check the result type to determine whether an error occurs; we cannot just assume it is an `int`.

An important problem with this approach is that it is not clear which type is the success value and which type
represents the error condition—because we are trying to repurpose existing built-in types to represent new meanings.

In hindsight, it might seem like this "return package" approach is much more obvious than the elaborate
exception-handling scheme that was adopted for C++, Java and other languages, but at the time the apparent overhead of
returning extra bytes seemed unacceptable (I don’t know of any comparisons between that and the overhead of
exception-handling mechanisms, but I do know that the goal of C++ exception handling is to have zero execution overhead
if no exceptions occur).

Note that in the definition of `composed`, the type checker requires that you return `int | str` because `fa`
returns those types.
Thus, when composing, type-safety is preserved.
This means you won’t lose error type information during composition, so composability automatically scales.

## Creating a New Return Type

We now have the unfortunate situation that `outputs` contains multiple types: both `int` and `str`.
The solution is to create a new type that unifies the "answer" and "error" types.
We’ll call this `Result` and define it using generics to make it universally applicable:

```python
# result.py
# Generic Result with Success & Failure subtypes
from dataclasses import dataclass


class Result[ANSWER, ERROR]:
    pass


@dataclass(frozen=True)
class Success[ANSWER, ERROR](Result[ANSWER, ERROR]):
    answer: ANSWER  # Usage: return Success(answer)

    def unwrap(self) -> ANSWER:
        return self.answer


@dataclass(frozen=True)
class Failure[ANSWER, ERROR](Result[ANSWER, ERROR]):
    error: ERROR  # Usage: return Failure(error)
```

Each subtype of `Result` only holds one field: `answer` for a successful `Success` calculation, and `error` for a `Failure`.
If a `Failure` is returned, the client programmer cannot reach in and grab the `answer` because that field doesn’t exist.
The client programmer must properly analyze the `Result`.

To use `Result`, you `return Success(answer)` when you’ve successfully created an answer,
and `return Failure(error)` to indicate a failure.
`unwrap` is a convenience method that is only available for a `Success`.

The modified version of the example using `Result` is now:

```python
# return_result.py
# Result type returns Success/Failure
# Using https://github.com/dry-python/returns
from returns.result import Failure, Result, Success


def fa(i: int) -> Result[int, str]:
    if i == 1:
        return Failure(f"fa({i})")
    return Success(i)
```

```python
# return_result_demo.py
from pprint import pprint
from return_result import fa

pprint([(i, fa(i)) for i in range(5)])
## [(0, <Success: 0>),
##  (1, <Failure: fa(1)>),
##  (2, <Success: 2>),
##  (3, <Success: 3>),
##  (4, <Success: 4>)]
```

Now `fa` returns a single type, `Result`.
The first type parameter to `Result` is the type returned by `Success` and the second type parameter is the type
returned by `Failure`.
The `outputs` from the comprehension are all of type `Result`, and we have preserved the successful calculations even
though there is a failing call.
We can also pattern-match on outputs; it is clear which is for success and failure.

The `returns` library has been slipped in here, but its basic form is that of `result.py`.

## Composing with `Result`

The previous examples included composition in the `composed` functions which just called a single other function.
What if you need to compose a more complex function from multiple other functions?
The `Result` type ensures that the `composed` function properly represents both the `Answer` type but also the various
different errors that can occur:

```python
# composing_functions.py
from pprint import pprint

from return_result import fa
from returns.result import (
    Failure,
    Result,
    Success,
    safe,
)


# Use an exception as info (but don't raise it):
def fb(i: int) -> Result[int, ValueError]:
    if i == 2:
        return Failure(ValueError(f"fb({i})"))
    return Success(i)


# Convert exception to Failure:
def fc(i: int) -> Result[int, ZeroDivisionError]:
    try:
        j = int(1 / (i - 3))
    except ZeroDivisionError as e:
        return Failure(ZeroDivisionError(f"fc({i}): {e}"))
    return Success(j)


@safe  # Convert existing function
def fd(
        i: int,
) -> str:  # Result[str, ZeroDivisionError]
    j = int(1 / i)
    return f"fd({i}): {j}"


def composed(
        i: int,
) -> Result[str, str | ValueError | ZeroDivisionError]:
    result_a = fa(i)
    if isinstance(result_a, Failure):
        return result_a  # type: ignore

    # unwrap() gets the answer from Success:
    result_b = fb(result_a.unwrap())
    if isinstance(result_b, Failure):
        return result_b  # type: ignore

    result_c = fc(result_b.unwrap())
    if isinstance(result_c, Failure):
        return result_c  # type: ignore

    return fd(result_c.unwrap())  # type: ignore
```

```python
# composing_functions_demo.py
from pprint import pprint
from composing_functions import composed

pprint([(i, composed(i)) for i in range(5)])
## [(0, <Failure: division by zero>),
##  (1, <Failure: fa(1)>),
##  (2, <Failure: fb(2)>),
##  (3, <Failure: fc(3): division by zero>),
##  (4, <Success: fd(1): 1>)]
```

The `fa`, `fb` and `fc` functions each have argument values that are unacceptable.
Notice that `fb` and `fc` both use built-in exception types as arguments to `Failure`, but those exceptions are never
raised—they are used to convey information, just like the `str` in `fa`.

In `composed`, we call `fa`, `fb` and `fc` in sequence.
After each call, we check to see if the result type is `Failure`.
If so, the calculation has failed.
We can’t continue, so we return a `Failure` object containing the reason for the failure.
Succeeding produces a `Success` containing an `unwrap` method used to extract the answer from that calculation.
It returns the `ANSWER` type so its use can be properly type-checked.

This means that any failure during a sequence of composed function calls will short-circuit out of `composed`,
returning a `Failure` that tells you exactly what happened.
You can’t ignore it and assume that it will "bubble up" until it finds an appropriate handler.
You must deal with it at the point of origin, the place where you typically know the most about an error.

## Simplifying Composition with `bind`

There’s still a problem that impedes our ultimate goal of composability:
every time you call a function within a composed function, you must write code to check the `Result` type and extract
the `answer` with `unwrap`.
This is extra repetitive work that interrupts the flow and readability of the program.
We need some way to reduce or eliminate the extra code.

Let's modify `Result` to add a new member function, `bind`:

```python
# result_with_bind.py
from __future__ import annotations

from dataclasses import dataclass
from typing import Callable


class Result[ANSWER, ERROR]:
    def bind(
            self, func: Callable[[ANSWER], Result]
    ) -> Result[ANSWER, ERROR]:
        if isinstance(self, Success):
            return func(self.unwrap())
        return self  # Pass the Failure forward


@dataclass(frozen=True)
class Success[ANSWER, ERROR]:
    answer: ANSWER

    def unwrap(self) -> ANSWER:
        return self.answer


@dataclass(frozen=True)
class Failure[ANSWER, ERROR]:
    error: ERROR
```

`bind` removes the duplicated code:

```python
# composing_with_bind.py
from pprint import pprint
from returns.result import Result

from composing_functions import fa, fb, fc, fd


def composed(
        i: int,
) -> Result[str, str | ZeroDivisionError | ValueError]:
    # fmt: off
    return (
        # TODO: typing is incorrect & needs fixing
        fa(i)
        .bind(fb)  # type: ignore
        .bind(fc)  # type: ignore
        .bind(fd)  # type: ignore
    )


pprint([(i, composed(i)) for i in range(5)])
## [(0, <Failure: division by zero>),
##  (1, <Failure: fa(1)>),
##  (2, <Failure: fb(2)>),
##  (3, <Failure: fc(3): division by zero>),
##  (4, <Success: fd(1): 1>)]
```

In `composed`, we call `fa(i)` which returns a `Result`.
The `bind` method is called on that `Result`, passing it the next function we want to call (`fb`) as an argument.
The return value of `bind` is _also_ a `Result`, so we can call `bind` again upon that `Result`, passing it the third
function we want to call (`fc`), and so on.

At each "chaining point" in `fa(i).bind(fb).bind(fc).bind(fd)`, `bind` checks the `Result` type to see
if it `Success`.
If so, it passes the result `answer` from that call as the argument to the next function in the chain.
If not, that means `self` is a `Failure` object (containing specific error information), so all it needs to do is
`return self`.
The next call in the chain sees that the returned type is `Failure`, so it doesn’t try to apply the next function but
just (again) returns the `Failure`.
Once you produce a `Failure`, no more function calls occur (that is, it short-circuits) and the `Failure` result gets
passed all the way out of the composed function so the caller can deal with that specific failure.

## Handling Multiple Arguments

We could continue adding features to our `Result` library until it becomes a complete solution.
However, others have worked on this problem, so it makes more sense to reuse their libraries.
The most popular Python library that includes this extra functionality
is [Returns](https://github.com/dry-python/returns).
`Returns` includes other features, but we will only focus on `Result`.

What if you need to create a `composed` function that takes multiple arguments?
For this, we use something called "do notation," which you access using `Result.do`:

```python
# multiple_arguments.py
from pprint import pprint

from composing_functions import fa, fb, fc
from returns.result import Result


def add(first: int, second: int, third: int) -> str:
    return f"add({first} + {second} + {third}): {first + second + third}"


def composed(
        i: int, j: int
) -> Result[str, str | ZeroDivisionError | ValueError]:
    # fmt: off
    return Result.do(
        add(first, second, third)
        for first in fa(i)
        for second in fb(j)
        for third in fc(i + j)
    )


inputs = [(1, 5), (7, 2), (2, 1), (7, 5)]
pprint([(args, composed(*args)) for args in inputs])
## [((1, 5), <Failure: fa(1)>),
##  ((7, 2), <Failure: fb(2)>),
##  ((2, 1), <Failure: fc(3): division by
## zero>),
##  ((7, 5), <Success: add(7 + 5 + 0): 12>)]
```

`Returns` provides a `@safe` decorator that you see applied to the "plain" function `fb`.
This changes the normal `int` return type into a `Result` that includes `int` for the `Success` type but is also somehow
able to recognize that the division might produce a `ZeroDivisionError` and include that in the `Failure` type.
In addition, `@safe` is apparently catching the exception and converting it to the `ZeroDivisionError` returned as the
information object in the `Failure` object.
`@safe` is a helpful tool when converting exception-throwing code into error-returning code.

`fc` adds some variety by rejecting `-1` and producing a `str` result.
We can now produce `composed` using a `pipe` and `bind`.
All the previous error-checking and short-circuiting behaviors happen as before, but the syntax is now more
straightforward and readable.

Notice that when the `outputs` list is created, the output from `reject0` only happens for the values `-1` and `2`,
because the other values cause errors in the `composed` chain of operations.
The value `1` never gets to `fb` because it is intercepted by the prior `composed` call to `fa`.
The value `0` causes `fb` to produce a `ZeroDivisionError` when it tries to perform the division inside the `print`.

[Explain the rest of the example]

Note that there may be an issue with the `Returns` library: for proper type checking it requires using a MyPy extension.
So far I have been unable to get that extension to work (however, I have no experience with MyPy extensions).

## Functional Error Handling is Happening

Functional error handling has already appeared in languages like Rust, Kotlin, and recent versions of C++ support these
combined answer-error result types, with associated unpacking operations.
In these languages, errors become part of the type system, and it becomes difficult for an error to be lost.

Python has only been able to support functional error handling since the advent of typing and type checkers, and it
doesn’t provide any direct language or library constructs for this.
The benefits of better error handling and robust composability make it worth adopting a library like `Results`.
