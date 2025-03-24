# Make Illegal Types Unrepresentable

A common strategy for preventing problems is to check values after arguments are passed to functions.
This spreads validation code across functions, producing maintenance problems.
This chapter moves validation into custom types that make invalid data impossible.
In addition, data is checked when you create an instance, rather than when data is passed to a function.
With this approach, you:

1. Discover problems sooner.
2. Eliminate duplicate validation checks and their associated maintenance.
3. Share custom type benefits across all functions that use those types.
4. Localize validation to a single point, making changes much easier.
5. Eliminate the need for techniques such as Design By Contract (DBC).
6. Enable more focused testing with finer granularity.
7. Clarify the meaning of your code.

## "Stringly" Typed

Years ago I came across some research looking at the way generic components like `List`, `Set` and `Map` were being used in Java.
Only a tiny percentage of the code reviewed used anything *except* strings as type parameters.
