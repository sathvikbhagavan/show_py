"""Tests for the show function."""

import sys
from io import StringIO
from unittest.mock import Mock, patch

from show_py import show


def test_show_single_value():
    """Test show with a single value."""
    x = 42
    captured_output = StringIO()
    sys.stdout = captured_output

    result = show(x)

    sys.stdout = sys.__stdout__
    output = captured_output.getvalue().strip()

    assert output == "x = 42"
    assert result == 42


def test_show_multiple_values():
    """Test show with multiple values."""
    a = 1
    b = 2
    c = 3

    captured_output = StringIO()
    sys.stdout = captured_output

    result = show(a, b, c)

    sys.stdout = sys.__stdout__
    output = captured_output.getvalue().strip()

    assert "a = 1" in output
    assert "b = 2" in output
    assert "c = 3" in output
    assert result == (1, 2, 3)


def test_show_expression():
    """Test show with an expression."""
    x = 5
    y = 10

    captured_output = StringIO()
    sys.stdout = captured_output

    result = show(x + y)

    sys.stdout = sys.__stdout__
    output = captured_output.getvalue().strip()

    assert "x + y = 15" in output
    assert result == 15


def test_show_string():
    """Test show with string values."""
    message = "hello"

    captured_output = StringIO()
    sys.stdout = captured_output

    result = show(message)

    sys.stdout = sys.__stdout__
    output = captured_output.getvalue().strip()

    assert output == "message = 'hello'"
    assert result == "hello"


def test_show_list():
    """Test show with list values."""
    my_list = [1, 2, 3]

    captured_output = StringIO()
    sys.stdout = captured_output

    result = show(my_list)

    sys.stdout = sys.__stdout__
    output = captured_output.getvalue().strip()

    assert "my_list = [1, 2, 3]" in output
    assert result == [1, 2, 3]


def test_show_dict():
    """Test show with dictionary values."""
    my_dict = {"a": 1, "b": 2}

    captured_output = StringIO()
    sys.stdout = captured_output

    result = show(my_dict)

    sys.stdout = sys.__stdout__
    output = captured_output.getvalue().strip()

    assert "my_dict = " in output
    assert result == {"a": 1, "b": 2}


def test_show_none():
    """Test show with None value."""
    x = None

    captured_output = StringIO()
    sys.stdout = captured_output

    result = show(x)

    sys.stdout = sys.__stdout__
    output = captured_output.getvalue().strip()

    assert output == "x = None"
    assert result is None


def test_show_function_call():
    """Test show with a function call."""
    def add(a, b):
        return a + b

    captured_output = StringIO()
    sys.stdout = captured_output

    result = show(add(3, 4))

    sys.stdout = sys.__stdout__
    output = captured_output.getvalue().strip()

    assert "add(3, 4) = 7" in output
    assert result == 7


def test_show_multiline_expression():
    """Test show with a multi-line expression."""
    x = 1
    y = 2
    z = 3

    captured_output = StringIO()
    sys.stdout = captured_output

    result = show(
        x + y + z
    )

    sys.stdout = sys.__stdout__
    output = captured_output.getvalue().strip()

    # Should capture the expression even if it spans multiple lines
    assert "7" in output or "x + y + z = 6" in output
    assert result == 6


def test_show_nested_structure():
    """Test show with nested data structures."""
    data = {
        "nested": {
            "list": [1, 2, {"inner": "value"}]
        }
    }

    captured_output = StringIO()
    sys.stdout = captured_output

    result = show(data)

    sys.stdout = sys.__stdout__
    output = captured_output.getvalue().strip()

    assert "data = " in output
    assert result == data


def test_show_return_value_single():
    """Test that show returns the value when called with single argument."""
    x = 100
    result = show(x)
    assert result == 100


def test_show_return_value_multiple():
    """Test that show returns tuple when called with multiple arguments."""
    a, b, c = 1, 2, 3
    result = show(a, b, c)
    assert result == (1, 2, 3)


def test_show_in_function():
    """Test show when called from within a function."""
    def test_func():
        local_var = 42
        return show(local_var)

    captured_output = StringIO()
    sys.stdout = captured_output

    result = test_func()

    sys.stdout = sys.__stdout__
    output = captured_output.getvalue().strip()

    assert "local_var = 42" in output
    assert result == 42


def test_show_ipython_single_value():
    """Test show with IPython history for single value."""
    # Mock IPython modules
    mock_ipython = Mock()
    mock_ip = Mock()
    mock_hist = Mock()

    # Set up history manager
    mock_hist.session_number = 1
    mock_hist.get_range.return_value = [(1, 1, "show(x)")]
    mock_ip.history_manager = mock_hist
    mock_ipython.get_ipython.return_value = mock_ip

    x = 42

    with patch.dict('sys.modules', {'IPython': mock_ipython}):
        captured_output = StringIO()
        sys.stdout = captured_output

        result = show(x)

        sys.stdout = sys.__stdout__
        output = captured_output.getvalue().strip()

        assert output == "x = 42"
        assert result == 42


