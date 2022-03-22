from typing import Union

from ast_def import Number, Identifier, BinOperator, UnaryOperator, Bool, Call, Expression
from cpp_codegen.code_context import CodeContext
from linter.lint_context import ExprType


def generate_binary_operator(ctx: CodeContext, expr: ExprType) -> None:
    from cpp_codegen.generate_expr import generate_expression
    operator = expr.data
    first, second = expr.content
    generate_expression(ctx, first)
    if operator == ".":
        assign_to = ctx.pop() + "." + second.data
        ctx.add(f"{expr.type.cpp} {ctx.add_reg()} = {assign_to};")
        ctx.parameters.append(ctx.reg)
        return
    if operator == "as":
        ctx.add(f"{expr.type.cpp} * {ctx.add_reg()} = ({expr.type.cpp}) {ctx.pop()};")
        ctx.parameters.append(ctx.reg)
        return
    generate_expression(ctx, second)
    second_reg, first_reg = ctx.pop(), ctx.pop()
    if operator in ("==", "!=", "<", "<=", ">", ">=", "or", "and", "+", "-", "*"):
        ctx.listing.append(f"{expr.type.cpp} {ctx.add_reg()} = {first_reg} {operator} {second_reg};")
    if operator == "/":
        ctx.listing.append(f"{expr.type.cpp} {ctx.add_reg()} = (float){first_reg} {operator} {second_reg};")
    if operator == "as":
        ctx.listing.append(f"{expr.type.cpp} {ctx.add_reg()} = ({expr.type.cpp}) {first_reg};")
    ctx.parameters.append(ctx.reg)
