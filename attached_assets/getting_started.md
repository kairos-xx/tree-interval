# Getting Started

Welcome to the **Transformer** package! This guide will help you get started with transforming and tracking Python objects.

## Installation

You can install Transformer using `pip`:

```bash
pip install Transformer

Or install it manually:

git clone https://github.com/yourusername/Transformer.git
cd Transformer
pip install .
```

## Basic Usage

Here's a simple example to demonstrate how to use Transformer:
```python
from Transformer.transformer import Transformer


def main():
    transformer = Transformer()
    a = transformer.transform({})

    # Chained Attribute Assignment
    a.b.c.d.e.f = 3
    print(a)  # Output: DictProxy({'b': {'c': {'d': {'e': {'f': 3}}}}}})
    print(a.b.c.d.e.f)  # Output: 3


if __name__ == "__main__":
    main()
```

## Exploring Proxies

Transformer uses proxy classes to wrap original objects. Here's how different types are handled:

- **Mutable Types**: dict, list, set
- **Immutable Types**: int, float, str, tuple, frozenset, complex

*Each proxy allows dynamic attribute assignments and method interceptions.*

# Advanced Usage

*For more complex scenarios, Transformer supports path-based access and method interception.*

```python
from Transformer.transformer import Transformer


def advanced_example():
    transformer = Transformer()
    a = transformer.transform({"numbers": [1, 2, 3]})

    # Path-Based Access
    a["numbers"].append(4)
    print(a["numbers"])  # Output: [1, 2, 3, 4]

    # Chained Attribute Access
    a.new_attr.sub_attr = "Hello"
    print(a.new_attr.sub_attr)  # Output: Hello


if __name__ == "__main__":
    advanced_example()
```
# API Reference

Refer to the API Documentation for detailed information on classes and methods.

# FAQs

**Q1:** What types of objects can be transformed?

**A1:** Transformer supports both mutable and immutable types, including dict, list, set, int, float, str, tuple, frozenset, and complex.

**Q2:** How does method interception work?

**A2:** Transformer wraps methods to log calls and transform their results into proxies, allowing you to monitor method executions.

# License

Transformer is licensed under the MIT License.