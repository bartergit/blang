from ast_def import Number, Identifier, BinOperator, UnaryOperator, Bool, Call, Expression, StringLiteral
from linter.lint_binary import lint_binary_operator
from linter.lint_call import lint_function_call
from linter.lint_context import LintContext, BType, ExprType
from linter.lint_unary import lint_unary_operator


def expr_as_type(ctx: LintContext, expr: ExprType) -> str:
    if type(expr) == Identifier:
        return expr.data
    if type(expr) == UnaryOperator:
        return "*" + expr_as_type(ctx, expr.content)
    assert 0


def lint_expression(ctx: LintContext, expr: ExprType) -> BType:
    # probably unary/bin should be handled the same way as functions, idk
    data_type = type(expr)
    if data_type is Number:
        return BType("int")
    if data_type is Bool:
        return BType("bool")
    if data_type is BinOperator:
        return lint_binary_operator(ctx, expr)
    if data_type is UnaryOperator:
        return lint_unary_operator(ctx, expr)
    if data_type == Call:
        return lint_function_call(ctx, expr)
    if data_type == Expression:
        assert len(expr.data) == 1
        return lint_expression(ctx, expr.data[0])
    if data_type == Identifier:
        var_name = expr.data
        typeof = ctx.vars.get(var_name)
        assert typeof is not None, f"unknown reference `{var_name}`, known are: {', '.join(ctx.vars.keys())}"
        return typeof
    if data_type == StringLiteral:
        return BType("*byte")
    else:
        assert 0, expr
