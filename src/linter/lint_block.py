from b_type import BType, special
from ast_def import Block, Expression, VariableDeclaration, Assign, Loop, Condition, Return
from linter.lint_context import LintContext
from linter.lint_expr import lint_expression


def lint_block(ctx: LintContext, block: Block, return_type: BType):
    for statement in block.statements:
        statement_type = type(statement)
        try:
            if statement_type == Expression:
                lint_expression(ctx, statement)
            elif statement_type == VariableDeclaration:
                declared_type = statement.var_type
                expr_type = lint_expression(ctx, statement.expr)
                var_name = statement.var_name
                ctx.check(expr_type, declared_type, f"declaration `{var_name}`")
                assert ctx.vars.get(var_name) is None, f"`{var_name}` is already exists in the scope"
                assert var_name not in special, f"`{var_name}` is reserved keyword"
                assert var_name not in ctx.function_signatures, f"`{var_name}` is already used as function name"
                ctx.vars[var_name] = declared_type
            elif statement_type == Assign:
                assign_to_type = lint_expression(ctx, statement.assign_to)
                expr_type = lint_expression(ctx, statement.expr)
                ctx.check(expr_type, assign_to_type, "assignment:")
            elif statement_type in (Loop, Condition):
                ctx.check(lint_expression(ctx, statement.expr), BType("bool"), statement_type.__name__)
                lint_block(ctx, statement.block, return_type)
            elif statement_type == Return:
                got_return_type = lint_expression(ctx, statement.expr)
                ctx.check(got_return_type, return_type, "return")
            else:
                assert 0, statement
        except AssertionError as e:
            line_start = statement.tokens[0].start[0]
            line = '\n'.join(set([token.line.strip() for token in statement.tokens]))
            e.args = f"at line {line_start}:\n{line}\n\n{e.args[0]}",
            raise e