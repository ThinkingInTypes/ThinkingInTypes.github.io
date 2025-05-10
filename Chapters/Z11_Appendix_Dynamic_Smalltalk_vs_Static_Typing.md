# Appendix: Dynamic Smalltalk vs. Static Typing

> **NOTE:** This material is being developed for one of the introductory chapters

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
and objects do not change types arbitrarily, but the language does not check types until a message is sent.
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

## Why Smalltalk OOP Didn't Become Statically Compiled OOP

### A Proof-of-Concept is not a Product

### The Dynamism of Smalltalk Can't be Tied Down

### Inheritance Forces you to Deal with the Base Class

You _must_ make your new class a "type of" the base class, and all that entails, including overriding methods you don't care about.
Your new class _belongs_ to the base class, but with composition, the member object belongs to your new class.
With composition, the object does what you want it to do, with inheritance, you must do what the base class wants you to do.

Arguably the only success story, Ruby, is a kind of Smalltalk.

## "Type" in Smalltalk: A Dynamic, Message--Driven Perspective

In Smalltalk, an object's identity and capabilities are not described by an explicit static type annotation.
Instead, an object is defined by the messages it can respond to.
In other words, an object's protocol--the collection of message selectors (methods) it understands--is effectively its "type."
You determine what an object can do by the messages you send it and how it responds, not by checking a formal static type label.

This message-centric view is fundamental to the Smalltalk experience.
All computation in Smalltalk is performed by sending messages to objects.
There are no free functions or primitive operations outside of this model--every operation is a message sent to some object.
The result of a message depends entirely on the receiver object: the same message selector might do something completely different on another object because each class provides its own method for that message.
This means the object itself decides how to fulfill a request,
reinforcing the idea that what matters is the object's behavior (its responses to messages), not an external static description.

### "Type" as an Emergent Set of Behaviors (Duck Typing)

Because there are no declared types on variables or method arguments in Smalltalk, the concept of "type" becomes an emergent property of an object's behavior.
A Smalltalk object's type can be thought of as "the set of messages to which an object can meaningfully respond."
In modern parlance, this is essentially duck typing--"if it walks like a duck and quacks like a duck, it's a duck."
Smalltalkers don't ask "Is this object of type Duck?"--there is no formal type check or interface to query.
Instead, they ask *"Can this object respond to the messages we associate with a duck (like `quack`or `swim`)?".
If yes, then for all intents and purposes, it can play the role of a duck in the program.
Different classes can implement the same set of messages, thereby effectively conforming to the same "duck type."
This gives Smalltalk tremendous flexibility and polymorphism--any object that implements the expected messages can be used in a given context, regardless of its class.

It's important to note that Smalltalk is not "weakly typed" or "untyped."
It is in fact strongly typed at runtime--if you send a message an object doesn't understand, the system will throw a runtime error rather than blindly misinterpreting it.
Strong typing only means type errors are prevented; it does not require that they be prevented at compile time.
Smalltalk enforces type safety dynamically: a `MessageNotUnderstood` error will halt a misuse, analogous to a type error in a static system, but occurring at runtime.
Thus, every object has a type in the sense of a well-defined set of messages/methods; what Smalltalk lacks is a static type checker to verify those at compile time.
A value's type is an intrinsic property of the object (determined by its class and methods) and not of the variable referencing it.
Any variable can refer to any object, so the "type" lives with the object, not the variable.
This is a form of optimistic typing--the system trusts the programmer to send appropriate messages and will dynamically prevent or flag errors if the trust is violated.

### *Handling the Unknown: `doesNotUnderstand:`

One fascinating aspect of Smalltalk's message-centric design is how it handles an unknown message.
If you send an object a message for which it has no defined method, the runtime doesn't immediately crash.
Instead, it sends a special message `doesNotUnderstand:` to that object, passing along a description of the original message.
By default, `Object>>doesNotUnderstand:` will raise a `MessageNotUnderstood` error (often opening a debugger in a Smalltalk IDE),
but critically, developers can override this method to change the behavior.
This means an object can be designed to gracefully handle any message at all, even ones not originally defined in its class's method dictionary.

