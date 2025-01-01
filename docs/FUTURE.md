
# Future - Dynamic Attribute Handling

The `Future` class provides powerful dynamic attribute handling with context-aware error reporting. It can intelligently determine whether an attribute chain access is for setting or getting values, and act accordingly.

## Key Features

### 1. Context-Aware Attribute Creation
The `Future` class analyzes the call stack to determine if an attribute access is part of:
- A setting operation (e.g., `obj.a.b.c = 42`) → Creates missing attributes
- A getting operation (e.g., `print(obj.a.b.c)`) → Raises AttributeError if not found

### 2. Rich Error Context
When an attribute is not found, the error message includes:
- The exact position in code where the error occurred
- The full context of the failed statement
- Visual markers showing which part of the chain failed

## Usage Example

```python
from inspect import stack
from typing import Any
from tree_interval.core.future import Future

class Nested:
    def __init__(self) -> None:
        self.__dict__: dict[str, "Nested"] = {}

    def __getattr__(self, name: str) -> Any:
        return Future(name,
                     frame=stack()[1].frame,
                     instance=self,
                     new_return=type(self)())

# Usage
a = Nested()
a.b.c.d = 3  # Creates the entire chain: b, c, and d
print(a.b.c.d)  # Prints: 3
print(a.x.y.z)  # Raises AttributeError with context
```

### Error Output Example
```
Attribute x not found in obj
   File "example.py", line 15, in <module>
   print(obj.x.y.z)
   ^^^^^^~~~~*~~~~^
```

## Implementation Details

The `Future` class achieves this by:
1. Analyzing the call stack frame when an attribute is accessed
2. Using AST analysis to determine if the access is part of a setting operation
3. For setting operations: Creates new instances of the class dynamically
4. For getting operations: Raises detailed AttributeError with context

## Best Practices

1. Always provide a `new_return` value that matches your class type
2. Use the frame from `stack()[1]` to get the correct caller context
3. Initialize an empty `__dict__` in `__init__` to store dynamic attributes

This powerful feature enables building flexible nested structures while maintaining strict attribute access control and helpful debugging information.
