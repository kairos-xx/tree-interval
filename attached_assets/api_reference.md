# API Reference

## Module: `transformer.py`

### Class: `Transformer`

The `Transformer` class is responsible for transforming and managing proxies.

#### Methods:

- **`__init__(self) -> None`**
  
  Initializes the Transformer instance.

- **`transform(self, value: T) -> TransformedObject[T]`**
  
  Transforms the given value into a proxy object.

  - **Parameters:**
    - `value` (`T`): The object to transform.
  
  - **Returns:**
    - `TransformedObject[T]`: The transformed proxy object.

- **`wrap_class(self, cls: Type[T]) -> Type[T]`**
  
  Wraps a class by creating a proxy subclass that intercepts method calls.

  - **Parameters:**
    - `cls` (`Type[T]`): The class to wrap.
  
  - **Returns:**
    - `Type[T]`: The wrapped class.

- **`reshape_references(self, original: T, transformed: Any) -> None`**
  
  Replaces all references to the original object with the transformed proxy object.

  - **Parameters:**
    - `original` (`T`): The original object.
    - `transformed` (`Any`): The transformed proxy object.

- **`add_class(self, cls: Type[T]) -> None`**
  
  Adds a class to be tracked and shadow its methods.

  - **Parameters:**
    - `cls` (`Type[T]`): The class to add.

- **`add_instance(self, instance: T) -> None`**
  
  Adds an instance to be tracked.

  - **Parameters:**
    - `instance` (`T`): The instance to add.

## Module: `proxy.py`

### Class: `DynamicProxy`

A versatile proxy class that supports both attribute and item access.

#### Methods:

- **`__new__(cls, obj: T, transformer: 'Transformer') -> 'DynamicProxy[T]'`**
  
  Creates a new instance of DynamicProxy or returns an existing one from the registry.

- **`__init__(self, obj: T, transformer: 'Transformer') -> None`**
  
  Initializes the proxy instance.

- **`__getattr__(self, name: str) -> Any`**
  
  Handles attribute access, creating intermediate proxies during assignments.

- **`__setattr__(self, name: str, value: Any) -> None`**
  
  Handles attribute assignments.

- **`__getitem__(self, key: Any) -> Any`**
  
  Handles item access, supporting path-based strings.

- **`__setitem__(self, key: Any, value: Any) -> None`**
  
  Handles item assignments, supporting path-based strings.

- **`get_original(self) -> T`**
  
  Retrieves the original object.

- **`__repr__(self) -> str`**
  
  Returns the string representation of the proxy.

- **`__str__(self) -> str`**
  
  Returns the string representation of the original object.

### Class: `DictProxy`

A specialized proxy class for dictionaries that allows attribute-style access.

#### Methods:

- **`__getattr__(self, name: str) -> Any`**
  
  Retrieves the value associated with the given key, transforming it if necessary.

- **`__setattr__(self, name: str, value: Any) -> None`**
  
  Sets the value for the given key, transforming it if necessary.

- **`__repr__(self) -> str`**
  
  Returns the string representation of the dictionary proxy.

### Immutable Proxies: `IntProxy`, `FloatProxy`, `StrProxy`, `TupleProxy`, `FrozensetProxy`, `ComplexProxy`

Each immutable proxy inherits from its respective built-in type and `DynamicProxy`, enabling dynamic attribute assignments without compromising immutability.

#### Common Methods:

- **Arithmetic Operations (`__add__`, `__sub__`, `__mul__`, etc.)**
  
  Overridden to include logging and ensure results are transformed into proxies.

- **`get_original(self) -> OriginalType`**
  
  Retrieves the original immutable value.

- **`__repr__(self) -> str`**
  
  Returns the string representation of the proxy.

- **`__str__(self) -> str`**
  
  Returns the string representation of the original value.
