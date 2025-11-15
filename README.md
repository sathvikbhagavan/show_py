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

## Use Case: Debugging Code

The `show` function is particularly useful for debugging code. Instead of manually adding print statements, you can quickly inspect variable values and expressions:

```python
from show_py import show

def process_data(items, threshold):
    # Debug: Check input values
    show(items, threshold)
    filtered = [x for x in items if x > threshold]
    # Debug: Check filtered results
    show(filtered, len(filtered))
    result = sum(filtered) / len(filtered) if filtered else 0
    # Debug: Check final calculation
    show(result)
    return result

# Usage
data = [10, 20, 30, 40, 50]
avg = process_data(data, 25)
# Output:
# items = [10, 20, 30, 40, 50]
# threshold = 25
# filtered = [30, 40, 50]
# len(filtered) = 3
# result = 40.0
```

**Benefits for debugging:**
- **No need to write separate print statements** - the expression is automatically captured
- **See both the expression and its value** - helps understand what's being computed
- **Works inline** - can be used in the middle of expressions without breaking code flow
- **Easy to remove** - just delete the `show()` call when done debugging

**Example: Debugging a complex calculation**

```python
from show_py import show

def calculate_score(scores):
    # Debug each step
    total = sum(scores)
    show(total)
    
    count = len(scores)
    show(count)
    
    average = total / count
    show(average)
    
    # Debug the final expression
    final_score = show(average * 1.2)
    return final_score

scores = [85, 90, 78, 92, 88]
result = calculate_score(scores)
# Output:
# total = 433
# count = 5
# average = 86.6
# average * 1.2 = 103.92
```

## Running Tests

```bash
pytest
```

With coverage:
```bash
pytest --cov=show_py --cov-report=html
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

