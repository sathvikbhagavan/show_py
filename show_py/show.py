"""Implementation of show function that mimics Julia's @show macro.

This module provides a Python equivalent of Julia's @show macro, which
prints expressions along with their values. It works by introspecting
the caller's source code to extract the original expressions.
"""

import ast
import inspect
import sys
import textwrap


def _get_function_name(node):
    """Extract function name from an AST node.

    Args:
        node: AST node representing a function call

    Returns:
        str or None: Function name if found, None otherwise
    """
    if isinstance(node.func, ast.Name):
        return node.func.id
    elif isinstance(node.func, ast.Attribute):
        return node.func.attr
    return None


def _extract_expressions_from_ast(tree, source, target_func="show",
                                   target_lineno=None, lineno_offset=0):
    """Extract argument expressions from AST for a specific function call.

    Args:
        tree: Parsed AST tree
        source: Source code string
        target_func: Name of the function to find (default: "show")
        target_lineno: Target line number to match (None to match any)
        lineno_offset: Offset to add to AST line numbers

    Returns:
        list: List of expression strings
    """
    exprs = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            func_name = _get_function_name(node)
            if func_name == target_func:
                # Check line number if specified
                if target_lineno is None or (node.lineno + lineno_offset == target_lineno):
                    for arg in node.args:
                        expr_str = ast.get_source_segment(source, arg)
                        if expr_str:
                            exprs.append(expr_str.strip())
                    if exprs:
                        break
    return exprs


def _try_ipython_history(frame):
    """Try to extract expressions from IPython input history.

    Args:
        frame: Caller's frame object

    Returns:
        list: List of expression strings, empty if extraction fails
    """
    try:
        ipython = sys.modules.get('IPython')
        if not ipython:
            return []

        ip = ipython.get_ipython()
        if not ip or not hasattr(ip, 'history_manager'):
            return []

        hist = ip.history_manager
        session = hist.session_number
        history_range = list(hist.get_range(session, output=False))

        if not history_range:
            return []

        # Get the last command from history
        last_cmd = history_range[-1]
        if not last_cmd or len(last_cmd) < 3:
            return []

        source = last_cmd[2]  # last_cmd is (session, line_num, input)
        if not source or 'show(' not in source:
            return []

        # Parse and extract expressions
        tree = ast.parse(source)
        return _extract_expressions_from_ast(tree, source)
    except Exception:
        return []


def _get_source_code(frame):
    """Get source code for the caller's frame.

    Args:
        frame: Caller's frame object

    Returns:
        tuple: (source_code, lineno_offset) or (None, 0) if unavailable
    """
    filename = frame.f_code.co_filename

    # Try inspect.getsourcelines first (works for functions/code blocks)
    try:
        source_lines, first_line = inspect.getsourcelines(frame)
        source = ''.join(source_lines)
        source = textwrap.dedent(source)
        return source, first_line - 1
    except OSError:
        pass

    # Try reading the file directly
    if filename and filename != '<stdin>' and not filename.startswith('<'):
        try:
            with open(filename) as f:
                return f.read(), 0
        except OSError:
            pass

    # Try inspect.getsource on frame
    try:
        return inspect.getsource(frame), 0
    except (OSError, TypeError):
        pass

    # Try inspect.getsource on code object
    try:
        return inspect.getsource(frame.f_code), 0
    except (OSError, TypeError):
        pass

    return None, 0


def _match_variables_to_values(values, local_vars):
    """Match values to variable names in local scope.

    Args:
        values: Tuple of values to match
        local_vars: Dictionary of local variables

    Returns:
        list: List of variable names or "<expression>" placeholders
    """
    exprs = []
    for val in values:
        matched = False

        # First try identity match (exact same object)
        for name, var_val in local_vars.items():
            if var_val is val:
                exprs.append(name)
                matched = True
                break

        # If no identity match, try equality for immutable types
        if not matched:
            for name, var_val in local_vars.items():
                if (isinstance(val, (int, float, str, bool, type(None))) and
                    var_val == val and
                    not name.startswith('_')):
                    exprs.append(name)
                    matched = True
                    break

        if not matched:
            exprs.append("<expression>")

    return exprs


def show(*values):
    """Mimics Julia's @show macro, printing expressions and their values.

    This function prints each expression along with its value, then returns
    the value(s) for use in assignments. It works by extracting the source
    code of the calling context and parsing it to find the expressions.

    Args:
        *values: Variable number of values to show

    Returns:
        The single value if one argument provided, otherwise a tuple of values

    Examples:
        >>> x = 42
        >>> show(x)
        x = 42
        42

        >>> a, b = 1, 2
        >>> show(a, b)
        a = 1
        b = 2
        (1, 2)

        >>> result = show(x + 10)
        x + 10 = 52
        52

    Supported Contexts:
        - **Files**: Full expression extraction works perfectly
        - **Functions/code blocks**: Full expression extraction via inspect
        - **IPython/Jupyter**: Uses input history for expression extraction
        - **Pure Python REPL**:
          - Simple variables (e.g., ``show(x)``): Works via variable matching
          - Expressions (e.g., ``show(x + y)``): Falls back to ``<expression>``

    Note:
        In pure Python REPL, expressions cannot be extracted because Python
        doesn't store the source of single-line expressions. The function
        falls back to variable name matching for simple cases.
    """
    frame = inspect.currentframe().f_back
    filename = frame.f_code.co_filename
    caller_lineno = frame.f_lineno

    # Try IPython history first (if available)
    exprs = _try_ipython_history(frame)

    # If IPython didn't work, try standard source extraction
    if not exprs:
        source, lineno_offset = _get_source_code(frame)
        if source:
            try:
                tree = ast.parse(source, filename=filename if filename != '<stdin>' else '')
                exprs = _extract_expressions_from_ast(
                    tree, source,
                    target_lineno=caller_lineno,
                    lineno_offset=lineno_offset
                )
            except (SyntaxError, ValueError):
                # If AST parsing fails, fall through to variable matching
                pass

    # Fallback: try to match values to variable names in local scope
    if not exprs:
        exprs = _match_variables_to_values(values, frame.f_locals)

    # Ensure we have the right number of expressions
    while len(exprs) < len(values):
        exprs.append("<expression>")

    # Print each expression and its value
    for expr, val in zip(exprs, values):
        print(f"{expr} = {val!r}")

    # Return single value or tuple for consistency
    if len(values) == 1:
        return values[0]
    return values

