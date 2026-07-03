import re
import math
from agents import function_tool

SAFE_PATTERN = re.compile(r"^[\d\s+\-*/().,%^&|~<>!=\[\]a-zA-Z_]+$")


def _safe_eval(expression: str) -> str:
    """Evaluate a mathematical expression safely.

    Only allows numeric operations, math module functions, and basic logical
    operators. Blocks builtins, imports, and file I/O.
    """
    if not expression.strip():
        return "Error: Empty expression."

    if not SAFE_PATTERN.match(expression):
        return "Error: Expression contains disallowed characters."

    allowed_names = {
        "math": math,
        "abs": abs,
        "round": round,
        "min": min,
        "max": max,
        "sum": sum,
        "pow": pow,
        "int": int,
        "float": float,
        "True": True,
        "False": False,
        "pi": math.pi,
        "e": math.e,
    }

    try:
        result = eval(expression, {"__builtins__": {}}, allowed_names)
        return str(result)
    except ZeroDivisionError:
        return "Error: Division by zero."
    except Exception as e:
        return f"Error: {e}"


@function_tool
def calculate(expression: str) -> str:
    """Evaluate a mathematical expression and return the result.

    Supports: +, -, *, /, **, //, %, parentheses, and math.* functions
    (e.g., math.sqrt, math.sin, math.cos, math.pi, math.e).

    Args:
        expression: The mathematical expression to evaluate (e.g., "2 + 2",
            "math.sqrt(144)", "(15 + 3) * 2").
    """
    return _safe_eval(expression)
