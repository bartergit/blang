from b_type import BType
from linter.lint_context import LintContext, ExprType


def lint_binary_operator(ctx: LintContext, expr: ExprType) -> BType:
    from linter.lint_expr import lint_expression
    from linter.lint_expr import expr_as_type
    operator = expr.data
    first, second = expr.content
    if operator == ".":
        first_type = lint_expression(ctx, first)
        struct_params = ctx.struct_signatures.get(first_type.type)
        if struct_params is None:
            ctx.lint_error(first_type, "struct")
        for field in struct_params:
            if field.name == second.data:
                expr.type = field.type
                return expr.type
        ctx.lint_error(second.data, [x.name for x in struct_params], "unknown field .")
    if operator == "as":
        _ = lint_expression(ctx, first)
        try:
            to_cast_type = BType.new(ctx, expr_as_type(ctx, second))
        except AssertionError:
            ctx.lint_error(second, "type", "for operator as second argument")
        expr.type = to_cast_type
        return to_cast_type
    first_type, second_type = lint_expression(ctx, first), lint_expression(ctx, second)
    if operator in ("==", "!="):
        ctx.check(first_type, second_type, operator)
        expr.type = BType.new(ctx, "bool")
        return BType.new(ctx, "bool")
    if operator in ("<", "<=", ">", ">="):
        expected = (BType.new(ctx, "float"), BType.new(ctx, "int"))
        if first_type not in (BType.new(ctx, "float"), BType.new(ctx, "int")):
            ctx.lint_error(first_type, expected)
        if second_type not in (BType.new(ctx, "float"), BType.new(ctx, "int")):
            ctx.lint_error(second_type, expected)
        expr.type = BType.new(ctx, "bool")
        return BType.new(ctx, "bool")
    if operator in ("or", "and"):
        ctx.check((first_type, second_type), (BType.new(ctx, "bool"), BType.new(ctx, "bool")), operator)
        expr.type = BType.new(ctx, "bool")
        return first_type
    if operator in ("+", "-", "*"):
        expected = BType.new(ctx, "float"), BType.new(ctx, "int")
        if not (first_type in expected):
            ctx.lint_error(first_type, expected, operator)
        if not (second_type in expected):
            ctx.lint_error(second_type, expected, operator)
        if BType.new(ctx, "float") in (first_type, second_type):
            expr.type = BType.new(ctx, "float")
            return BType.new(ctx, "float")
        ctx.check((first_type, second_type), (BType.new(ctx, "int"), BType.new(ctx, "int")), operator)
        expr.type = BType.new(ctx, "int")
        return BType.new(ctx, "int")
    if operator == "/":
        expected = (BType.new(ctx, "float"), BType.new(ctx, "int"))
        if first_type not in expected:
            ctx.lint_error(first_type, expected)
        if second_type not in expected:
            ctx.lint_error(second_type, expected)
        expr.type = BType.new(ctx, "int")
        return BType.new(ctx, "float")
    assert 0, f"unknown binary operator {operator}"
