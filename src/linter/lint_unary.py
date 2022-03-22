from b_type import BType
from linter.lint_context import LintContext, ExprType


def lint_unary_operator(ctx: LintContext, expr: ExprType) -> BType:
    from linter.lint_expr import lint_expression
    expr_type = lint_expression(ctx, expr.content)
    operator = expr.data
    if operator == "*":
        if not expr_type.is_ref():
            ctx.lint_error(expr_type, "pointer", operator)
        expr.type = expr_type.deref()
        return expr_type.deref()
    elif operator == "!":
        ctx.check(expr_type, BType.new(ctx, "bool"), operator)
        expr.type = BType.new(ctx, "bool")
        return BType.new(ctx, "bool")
    elif operator == "-":
        expected = (BType.new(ctx, "int"), BType.new(ctx, "float"))
        if expr_type not in expected:
            ctx.lint_error(expr_type, expected, operator)
        expr.type = expr_type
        return expr_type
    else:
        assert 0, f"unknown unary operator {operator}"
