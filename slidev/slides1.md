---
# You can also start simply with 'default'
#theme: seriph
# random image from a curated Unsplash collection by Anthony
# like them? see https://unsplash.com/collections/94734566/slidev
# some information about your slides (markdown enabled)
title: Thinking in Types
info: |
  ## From ThinkingInTypes.com
# apply unocss classes to the current slide
class: text-center
# https://sli.dev/features/drawing
drawings:
  persist: false
# slide transition: https://sli.dev/guide/animations.html#slide-transitions
# enable MDC Syntax: https://sli.dev/features/mdc
mdc: true
# open graph
# seoMeta:
#  ogImage: https://cover.sli.dev
transition: fade-out

layout: image
image: background.png
backgroundSize: contain
---

# Make Illegal States Unrepresentable

## Pycon 2025 Typing Summit

### From ThinkingInTypes.com

---

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

---

```python
# missing_method.py
from smalltalk_object import SmalltalkObject

obj = SmalltalkObject()
obj.dance()
## SmalltalkObject: 'dance' not found
```