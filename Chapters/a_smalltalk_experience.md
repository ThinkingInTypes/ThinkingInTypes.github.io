## Smalltalk in Python

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

### The Base Object

We start with a basic object that handles unknown messages by implementing `not_found`, similar to how Smalltalk does it.

```python
# smalltalk_object.py
class SmalltalkObject:
    def __getattr__(self, name):
        def handler(*args, **kwargs):
            return self.not_found(name, *args, **kwargs)

        return handler

    def not_found(self, message, *args, **kwargs):
        print(f"{self.__class__.__name__}: '{message}' not found")
```

When you say `obj.some_attr`, Python (internally) runs `type(obj).__getattribute__(obj, "some_attr")`.
If that fails with `AttributeError`, _and_ you've defined __getattr__, Python calls `obj.__getattr__("some_attr")`.

So for `SmalltalkObject`, when you access a missing method:

```python
# missing_method.py
from smalltalk_object import SmalltalkObject

obj = SmalltalkObject()
obj.dance()
```

Python can't find the method `dance`, so it calls `obj.__getattr__("dance")` which returns a function `handler(...)`.
Calling `obj.dance()` now runs `handler(...)`, which calls `self.not_found("dance", ...)`

### Create a blank chatbot

Here's a simple `Chatbot` class that doesn't yet respond to anything:

```python
# chatbot.py
from smalltalk_object import SmalltalkObject


class Chatbot(SmalltalkObject):
    def init(self):
        self.history = []
```

If we send the `hello()` message to the `Chatbot`, it doesn't understand it:

```python
# talk_to_chatbot.py
from chatbot import Chatbot

bot = Chatbot()
bot.hello()
```

It uses `__getattr__` to search for `hello()` which it doesn't find, so it falls back to `not_found`.

### Teach it to say hello

```python
# add_hello.py
from chatbot import Chatbot


def hello(self):
    print("Hello! I'm your chatbot.")
    self.history.append("hello")


setattr(Chatbot, "hello", hello)
bot.hello()
```

We added this method at runtime.
No compilation step--just live system growth.

### Step 5: Make it remember unknown messages

We override the default `not_found` with a new version that appends unknown messages to its `history`.

```python
# override_not_found.py
from chatbot import Chatbot


def not_found(self, message, *args, **kwargs):
    print(f"Sorry, I don't understand '{message}', but I'll remember it.")
    self.history.append(message)


setattr(Chatbot, "not_found", not_found)

bot.weather()
bot.joke()
```

The chatbot learns from what it hears.

### Step 6: Teach it a joke

```python
# learn_joke.py
from chatbot import Chatbot


def joke(self):
    print("Why did the duck cross the road? It was the chicken's day off.")
    self.history.append("joke")


setattr(Chatbot, "joke", joke)
bot.joke()
```

Again, we add behavior dynamically.

### Step 7: Inspect its capabilities

# Messages it understands:

```python
# introspection.py
import add_hello
import override_not_found
import learn_joke

print([m for m in dir(bot) if not m.startswith("_")])
print(bot.history)
```

Just like a Smalltalk browser, we inspect our object's current interface and state.
