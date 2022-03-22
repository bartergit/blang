from b_type import BType
from linter.lint_context import LintContext, ExprType


def lint_function_call(ctx: LintContext, expr: ExprType) -> BType:
    from linter.lint_expr import lint_expression
    function_name = expr.name
    signature = ctx.function_signatures.get(function_name)
    assert signature is not None, f"unknown function `{function_name}`"
    return_type, expected_params = signature
    expr.type = return_type
    got_params = expr.params
    got_types = [lint_expression(ctx, param) for param in got_params]
    expected_types = [param.type for param in expected_params]
    ctx.check(got_types, expected_types)
    return return_type
