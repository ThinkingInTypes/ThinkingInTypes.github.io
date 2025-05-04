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
Smalltalk is strongly dynamically typed: every object's type is well-defined at runtime,
and objects do not change types arbitrarily, but the language does not check types until a message is actually sent.
Ultimately, whether Smalltalk can be said to have a "type system" in any meaningful sense depends on how one defines the term:
it certainly lacks compile-time type checking, yet it still categorizes and dispatches on types at runtime.
Meanwhile, languages like Java, Rust, and TypeScript use static type systems to rigidly define what can happen in a program, prioritizing
reliability and clarity over the dynamic extensibility that made Smalltalk so uniquely powerful.

Smalltalk is described as a reflective, object-oriented language known for its simplicity, dynamic nature,
and highly interactive development environment, treating everything as an object.
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
    known_phrases: set[str] = field(default_factory=set)

    def __getattr__(self, name: str):
        def handler(*args, **kwargs):
            return self.not_found(name, *args, **kwargs)

        return handler

    def not_found(self, message: str, *args, **kwargs):
        print(f"[Class] Parrot learns: {message}")

        def new_method(self, *args, **kwargs):
            print(f"Parrot says: {message}")
            self.known_phrases.add(message)

        setattr(self.__class__, message, new_method)
        return getattr(self, message)(*args, **kwargs)
```

The `__getattr__` method only runs if you try to access an attribute or method that doesn’t yet exist on either the instance or its class.
It captures the missing attribute `name`.
Then it returns a placeholder function `handler` that, when called, delegates to `self.not_found(...)`.

The `not_found` method teaches the parrot a new "method" on the fly and then immediately invokes it.
The `new_method` adds the phrase to that instance’s `known_phrases`.

The call to `setattr(self.__class__, message, new_method)` attaches `new_method` to the class.
Now all `Parrot` instances have a method with the name in the argument `message`.

Finally, `not_found` calls the new method in the `return` expression using `getattr`.

So, the first time you say `polly.hello()`, `__getattr__` catches the missing `hello`, returns `handler`, which calls `not_found("hello")`.
`not_found` prints that the class learned `"hello"`, then dynamically creates and installs `Parrot.hello`, adds `"hello"` to `polly.known_phrases`, and invokes `polly.hello()`.
For subsequent calls to `polly.hello()`, the method now exists on the class, so `__getattr__` is bypassed.
It simply prints "Parrot says: hello" and adds again to that instance’s list.

Other instances (e.g., `coco`) immediately gain a `hello` method, but their `known_phrases` remain separate: each instance tracks only the phrases it has ever spoken.

```python
# learning_parrot.py
from smalltalk_parrot import Parrot

polly = Parrot()
coco = Parrot()

# Before learning:
print(polly.known_phrases, coco.known_phrases)
## set() set()

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
## {'hello'} {'hello', 'squawk'}
```

Although `polly` and `coco` share each created method, each instance maintains its own `known_phrases` history.

## The Smalltalk Programming Experience

Smalltalk isn't just a language--it's a way of programming.
Rather than designing everything up front, Smalltalk encourages programmers to build systems interactively, incrementally, and dynamically.
The key ideas:

- Everything is an object.
- You send messages to objects, even if you don't know whether they understand them.
- Objects can learn new behaviors at runtime.
- The system evolves live as you work.

We'll simulate the Smalltalk programming experience using Python, so you can see what it feels like to develop in the Smalltalk style.
The entire session mirrors the experience of working in a Smalltalk image: there is no compile-run-edit loop.
You interact with objects directly, teach them behavior, and the system grows and adapts as you explore it.

We start with a basic object that handles unknown messages by implementing `not_found`, similar to how Smalltalk does it.

```python
# smalltalk_object.py
class SmalltalkObject:
    def __getattr__(self, name):
        def handler(*args, **kwargs):
            return self.not_found(name, *args, **kwargs)

        return handler

    def not_found(self, message, *args, **kwargs):
        print(
            f"{self.__class__.__name__}: '{message}' not found"
        )
```

When you say `obj.some_attr`, Python (internally) runs `type(obj).__getattribute__(obj, "some_attr")`.
If that fails with `AttributeError`, _and_ you've defined __getattr__, Python calls `obj.__getattr__("some_attr")`.

So for `SmalltalkObject`, when you access a missing method:

```python
# missing_method.py
from smalltalk_object import SmalltalkObject

obj = SmalltalkObject()
obj.dance()
## SmalltalkObject: 'dance' not found
```

Python can't find the method `dance`, so it calls `obj.__getattr__("dance")` which returns a function `handler(...)`.
Calling `obj.dance()` now runs `handler(...)`, which calls `self.not_found("dance", ...)`

### A blank chatbot

Here's a simple `Chatbot` class that doesn't yet respond to anything:

```python
# chatbot.py
from smalltalk_object import SmalltalkObject


class Chatbot(SmalltalkObject):
    def __init__(self):
        self.history = set()
```

If we send the `hello()` message to the `Chatbot`, it doesn't understand it:

```python
# talk_to_chatbot.py
from chatbot import Chatbot

bot = Chatbot()
bot.hello()
## Chatbot: 'hello' not found
```

It uses `__getattr__` to search for `hello()` which it doesn't find, so it falls back to `not_found`.

### Teach it to say hello

```python
# add_hello.py
from chatbot import Chatbot

bot = Chatbot()


def hello(self):
    print("Hello! I'm your chatbot.")
    self.history.add("hello")


setattr(Chatbot, "hello", hello)
bot.hello()
## Hello! I'm your chatbot.
```

We added this method at runtime.
No compilation step--just live system growth.

Now let's make it remember unknown messages by creating a new `not_found` that adds unknown messages to its `history`:

```python
# not_found_with_history.py


def not_found(self, message, *args, **kwargs):
    print(f"Don't know '{message}'; remembering it.")
    self.history.add(message)
```

We override the default `not_found` with our new version:

```python
# override_not_found.py
from chatbot import Chatbot
from not_found_with_history import not_found

bot = Chatbot()
setattr(Chatbot, "not_found", not_found)

bot.weather()
## Don't know 'weather'; remembering it.
bot.joke()
## Don't know 'joke'; remembering it.
```

The chatbot learns from what it hears.

### Teach it a joke

```python
# joke.py
def joke(self):
    print("Why did the duck cross the road?")
    print("It was the chicken's day off.")
    self.history.add("joke")
```

```python
# learn_joke.py
from chatbot import Chatbot
from joke import joke

bot = Chatbot()
setattr(Chatbot, "joke", joke)
bot.joke()
## Why did the duck cross the road?
## It was the chicken's day off.
```

Again, we add behavior dynamically.

### Inspect its capabilities

```python
# introspection.py
from add_hello import bot

## Hello! I'm your chatbot.
import override_not_found

## Don't know 'weather'; remembering it.
## Don't know 'joke'; remembering it.
import learn_joke
## Why did the duck cross the road?
## It was the chicken's day off.

print([m for m in dir(bot) if not m.startswith("_")])
## ['hello', 'history', 'joke', 'not_found']
print(bot.history)
## {'hello'}
```

Just like a Smalltalk browser, we inspect our object's current interface and state.
