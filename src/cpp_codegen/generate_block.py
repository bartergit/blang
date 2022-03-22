from b_type import BType
from cpp_codegen.code_context import CodeContext
from cpp_codegen.generate_expr import generate_expression
from ast_def import Block, Expression, VariableDeclaration, Assign, Identifier, UnaryOperator, BinOperator, Loop, \
    Condition, Return


def generate_block(ctx: CodeContext, block: Block, to_open = True):
    if to_open:
        ctx.add("{")
    for statement in block.statements:
        statement_type = type(statement)
        if statement_type == Expression:
            generate_expression(ctx, statement.data[0])
            ctx.pop()
        elif statement_type == VariableDeclaration:
            generate_expression(ctx, statement.expr)
            ctx.add(f"{statement.var_type.cpp} {statement.var_name} = {ctx.pop()};")
        elif statement_type == Assign:
            generate_expression(ctx, statement.expr)
            assign_to_expr = statement.assign_to.data[0]
            if type(assign_to_expr) == Identifier:
                assign_to = assign_to_expr.data
            elif type(assign_to_expr) == UnaryOperator and assign_to_expr.data == "*":
                generate_expression(ctx, assign_to_expr.content)
                assign_to = "*" + ctx.pop()
            elif type(assign_to_expr) == BinOperator and assign_to_expr.data == ".":
                generate_expression(ctx, assign_to_expr.content[0])
                assign_to = ctx.pop() + "." + assign_to_expr.content[1].data
            ctx.add(f"{assign_to} = {ctx.pop()};")
        elif statement_type == Loop:
            ctx.add("while (1){")
            generate_expression(ctx, statement.expr)
            ctx.add(f"if (!{ctx.pop()}) break;")
            generate_block(ctx, statement.block, False)
        elif statement_type == Condition:
            generate_expression(ctx, statement.expr)
            ctx.add(f"if ({ctx.pop()})")
            generate_block(ctx, statement.block)
        elif statement_type == Return:
            generate_expression(ctx, statement.expr)
            ctx.add(f"return {ctx.pop()};")
    ctx.add("}")