For example, one could create a proxy object that intercepts all messages via `doesNotUnderstand:` and forwards them to another object,
or a stub that logs all unknown messages for testing.
In fact, Smalltalk was the first language to introduce this kind of open-ended message handling, and it unlocks a lot of power.
Using `doesNotUnderstand:`, programmers have implemented features like remote method invocation proxies,
lazy-loaded objects, futures, and other patterns that require catching arbitrary messages at runtime.
The existence of `doesNotUnderstand:` underscores that an object's "type" (its message-handling ability) isn't necessarily fixed by its class--it can be extended or altered at runtime in a very dynamic fashion.
Thanks to this mechanism, an object can respond to a message without considering when it was written.
From a philosophical view, this pushes the "duck typing" idea to the extreme: an object can choose to attempt anything asked of it,
defining its behavior on the fly.

The flip side is that you truly don't know if a given message will be handled until you send it.
In practice, Smalltalk programmers cope with this by testing and by building systems where the expectations are clear
(or by using the interactive tools to inspect an object's class/protocol).
But it does raise an interesting question: if the only way to know what an object can do is to try it
and see, can we really say the object "has a type" in the same sense as in a statically typed language?
The answer in Smalltalk is that type is a dynamic notion--it's something an object does, not something it declares.
The object's type manifests when a message is sent and successfully understood.
If it isn't, that's effectively a type mismatch, caught by the runtime (often during development in the live environment).

### Classes as Behavioral Templates, Not Compile-Time Constraints

Smalltalk is a class-based OO language, and every object is an instance of some class.
However, a class in Smalltalk is not a "type" in the static sense; it's more like a template that defines behavior and structure.
A class specifies which messages its instances will understand (by providing method implementations for those messages), and it defines the internal state structure.
Two different classes could end up implementing the same protocol (thus effectively the same behavioral
type), but they would still be distinct classes (perhaps with different internal representations).
The Smalltalk system doesn't have a separate notion of an interface or protocol type distinct from classes--classes are how you organize and advertise what messages exist.
But importantly, the system will never restrict you to using only a particular class in a given variable or call.
There's no static type checker insisting "this variable must contain an instance of class X."
The class is a property of the object itself, not a restriction on its use by others.

In the Smalltalk programmer's mind, classes serve as a useful guide and documentation of an object's capabilities, but not a rigid cage.
They provide a shared vocabulary of messages
for all instances of that class (and subclasses), which helps humans reason about what an object can do.
For example, if you have a `GraphicsShape` class with methods like `drawOn:`,
`area`, etc., you know any instance of that class (or its subclasses) will respond to those messages.
In day-to-day practice, a Smalltalk developer
does often think in terms of an object's class when reasoning about what messages it can handle--the class system is the primary organizational tool for behavior.
But this is a convention and convenience, not an enforcement mechanism.
You could always substitute an object of a completely different class in a piece of code, as long as it implements the needed messages.
The Smalltalk environment even allows adding methods to classes at runtime or creating entirely new classes on the fly,
which means the system's notion of who can respond to what is always malleable.
Classes thus shape an object's behavior, but they do not constitute a static contract imposed on the rest of the program.

It's illuminating to compare this with how statically typed languages use classes.
In a language like Java or C++, a class (or an interface) is treated as a type contract.
Programmers in those languages think of types as a form of guarantee or enforcement:
if a variable is declared of interface type `Drawable`,
the compiler guarantees it can only ever hold objects that implement the `draw()` method
(and will refuse to compile code that tries to call a non-existent method or assign an incompatible type).
Types in statically typed languages act
like promises enforced by the compiler--they delineate what you can and cannot do at compile time.
They also function as explicit documentation: you read a function signature and see exactly what types it accepts/returns, shaping your expectations.
Many developers in static systems conceptualize a type as a contractual
specification of an object's interface (sometimes even enriched with static checks for invariants, generics, etc., as the "shape" of data).

In Smalltalk, by contrast, a class is not a promise to the compiler (since there is no compile-time type checking).
It's more a description for the programmer and a container of methods.
The "contract" in Smalltalk is informal and psychological: you are expected to pass objects that will do the right thing.
If you violate that expectation, the system will tell you at runtime.
Thus, the mental model shifts from "I have a guarantee this object supports X, Y, Z operations" to
"I believe (or have tested) that this object supports X, Y, Z--and if I'm wrong, I'll find out when I run the code."
The class of the object is a strong hint (since class defines the methods), but it's not an enforced boundary.
Indeed, a seasoned Smalltalker might say an object's true "type" is simply the set of messages it knows how to
handle, regardless of its class name.
The class is one way to know that set, but it's not the only way--you could also query the object at runtime (ask it `respondsTo:` a certain selector) or consult documentation/tests.

### Living with Dynamic Typing: The Programmer's Experience

The day-to-day experience of programming in Smalltalk is very dynamic and interactive, which affects how one thinks about types.
In a static language, you often plan out type hierarchies and use the compiler as a tool to catch mistakes early.
In Smalltalk, you rely on a combination of clear design, tests, and the interactive environment to ensure objects are used appropriately.
For example, you might write a method that expects "an object that can print itself."
You won't declare a type, but you'll likely name the parameter suggestively (e.g. `anObject` or `aPrintable`) and maybe mention in a comment that it should respond to `printOn:`.
When using that method, you ensure you pass something like a String or a Number (classes that you know implement `printOn:`).
There is a lot of trust and convention involved--but it's trust backed by the ability to quickly try things out in the live environment.

Smalltalk's development environment is a persistent image of objects, where you can test sending messages in a Workspace or inspect an object's class and methods on the fly.
This means that if you're unsure about what messages an object supports, you can literally ask the object or its class at runtime.
The system can list an object's method selectors or let you browse its class hierarchy.
This introspective capability (made possible because everything is alive in the image) gives you a form of "live documentation."
A Smalltalk system is an ecosystem of live objects.
You can query the running program directly, rather than rely solely on static type information.

When you make a mistake--say you send a message an object doesn't understand--it's not usually a silent failure.
In a typical Smalltalk IDE, a debugger pops up at the point of error (the MessageNotUnderstood).
This is not just an error message; it's an opportunity.
You can inspect the actual object that failed (seeing its class and state), figure out why it didn't have the method, and often even
define the missing method right there in the debugger and continue execution.
This exemplifies the "lived" experience: the program is malleable and can be fixed or extended on the fly.
The boundary of what an object's "type" is can literally be extended during runtime by adding a new method to its class (or by implementing
`doesNotUnderstand:` to catch that message next time).
Such dynamism is foreign to statically typed environments but is natural in Smalltalk's philosophy.
It emphasizes that software is fluid--an object's behavior (hence its type) can evolve as the program runs.

