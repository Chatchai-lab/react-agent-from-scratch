import ast
import operator

from src.tools.base import Tool

_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.Mod: operator.mod,
    ast.USub: operator.neg,
    ast.UAdd: operator.pos,
}


def _eval_node(node):
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return node.value
    if isinstance(node, ast.BinOp) and type(node.op) in _OPERATORS:
        return _OPERATORS[type(node.op)](_eval_node(node.left), _eval_node(node.right))
    if isinstance(node, ast.UnaryOp) and type(node.op) in _OPERATORS:
        return _OPERATORS[type(node.op)](_eval_node(node.operand))
    raise ValueError(f"Unzulässiger Ausdruck: {ast.dump(node)}")


def _format_result(value) -> str:
    if isinstance(value, float) and value.is_integer():
        return str(int(value))
    return str(value)


class CalculatorTool(Tool):
    name = "calculator"
    description = "Evaluates a mathematical expression and returns the result."
    parameters = {
        "type": "object",
        "properties": {
            "expression": {
                "type": "string",
                "description": "The mathematical expression to evaluate, e.g. '12 * (3 + 4)'",
            },
        },
        "required": ["expression"],
    }

    def run(self, args: dict) -> str:
        expression = args["expression"]
        try:
            tree = ast.parse(expression, mode="eval")
            result = _eval_node(tree.body)
        except ZeroDivisionError:
            return "Fehler: Division durch 0"
        except (ValueError, SyntaxError, TypeError):
            return f"Fehler: ungültiger Ausdruck '{expression}'"
        return _format_result(result)


calculator = CalculatorTool()
