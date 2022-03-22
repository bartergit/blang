# some ugggggly code, can be refactored, but hey, it works
from typing import Any

from ast_def import *


def pretty_expr(expr, shift=0) -> str:
    if type(expr) == Expression:
        s = ""
        for el in expr.data:
            s += ast_pretty(el, shift)
        return s
    if type(expr) == UnaryOperator:
        return "  " * shift + expr.data + "\n" + pretty_expr(expr.content, shift + 1)
    if type(expr) == BinOperator:
        return "  " * shift + expr.data + "\n" + pretty_expr(expr.content[0], shift + 1) + pretty_expr(expr.content[1],
                                                                                                       shift + 1)
    if type(expr) in (Bool, Number, Identifier):
        return "  " * shift + str(expr.data) + "\n"
    return ast_pretty(expr, shift)


def ast_pretty(node: Any, shift=0, header="") -> str:
    tmp = []
    nested = []
    if isinstance(node, (BinOperator, UnaryOperator, Number, Identifier, Expression)):
        return "  " * shift + "expr=\n" + pretty_expr(node, shift + 1)
    if isinstance(node, (str, int)):
        return str(node)
    if isinstance(node, list):
        return ''.join([ast_pretty(el, shift + 1) for el in node])
    for key, value in node.__dict__.items():
        if key == "tokens":
            continue
        if isinstance(value, list):
            nested.append(ast_pretty(value, shift))
            continue
        if not isinstance(value, (str, int)):
            nested.append(ast_pretty(value, shift + 1, key))
            continue
        tmp.append(f"{key}={value}")
    if list(node.__dict__.keys()) == ["data"]:
        tmp = [value]
    type_name = type(node).__name__
    header = header + "=" if len(header) else ""
    return "  " * shift + header + type_name + ': ' + ', '.join(tmp) + '\n' + ''.join(nested)
