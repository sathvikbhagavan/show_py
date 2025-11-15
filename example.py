"""Example usage of the show function."""

from show_py import show

# Single value
x = 42
show(x)

# Multiple values
a, b = 1, 2
show(a, b)

# Expressions
y = 10
result = show(x + y)

# Function calls
def add(a, b):
    return a + b

show(add(3, 4))

# Lists and dictionaries
my_list = [1, 2, 3]
show(my_list)

my_dict = {"key": "value", "number": 42}
show(my_dict)

# Nested structures
nested = {
    "outer": {
        "inner": [1, 2, 3]
    }
}
show(nested)

