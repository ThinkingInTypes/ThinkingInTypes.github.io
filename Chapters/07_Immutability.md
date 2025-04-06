# Immutability

- Benefits of immutability
- Historic immutability by convention with all caps
- Immutability with `Final`

Dataclasses support immutability with `frozen`:

```python
# example_2.py
from dataclasses import dataclass, field
from typing import List


@dataclass(frozen=True)
class Order:
    order_id: int
    items: List[str] = field(default_factory=list)


order = Order(order_id=123)
# order.order_id = 456  # Error: dataclass is frozen (immutable)
```

- show *post\_init* with frozen
