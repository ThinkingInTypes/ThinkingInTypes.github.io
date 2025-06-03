# Async Types

```python
# async_resource.py
# For reuse in subsequent examples
import asyncio
from dataclasses import dataclass


@dataclass
class Resource:
    name: str

    @classmethod
    async def get(cls, name: str) -> Resource:
        await asyncio.sleep(0.1)
        return cls(name=name)

    async def work(self) -> str:
        await asyncio.sleep(0.1)
        return f"Completed: {self.name}"
```

```python
# awaitable.py
import asyncio
from typing import Awaitable

from async_resource import Resource


def get_resource_awaitable() -> Awaitable[Resource]:
    return Resource.get("1. Awaitable")


async def get_async_resource_awaitable() -> None:
    resource = await get_resource_awaitable()
    print(await resource.work())


asyncio.run(get_async_resource_awaitable())
## Completed: 1. Awaitable
```

```python
# coroutine.py
import asyncio
from typing import Coroutine
from async_resource import Resource


def get_resource_coroutine() -> Coroutine[None, None, Resource]:
    return Resource.get("2. Coroutine")


async def get_async_resource_coroutine() -> None:
    resource = await get_resource_coroutine()
    print(await resource.work())


asyncio.run(get_async_resource_coroutine())
## Completed: 2. Coroutine
```

```python
# async_iterator_iterable.py
import asyncio
from typing import AsyncIterator, AsyncIterable

from async_resource import Resource


class ResourceStreamer:
    def __init__(self) -> None:
        self.count = 3

    def __aiter__(self) -> AsyncIterator[Resource]:
        return self

    async def __anext__(self) -> Resource:
        if self.count <= 0:
            raise StopAsyncIteration
        self.count -= 1
        await asyncio.sleep(0.1)
        return Resource(f"3. stream-{self.count}")


async def consume_stream(
    stream: AsyncIterable[Resource],
) -> None:
    async for resource in stream:
        print(await resource.work())


async def consumer() -> None:
    await consume_stream(ResourceStreamer())


asyncio.run(consumer())
## Completed: 3. stream-2
## Completed: 3. stream-1
## Completed: 3. stream-0
```

```python
# async_generator.py
import asyncio
from typing import AsyncGenerator

from async_resource import Resource


async def generate_resources() -> AsyncGenerator[Resource, None]:
    for i in range(3):
        await asyncio.sleep(0.1)
        yield Resource(f"4. gen-{i}")


async def generate_resources_coroutine() -> None:
    async for r in generate_resources():
        print(await r.work())


asyncio.run(generate_resources_coroutine())
## Completed: 4. gen-0
## Completed: 4. gen-1
## Completed: 4. gen-2
```

```python
# async_context_manager.py
import asyncio
from contextlib import asynccontextmanager
from typing import AsyncIterator

from async_resource import Resource


@asynccontextmanager
async def resource_context() -> AsyncIterator[Resource]:
    print("5. Acquiring resource")
    await asyncio.sleep(0.1)
    yield Resource("5. AsyncContextManager")
    print("5. Releasing resource")
    await asyncio.sleep(0.1)


async def get_resource_manager_async() -> None:
    async with resource_context() as res:
        print(await res.work())


asyncio.run(get_resource_manager_async())
## 5. Acquiring resource
## Completed: 5. AsyncContextManager
## 5. Releasing resource
```

```python
# callable_returning_awaitable.py
import asyncio
from typing import Awaitable, Callable

from async_resource import Resource


def resource_factory() -> Callable[[], Awaitable[Resource]]:
    async def make() -> Resource:
        await asyncio.sleep(0.1)
        return Resource("6. Callable returning Awaitable")

    return make


async def get_resource_factory() -> None:
    factory = resource_factory()
    resource = await factory()
    print(await resource.work())


asyncio.run(get_resource_factory())
## Completed: 6. Callable returning Awaitable
```

```python
# generic_async_context_manager.py
import asyncio
from contextlib import asynccontextmanager
from typing import AsyncIterator

from async_resource import Resource


@asynccontextmanager
async def manage[T](value: T) -> AsyncIterator[T]:
    print(f"Acquiring {value}")
    yield value
    print(f"Releasing {value}")


async def generic_async_context_manager() -> None:
    async with manage(Resource("7. Generic")) as resource:
        print(await resource.work())


asyncio.run(generic_async_context_manager())
## Acquiring Resource(name='7. Generic')
## Completed: 7. Generic
## Releasing Resource(name='7. Generic')
```
