from b_type import BType
from ast_def import Program, Param
from linter.lint_block import lint_block
from linter.lint_context import LintContext


def lint_program(program: Program) -> None:
    FunctionSignature = tuple[BType, list[Param]]
    function_signatures: dict[str, FunctionSignature] = {
        'malloc': (BType('void').ref(), [Param(BType('int'), 'size')]),
        'alloc': (BType('void').ref(), [Param(BType('int'), 'size')]),
        'shift': (BType('void').ref(), [Param(BType('*void'), 'size'), Param(BType('int'), 's')]),
        'free': (BType('void'), [Param(BType('*void'), 'ptr')]),
        'sizeof': (BType('int'), [Param(BType('int'), 's')]),
        'printf': (BType('int'), [Param(BType('*byte'), 's')]),
        'printd': (BType('int'), [Param(BType('int'), 's')]),
    }
    ctx = LintContext(function_signatures=function_signatures)
    for struct in program.structs:
        ctx.struct_signatures[struct.struct_name] = struct.fields
    for function in program.functions:
        ctx.function_signatures[function.function_name] = function.return_type, function.params
    for function in program.functions:
        return_type = function.return_type
        for param in function.params:
            ctx.vars[param.name] = param.type
        lint_block(ctx, function.block, return_type)
        ctx.vars.clear()