def test_show_ipython_expression():
    """Test show with IPython history for expression."""
    # Mock IPython modules
    mock_ipython = Mock()
    mock_ip = Mock()
    mock_hist = Mock()

    # Set up history manager
    mock_hist.session_number = 1
    mock_hist.get_range.return_value = [(1, 1, "show(x + y)")]
    mock_ip.history_manager = mock_hist
    mock_ipython.get_ipython.return_value = mock_ip

    x = 5
    y = 10

    with patch.dict('sys.modules', {'IPython': mock_ipython}):
        captured_output = StringIO()
        sys.stdout = captured_output

        result = show(x + y)

        sys.stdout = sys.__stdout__
        output = captured_output.getvalue().strip()

        assert "x + y = 15" in output
        assert result == 15


def test_show_ipython_multiple_values():
    """Test show with IPython history for multiple values."""
    # Mock IPython modules
    mock_ipython = Mock()
    mock_ip = Mock()
    mock_hist = Mock()

    # Set up history manager
    mock_hist.session_number = 1
    mock_hist.get_range.return_value = [(1, 1, "show(a, b, c)")]
    mock_ip.history_manager = mock_hist
    mock_ipython.get_ipython.return_value = mock_ip

    a = 1
    b = 2
    c = 3

    with patch.dict('sys.modules', {'IPython': mock_ipython}):
        captured_output = StringIO()
        sys.stdout = captured_output

        result = show(a, b, c)

        sys.stdout = sys.__stdout__
        output = captured_output.getvalue().strip()

        assert "a = 1" in output
        assert "b = 2" in output
        assert "c = 3" in output
        assert result == (1, 2, 3)


def test_show_ipython_function_call():
    """Test show with IPython history for function call."""
    # Mock IPython modules
    mock_ipython = Mock()
    mock_ip = Mock()
    mock_hist = Mock()

    # Set up history manager
    mock_hist.session_number = 1
    mock_hist.get_range.return_value = [(1, 1, "show(add(3, 4))")]
    mock_ip.history_manager = mock_hist
    mock_ipython.get_ipython.return_value = mock_ip

    def add(a, b):
        return a + b

    with patch.dict('sys.modules', {'IPython': mock_ipython}):
        captured_output = StringIO()
        sys.stdout = captured_output

        result = show(add(3, 4))

        sys.stdout = sys.__stdout__
        output = captured_output.getvalue().strip()

        assert "add(3, 4) = 7" in output
        assert result == 7


def test_show_ipython_no_history():
    """Test show with IPython but no history (falls back to normal behavior)."""
    # Mock IPython modules but with empty history
    mock_ipython = Mock()
    mock_ip = Mock()
    mock_hist = Mock()

    # Set up history manager with empty history
    mock_hist.session_number = 1
    mock_hist.get_range.return_value = []
    mock_ip.history_manager = mock_hist
    mock_ipython.get_ipython.return_value = mock_ip

    x = 42

    with patch.dict('sys.modules', {'IPython': mock_ipython}):
        captured_output = StringIO()
        sys.stdout = captured_output

        result = show(x)

        sys.stdout = sys.__stdout__
        output = captured_output.getvalue().strip()

        # Should fall back to variable matching
        assert "x = 42" in output
        assert result == 42


def test_show_ipython_no_show_in_history():
    """Test show with IPython but history doesn't contain show call."""
    # Mock IPython modules
    mock_ipython = Mock()
    mock_ip = Mock()
    mock_hist = Mock()

    # Set up history manager with history that doesn't contain 'show('
    mock_hist.session_number = 1
    mock_hist.get_range.return_value = [(1, 1, "x = 42")]
    mock_ip.history_manager = mock_hist
    mock_ipython.get_ipython.return_value = mock_ip

    x = 42

    with patch.dict('sys.modules', {'IPython': mock_ipython}):
        captured_output = StringIO()
        sys.stdout = captured_output

        result = show(x)

        sys.stdout = sys.__stdout__
        output = captured_output.getvalue().strip()

        # Should fall back to variable matching
        assert "x = 42" in output
        assert result == 42


def test_show_ipython_no_ipython_module():
    """Test show when IPython module is not available."""
    x = 42

    # Ensure IPython is not in sys.modules
    with patch.dict('sys.modules', {}, clear=False):
        if 'IPython' in sys.modules:
            del sys.modules['IPython']

        captured_output = StringIO()
        sys.stdout = captured_output

        result = show(x)

        sys.stdout = sys.__stdout__
        output = captured_output.getvalue().strip()

        # Should work normally without IPython
        assert "x = 42" in output
        assert result == 42

