"""Evaluator: walks the AST with an environment of variables, constants,
and math functions.
"""
import math

from .errors import CalcNameError, CalcMathError
from .parser import Number, Var, BinOp, UnaryOp, Call, Assign


def _log(*args):
    if len(args) == 1:
        return math.log(args[0])
    if len(args) == 2:
        return math.log(args[0], args[1])
    raise CalcMathError(f"log() takes 1 or 2 arguments, got {len(args)}")


FUNCTIONS = {
    "sin": math.sin, "cos": math.cos, "tan": math.tan,
    "asin": math.asin, "acos": math.acos, "atan": math.atan,
    "sqrt": math.sqrt, "exp": math.exp, "abs": abs,
    "floor": math.floor, "ceil": math.ceil,
    "log": _log, "ln": math.log,
    "max": max, "min": min,
    "round": round,
}

CONSTANTS = {"pi": math.pi, "e": math.e, "tau": math.tau}


class Evaluator:
    def __init__(self):
        self.env = dict(CONSTANTS)

    def evaluate(self, node):
        if isinstance(node, Number):
            return node.value
        if isinstance(node, Var):
            if node.name not in self.env:
                raise CalcNameError(f"unknown variable {node.name!r}")
            return self.env[node.name]
        if isinstance(node, Assign):
            if node.name in CONSTANTS:
                raise CalcNameError(f"cannot reassign constant {node.name!r}")
            value = self.evaluate(node.value)
            self.env[node.name] = value
            return value
        if isinstance(node, UnaryOp):
            v = self.evaluate(node.operand)
            return -v if node.op == "-" else v
        if isinstance(node, BinOp):
            return self._binop(node)
        if isinstance(node, Call):
            return self._call(node)
        raise CalcMathError(f"cannot evaluate node {node!r}")

    def _binop(self, node):
        left = self.evaluate(node.left)
        right = self.evaluate(node.right)
        try:
            if node.op == "+":
                return left + right
            if node.op == "-":
                return left - right
            if node.op == "*":
                return left * right
            if node.op == "/":
                if right == 0:
                    raise CalcMathError("division by zero")
                return left / right
            if node.op == "%":
                if right == 0:
                    raise CalcMathError("modulo by zero")
                return left % right
            if node.op == "^":
                return left ** right
        except OverflowError as exc:
            raise CalcMathError(f"numeric overflow: {exc}")
        raise CalcMathError(f"unknown operator {node.op!r}")

    def _call(self, node):
        fn = FUNCTIONS.get(node.name)
        if fn is None:
            raise CalcNameError(f"unknown function {node.name!r}")
        args = [self.evaluate(a) for a in node.args]
        try:
            return fn(*args)
        except ValueError as exc:
            raise CalcMathError(f"{node.name}(): {exc}")
        except TypeError as exc:
            raise CalcMathError(f"{node.name}(): {exc}")


def calculate(text, evaluator=None):
    """Parse and evaluate one line; returns the numeric result."""
    from .tokenizer import tokenize
    from .parser import parse
    ev = evaluator or Evaluator()
    return ev.evaluate(parse(tokenize(text), text))
