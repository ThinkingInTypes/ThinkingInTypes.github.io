# Make Illegal Types Unrepresentable

A common strategy for preventing problems is to check values after arguments are passed to functions.
This spreads validation code across functions, producing maintenance problems.
This chapter moves validation into custom types that make invalid data impossible.
In addition, data is checked when you create an instance, rather than when data is passed to a function.
With this approach, you:

1. Discover problems sooner.
1. Clarify the meaning of your code.
1. Share custom type benefits across all functions that use those types.
1. Eliminate duplicate validation checks and their associated maintenance.
1. Make changes easier by localizing validation to a single point.
1. Eliminate the need for techniques such as Design By Contract (DBC).
1. Enable more focused testing with finer granularity.

## "Stringly Typed"

Years ago I came across some research looking at the way generic components like `List`, `Set` and `Map` were being used in Java.
Only a tiny percentage of the code reviewed used anything *except* strings as type parameters.
This study suggested that the vast majority of systems were using strings as their primary data type.

Because you can put any characters in any format into a string, such "stringly typed" systems (an ironic play on "strongly typed") may be the worst of all possible worlds.
Unless it's actually text, classifying something as a string says virtually nothing about it.
When a function receives a string that is meant to represent a type, that function can assume precisely nothing about it.
Every such function must start from scratch and analyze that string to see if it conforms to what that function needs.

If you ever change the meaning of that stringly-typed item, you have a daunting job ahead of you: to look through every function that uses it and ensure that your change is reflected in the validations in every single function.

[[Stringly typed example, possibly telephone numbers]]

## Design by Contract

The argument-validation problem was observed by Bertrand Meyer and introduced as a core concept in his Eiffel programming language, described in the book *Object-Oriented Software Construction* (1988).
*Design By Contract* (DbC) tried to reduce errors by treating the interaction between software components as a formal agreement:

- Preconditions: What must be true before a function/method runs.
- Postconditions: What must be true after the function completes.
- Invariants: What must always be true about the object state.

Eiffel provided explicit keywords to make DbC a first-class citizen in the language:

| Keyword     | Purpose                |
|-------------|------------------------|
| `require`   | Preconditions          |
| `ensure`    | Postconditions         |
| `invariant` | Class-wide conditions  |
| `old`       | Refers to previous state in postconditions |

The idea was that each function you wrote would use these to ensure the correctness of the inputs and outputs of that function.
In particular, `require` typically checks the argument values for correctness.
For preconditions in Python, we can create a `requires` decorator to check argument values:

```python
# require.py
from typing import Callable, NamedTuple
from functools import wraps


class Condition(NamedTuple):
    check: Callable[..., bool]
    message: str


def requires(*conditions: Condition):
    def decorator(func: Callable):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for condition in conditions:
                if not condition.check(*args, **kwargs):
                    # Do something like this:
                    # raise ValueError(condition.message)
                    # We'll just:
                    print(condition.message)
            return func(*args, **kwargs)
        return wrapper
    return decorator
```

Now we can apply `require` to validate function arguments:

```python
# bank_account.py
from require import requires, Condition

POSITIVE_AMOUNT = Condition(
    check=lambda self, amount: amount > 0,
    message="Amount must be positive"
)

SUFFICIENT_BALANCE = Condition(
    check=lambda self, amount: self.balance >= amount,
    message="Insufficient balance"
)

class BankAccount:
    def __init__(self, balance: float):
        self.balance = balance

    @requires(POSITIVE_AMOUNT, SUFFICIENT_BALANCE)
    def withdraw(self, amount: float) -> None:
        self.balance -= amount
        print(f"Withdrew {amount}, new balance: {self.balance}")

    @requires(POSITIVE_AMOUNT)
    def deposit(self, amount: float) -> None:
        self.balance += amount
        print(f"Deposited {amount}, new balance: {self.balance}") 

account = BankAccount(100)
account.deposit(50)
account.withdraw(30)
account.withdraw(200)
account.deposit(-10) 
```

This is an improvement over placing the testing code at the beginning of each function, as Eiffel does and as traditional Python functions do--assuming they test their arguments.
The `@require` clearly shows that constraints have been placed on the arguments.
`Condition` reduces duplicated code.

DbC definitely helps, but it has limitations:

1. A programmer can forget to use `requires`, or simply choose to perform argument checks by hand if DbC doesn't make sense to them.
1. The tests are spread throughout your system. Using `Condition` centralizes the test logic but making changes still risks missing updates on functions.
