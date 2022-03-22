from typing import Union

from ast_def import Number, Identifier, BinOperator, UnaryOperator, Bool, Call, Expression, StringLiteral
from cpp_codegen.code_context import CodeContext
from cpp_codegen.generate_binary import generate_binary_operator
from cpp_codegen.generate_unary import generate_unary_operator

ExprType = Union[Number, Identifier, BinOperator, UnaryOperator, Bool, Call, Expression]


def generate_call(ctx: CodeContext, expr: ExprType) -> None:
    arguments = []
    if expr.type.is_struct():
        ctx.add(f"{ctx.add_reg()}")
    for param in expr.params:
        generate_expression(ctx, param)
        arguments.append(str(ctx.pop()))
    typeof = expr.type.cpp
    pre = f"{typeof} {ctx.add_reg()} = " if typeof != "void" else ""
    ctx.listing.append(f"{pre}{expr.name}({', '.join(arguments)});")
    ctx.parameters.append(ctx.reg)


def generate_expression(ctx: CodeContext, expr: ExprType) -> None:
    data_type = type(expr)
    if data_type is Number:
        ctx.parameters.append(expr.data)
    elif data_type is Bool:
        ctx.parameters.append(expr.data)
    elif data_type is BinOperator:
        generate_binary_operator(ctx, expr)
    elif data_type is UnaryOperator:
        generate_unary_operator(ctx, expr)
    elif data_type == Call:
        generate_call(ctx, expr)
    elif data_type == Expression:
        generate_expression(ctx, expr.data[0])
    elif data_type == Identifier:
        ctx.parameters.append(expr.data)  # if expr.is_struct() else "&" + expr.data
    elif data_type == StringLiteral:
        ctx.parameters.append(f'"{expr.data}"')
    else:
        assert 0, expr
