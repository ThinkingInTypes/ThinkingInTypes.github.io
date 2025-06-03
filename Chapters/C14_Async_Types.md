# Async Types

```python
# async_resource.py
# For reuse in subsequent examples
import asyncio
from dataclasses import dataclass


async def do_work():
    await asyncio.sleep(0.1)


@dataclass
class Resource:
    name: str

    @classmethod
    async def get(cls, name: str) -> Resource:
        await do_work()
        return cls(name=name)

    async def process(self) -> str:
        await do_work()
        return f"Completed: {self.name}"
```

```python
# awaitable.py
import asyncio
from typing import Awaitable

from async_resource import Resource


def get_resource_awaitable() -> Awaitable[Resource]:
    return Resource.get("Awaitable")


async def get_async_resource_awaitable() -> None:
    resource = await get_resource_awaitable()
    print(await resource.process())


asyncio.run(get_async_resource_awaitable())
## Completed: Awaitable
```

```python
# coroutine.py
import asyncio
from typing import Coroutine
from async_resource import Resource


def get_resource_coroutine() -> Coroutine[None, None, Resource]:
    return Resource.get("Coroutine")


async def get_async_resource_coroutine() -> None:
    resource = await get_resource_coroutine()
    print(await resource.process())


asyncio.run(get_async_resource_coroutine())
## Completed: Coroutine
```

```python
# async_iterator_iterable.py
import asyncio
from typing import AsyncIterator, AsyncIterable

from async_resource import Resource, do_work


class ResourceStreamer:
    def __init__(self) -> None:
        self.count = 3

    def __aiter__(self) -> AsyncIterator[Resource]:
        return self

    async def __anext__(self) -> Resource:
        if self.count <= 0:
            raise StopAsyncIteration
        self.count -= 1
        await do_work()
        return Resource(f"Stream-{self.count}")


async def consume_stream(
    stream: AsyncIterable[Resource],
) -> None:
    async for resource in stream:
        print(await resource.process())


async def consumer() -> None:
    await consume_stream(ResourceStreamer())


asyncio.run(consumer())
## Completed: Stream-2
## Completed: Stream-1
## Completed: Stream-0
```

```python
# async_generator.py
import asyncio
from typing import AsyncGenerator

from async_resource import Resource, do_work


async def generate_resources() -> AsyncGenerator[Resource, None]:
    for i in range(3):
        await do_work()
        yield Resource(f"gen-{i}")


async def generate_resources_coroutine() -> None:
    async for r in generate_resources():
        print(await r.process())


asyncio.run(generate_resources_coroutine())
## Completed: gen-0
## Completed: gen-1
## Completed: gen-2
```

```python
# callable_returning_awaitable.py
import asyncio
from typing import Awaitable, Callable

from async_resource import Resource, do_work


def resource_factory() -> Callable[[], Awaitable[Resource]]:
    async def make() -> Resource:
        await do_work()
        return Resource("Callable Returning Awaitable")

    return make


async def get_resource_factory() -> None:
    factory = resource_factory()
    resource = await factory()
    print(await resource.process())


asyncio.run(get_resource_factory())
## Completed: Callable Returning Awaitable
```

```python
# async_context_manager.py
import asyncio
from contextlib import asynccontextmanager
from typing import AsyncIterator

from async_resource import Resource


@asynccontextmanager
async def resource_context() -> AsyncIterator[Resource]:
    resource = Resource("Async Context Manager")
    print(f"Acquired {resource}")
    yield resource
    print(f"Releasing {resource}")


async def async_context_manager_async() -> None:
    async with resource_context() as res:
        print(await res.process())


asyncio.run(async_context_manager_async())
## Acquired Resource(name='Async Context Manager')
## Completed: Async Context Manager
## Releasing Resource(name='Async Context Manager')
```

```python
# generic_async_context_manager.py
import asyncio
from contextlib import asynccontextmanager
from typing import AsyncIterator

from async_resource import Resource


@asynccontextmanager
async def manage[T](value: T) -> AsyncIterator[T]:
    print(f"Acquired {value}")
    yield value
    print(f"Releasing {value}")


async def generic_async_context_manager() -> None:
    async with manage(Resource("Generic ACM")) as resource:
        print(await resource.process())


asyncio.run(generic_async_context_manager())
## Acquired Resource(name='Generic ACM')
## Completed: Generic ACM
## Releasing Resource(name='Generic ACM')
```
