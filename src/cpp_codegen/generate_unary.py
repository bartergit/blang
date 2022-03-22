from cpp_codegen.code_context import CodeContext
from linter.lint_context import ExprType


def generate_unary_operator(ctx: CodeContext, expr: ExprType) -> None:
    from cpp_codegen.generate_expr import generate_expression
    operator = expr.data
    generate_expression(ctx, expr.content)
    if operator in ("*", "!", "-"):
        ctx.listing.append(f"{expr.type.cpp} {ctx.add_reg()} = {operator} {ctx.pop()};")
        ctx.parameters.append(ctx.reg)