From a philosophical standpoint, a Smalltalk programmer tends to think in terms of objects and messages first, and types (in the classical sense) hardly at all.
Alan Kay, the father of Smalltalk, famously remarked that "OOP to me means only messaging, local retention and protection and hiding
of state-process, and extreme late-binding of all things."
(Late-binding here refers to deciding at run-time what method to invoke for a given message--precisely what dynamic typing entails.) This mindset puts the focus on behavior rather than classification.
If you ask a Smalltalker "what type is this object?" they are likely to answer in terms of its class or its responsibilities (e.g.
"this is a kind of stream object--it can next/nextPut: etc.").
They wouldn't typically enumerate a static type name with a fixed interface contract because that's not how the language frames the discussion.

All you can do with any object is send it a message and observe the result; therefore, conceptually, "type" is just a description of those results you can expect.

### Contrast with the Static Typing Mindset

To crystallize the differences, it helps to compare the Smalltalk approach with how statically typed language programmers think about types:

Types as Explicit Contracts (Static Languages): In a static language (Java, C#, Haskell, etc.), a type is an explicit contract or
blueprint for both the compiler and the programmer.
For instance, an interface in Java might guarantee that anything of that interface type has certain methods.
The programmer leans on the compiler to enforce that contract--calling a non-existent method or violating type expectations is caught at compile time.
This often leads to designing software by starting with type definitions (classes/interfaces) that model the problem domain and using those as
constraints* to prevent incorrect usage.
Types also serve as documentation: you know a function `foo(Vector v)` requires a `Vector` and you know exactly what a `Vector` can do (from its class/interface definition).
There's comfort (and some rigidity) in this; you can't accidentally call
`v.turnPurple()` on a `Vector` if that method isn't in its type.
But you also can't pass a `Matrix` to `foo` unless `Matrix` is declared to be a subclass or implementer of `Vector`--even if
`Matrix` happens to support all the same operations needed, the static type system will reject it if it's not formally declared compatible.

* Types as Descriptions of Behavior (Smalltalk): In Smalltalk, types are not explicit labels but implicit descriptions of behavior.
  If a method expects a "duck-like" object, you simply pass it an object and trust it knows how to quack; there is no
  `IDuck` interface to check against.
  As long as the object can handle the messages used inside the method, it works--otherwise a runtime error occurs.
  This is often called "programming by wishful
  thinking" or optimistic coding: you code as if the object will do what you want, and usually your design ensures it will.
  In cases where you want to be cautious, you might do a runtime check (using `object respondsTo: #quack` or an
  `isKindOf:` check), but ideally polymorphism makes that unnecessary.
  The emphasis is on what an object can do, not what it is declared to be.
  The result is a very flexible system: any object that meets the behavioral expectations can be used, even if it wasn't originally anticipated.
  There is no need to cast or to adapt types to match an exact signature--the message itself is the only requirement.
  This is why Smalltalk (and languages like it) enable a style where
  "if it quacks like a duck, it's a duck."
  The trade-off is that mistakes show up at runtime, so thorough testing and a good suite of examples are essential to gain confidence in the code's correctness.

Classes vs. Types: Smalltalk's classes fill some of the same roles as static types (grouping objects with similar behavior,
giving a name to a set of methods), but they are not used as a compile-time gatekeeper.
They are more for the programmer's organization and the runtime method lookup.
In statically typed languages, you often have distinct concepts of "class vs interface vs type parameter," etc., which are all part of the type system.
Smalltalk collapses much of that--a class is essentially a concrete implementation and
potentially* also the description of a protocol, but there's nothing like a separately declared interface.
So a Smalltalk programmer might think "this object is a kind of OrderedCollection because it's an instance of that class, so it supports all the collection messages."
But they are also free to pass in any other object that honors the same messages (even if it's not a
`OrderedCollection` subclass) to code that was written with `OrderedCollection` in mind.
The flexibility is higher, though the guarantee is only verified when the code runs.

