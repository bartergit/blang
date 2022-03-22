from b_type import BType
from cpp_codegen.code_context import CodeContext
from cpp_codegen.generate_block import generate_block
from ast_def import Param, Function


def codegen_params(ctx: CodeContext, params: list[Param]):
    s = ""
    for i, param in enumerate(params):
        s += f"{param.type.cpp} {param.name}{',' if i != len(params) - 1 else ''}"
    ctx.add(s)


def generate_function(ctx: CodeContext, function: Function):
    barter_type = function.return_type
    ctx.add(f"{barter_type.cpp} {function.function_name}(")
    codegen_params(ctx, function.params)
    ctx.add(")")
    generate_block(ctx, function.block)