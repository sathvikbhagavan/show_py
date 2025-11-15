# show-py

A Python package that mimics Julia's `@show` macro, allowing you to print expressions and their values in a convenient way.

## Installation

```bash
pip install -e .
```

For development with tests:
```bash
pip install -e ".[dev]"
```

## Usage

The `show` function prints the expression and its value, then returns the value(s):

```python
from show_py import show

# Single value
x = 42
show(x)  # Prints: x = 42

# Multiple values
a, b = 1, 2
show(a, b)  # Prints: a = 1, b = 2

# Expressions
result = show(x + 10)  # Prints: x + 10 = 52, returns 52

# Function calls
def add(a, b):
    return a + b

show(add(3, 4))  # Prints: add(3, 4) = 7

# Works with any Python object
my_list = [1, 2, 3]
show(my_list)  # Prints: my_list = [1, 2, 3]

# Multi-line expressions (basic support)
show(
    x + 10
)  # Prints the expression and its value
```

## Features

- Prints expressions and their values in a readable format
- Supports single and multiple values
- Returns the value(s) for use in assignments
- Works with any Python object
- Basic support for multi-line expressions

## Running Tests

```bash
pytest
```

With coverage:
```bash
pytest --cov=show_py --cov-report=html
```

## License

MIT