In summary, programmers in statically typed languages often view types as static contracts or enforcement mechanisms, whereas Smalltalk programmers view types more as emergent properties of objects.
The Smalltalker's mindset is shaped by a live, message-oriented world where you gain understanding by sending messages and watching objects behave.
It's a very experience-driven understanding of type: an object "proves" its type by working correctly in response to your messages,
not by satisfying a compiler check ahead of time.
This can be incredibly liberating--it encourages focusing on what needs to happen in the problem domain,
letting different kinds of objects participate as long as they behave appropriately.
As the Smalltalk ethos would suggest, "Look at what the object does, not what it says it is."

### Conclusion: The Philosophical Takeaway

From a practical and philosophical perspective, "type" in Smalltalk is less a label and more a dynamic quality of an object's behavior.
It's defined by the messages an object understands and how it responds, which is ultimately determined by its class's methods (and any clever
`doesNotUnderstand:` tricks).
An object can certainly be said to "have a type" in Smalltalk--but that type isn't a static tag; it's the set of messages it can handle,
i.e., its protocol.
Smalltalk's class system provides the structure for those protocols (acting as a template for behavior),
but it doesn't impose the sort of strict borders that static type systems do.
Instead of types as fences that keep misuse at bay, Smalltalk offers open pastures
where objects roam freely as long as they know how to handle the interactions (messages) that come their way.

The lived Smalltalk experience is one of constant discovery and feedback: you send a message and see what happens.
This leads to a very concrete understanding of an object's capabilities--you gain knowledge of its "type" by observing it in action.
Philosophically, this shifts the notion of type from an abstract compile-time idea to a tangible runtime reality.
Rather than trust a compiler's assurances, you come to trust the objects themselves (and your tests of them).
Smalltalk's message-driven worldview teaches that an object is exactly what it does.
By emphasizing messaging and late binding, it reminds us that software is ultimately about dynamic interactions.
In statically typed systems, type is often treated as essence; in Smalltalk, type is experience.
The result is a programming model that is highly flexible, deeply object-oriented,
and rooted in the immediate reality of message sends--a model where the concept of "type" lives not in declarations,
but in the rich interplay between objects at runtime.
