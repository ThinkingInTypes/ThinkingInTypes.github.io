# Dynamic Smalltalk vs. Static Typing

Smalltalk is extremely dynamic.
A Smalltalk program runs inside a live image of objects that can be modified during execution.
Every component of the system--classes, methods, even control structures--is an object that can be inspected
and altered at runtime.
This produces a highly interactive development experience--developers can change code and see the effects immediately without restarting.
New methods or classes can be added on the fly, and objects will respond to new messages accordingly.
This open-ended dynamism promising much greater developer productivity and innovation.
It made Smalltalk a pioneer in object-oriented design.

When C++ was originally created, its designers hoped that OOP developer productivity could be tied to the ideas of objects and inheritance,
and were _not_ essentially bound to the rest of Smalltalk's features and development environment.
What we very slowly discovered over subsequent decades is that the fluid and open object model that Smalltalk enjoys
cannot be replicated in statically typed languages.

In effect, Smalltalk has no type system in the way that we've come to think about that term.
One can send any message to any object, and the system will attempt to find a matching method on the object at runtime.
If none exists, it triggers a `doesNotUnderstand:` handler (which by default raises a runtime "message not understood" error).
The only way to know whether an object will understand a given message is to send the message and see if the object responds.

Python has a lot of the dynamic flexibility of Smalltalk but:

1. It has a compile phase--this is brief and simple compared to non-dynamic languages, but it does some basic checking before the program runs.
2. Python's data elements have types; they are not just an object that will accept any message.

Statically typed languages require that an object's type (its class, interface, or trait) explicitly declare all the methods it supports.
Any call to a nonexistent method is caught at compile time as a type error.
Statically typed languages trade away Smalltalk's on-the-fly flexibility for the guarantee that method calls won't go astray.
Thus, certain idioms common in Smalltalk (such as adding methods to objects at runtime or relying on duck typing)
are impractical or impossible to express in a statically typed language.

In Smalltalk, the set of messages an object can respond to essentially defines its type at that moment--but this "type" is not a formal, static annotation;
it's just the object's current behavior, which can even change as the program runs.
Two objects are effectively the same type if they handle the same messages, regardless of their class lineage or internal representation.
Smalltalk is strongly dynamically typed: every object's type is
well-defined at runtime and objects do not change types arbitrarily, but the language does not check types until a message is actually sent.
Ultimately, whether Smalltalk can be said to have a "type system" in any meaningful sense depends on how one defines the term:
it certainly lacks compile-time type checking, yet it still categorizes and dispatches on types at runtime.
Meanwhile, languages like Java, Rust, and TypeScript use static type systems to rigidly define what can happen in a program, prioritizing
reliability and clarity over the dynamic extensibility that made Smalltalk so uniquely powerful.

Smalltalk is described as a reflective, object-oriented language known for its simplicity, dynamic nature, and highly interactive development environment, treating everything as an object
and supporting live coding for great flexibility and interactivity.
Smalltalk was designed to be a highly dynamic language, allowing developers to manipulate and experiment with code in real-time.

Because Smalltalk doesn't have a static way to encode expectations (types), the
community invented TDD--writing tests--to catch errors; xUnit testing was prototyped in Smalltalk.

## Emulating Smalltalk in Python

Because Python is a dynamic language, it is possible to emulate Smalltalk's behavior.
`type()` is most commonly seen as a function that returns the type of its argument:

```python
# type_function.py
class Plumbus:
    pass


print(type(Plumbus()))
## <class '__main__.Plumbus'>
```

However, `type()` can also be a class constructor to dynamically create a new class: `type(name, bases, dict)`:

```python
# dynamic_class_creation.py

BaseAnimal = type(
    "BaseAnimal",  # name
    (object,),  # bases
    # class body (attributes/methods):
    {"speak": lambda self: print("Generic animal sound.")},
)

Cat = type(  # Subclassing
    "Cat",
    (BaseAnimal,),
    {"speak": lambda self: print("Meow!")},
)

feline = Cat()
feline.speak()  # type: ignore
## Meow!
```

Lambdas are used here for brevity; more typically you'll see function names placed in the class body `dict`.

We can also create a Smalltalk-like object that dynamically adapts to new messages:

```python
# smalltalk_parrot.py
from dataclasses import dataclass, field


@dataclass
class Parrot:
    known_phrases: list[str] = field(default_factory=list)

    def __getattr__(self, name: str):
        def handler(*args, **kwargs):
            return self.not_found(name, *args, **kwargs)

        return handler

    def not_found(self, message: str, *args, **kwargs):
        print(f"[Class] Parrot learns: {message}")

        def new_method(self, *args, **kwargs):
            print(f"Parrot says: {message}")
            self.known_phrases.append(message)

        setattr(self.__class__, message, new_method)
        return getattr(self, message)(*args, **kwargs)
```

The `__getattr__` method only runs if you try to access an attribute or method that doesn’t yet exist on either the instance or its class.
It captures the missing attribute `name`.
Then it returns a placeholder function `handler` that, when called, delegates to `self.not_found(...)`.

The `not_found` method teaches the parrot a new “method” on the fly and then immediately invokes it.
The `new_method` appends the phrase to that instance’s `known_phrases`.

The call to `setattr(self.__class__, message, new_method)` attaches `new_method` to the class.
Now all `Parrot` instances have a method with the name in the argument `message`.

Finally, `not_found` calls the new method in the `return` expression using `getattr`.

So, the first time you say `polly.hello()`, `__getattr__` catches the missing `hello`, returns `handler`, which calls `not_found("hello")`.
`not_found` prints that the class learned `"hello"`, then dynamically creates and installs `Parrot.hello`, appends `"hello"` to `polly.known_phrases`, and invokes `polly.hello()`.
For subsequent calls to `polly.hello()`, the method now exists on the class, so `__getattr__` is bypassed.
It simply prints “Parrot says: hello” and appends again to that instance’s list.

Other instances (e.g., `coco`) immediately gain a `hello` method, but their `known_phrases` remain separate: each instance tracks only the phrases it has ever spoken.

```python
# learning_parrot.py
from smalltalk_parrot import Parrot

polly = Parrot()
coco = Parrot()

# Before learning:
print(polly.known_phrases, coco.known_phrases)
## [] []

polly.hello()
## [Class] Parrot learns: hello
## Parrot says: hello
coco.hello()
## Parrot says: hello
coco.squawk()
## [Class] Parrot learns: squawk
## Parrot says: squawk

# After learning:
print(polly.known_phrases, coco.known_phrases)
## ['hello'] ['hello', 'squawk']
```

Although `polly` and `coco` share each created method, each instance maintains its own `known_phrases` history.