Here’s a complete **Markdown-formatted chapter section** titled **"Programming in the Smalltalk Style (in Python)"**, ready to paste into your book.

---

````markdown
## Programming in the Smalltalk Style (in Python)

Smalltalk isn't just a language—it’s a way of programming. Rather than designing everything up front, Smalltalk encourages programmers to build systems **interactively**, **incrementally**, and **dynamically**. In this section, we’ll recreate that experience using Python to demonstrate what it
*feels* like to develop in the Smalltalk style.

The key ideas:

- Everything is an object.
- You send messages to objects, even if you don’t know whether they understand them.
- Objects can learn new behaviors at runtime.
- The system evolves live as you work.

Let’s build a simple chatbot, step by step, entirely at runtime.

---

### Step 1: Begin with the base object

```python
class SmalltalkObject:
    def __getattr__(self, name):
        def handler(*args, **kwargs):
            return self.does_not_understand(name, *args, **kwargs)
        return handler

    def does_not_understand(self, name, *args, **kwargs):
        print(f"{self.__class__.__name__} does not understand the message '{name}'")
````

We start with a basic object that handles unknown messages by implementing `does_not_understand`, similar to how Smalltalk does it.

---

### Step 2: Create a blank chatbot

```python
class Chatbot(SmalltalkObject):
    def __init__(self):
        self.history = []
```

Now we create an instance of our chatbot. It doesn't yet respond to anything.

---

### Step 3: Talk to it

```python
bot = Chatbot()
bot.hello()
```

Output:

```
Chatbot does not understand the message 'hello'
```

Just like in Smalltalk, when you send a message the object doesn't understand, it falls back to `doesNotUnderstand:`.

---

### Step 4: Teach it how to say hello

```python
def hello(self):
    print("Hello! I'm your chatbot.")
    self.history.append("hello")


setattr(Chatbot, "hello", hello)
bot.hello()
```

Output:

```
Hello! I'm your chatbot.
```

We added this method at runtime. No compilation step—just live system growth.

---

### Step 5: Make it remember unknown messages

```python
def does_not_understand(self, message, *args, **kwargs):
    print(f"Sorry, I don't understand '{message}', but I'll remember it.")
    self.history.append(message)


setattr(Chatbot, "does_not_understand", does_not_understand)

bot.weather()
bot.joke()
```

Output:

```
Sorry, I don't understand 'weather', but I'll remember it.
Sorry, I don't understand 'joke', but I'll remember it.
```

Now the chatbot learns from what it hears.

---

### Step 6: Teach it a joke

```python
def joke(self):
    print("Why did the duck cross the road? Because it was the chicken's day off.")
    self.history.append("joke")


setattr(Chatbot, "joke", joke)
bot.joke()
```

Output:

```
Why did the duck cross the road? Because it was the chicken's day off.
```

Again, we add behavior dynamically.

---

### Step 7: Inspect its capabilities

```python
print("Messages it understands now:", [m for m in dir(bot) if not m.startswith("_")])
print("History:", bot.history)
```

Output:

```
Messages it understands now: ['does_not_understand', 'hello', 'history', 'joke', 'weather']
History: ['hello', 'weather', 'joke', 'joke']
```

Just like a Smalltalk browser, we inspect our object’s current interface and state.

---

This entire session mirrors the experience of working in a Smalltalk image: there is no compile-run-edit loop. You interact with objects directly, teach them behavior, and the system grows and adapts as you explore it.

```

---

Would you like this turned into an executable Jupyter notebook or included in a Reveal.js slide deck?
```
