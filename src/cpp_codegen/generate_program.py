from ast_def import Program
from cpp_codegen.code_context import CodeContext
from cpp_codegen.generate_function import generate_function
from cpp_codegen.generate_struct import generate_struct


def generate_program(program: Program) -> str:
    ctx = CodeContext()
    for struct in program.structs:
        generate_struct(ctx, struct)
    for function in program.functions:
        generate_function(ctx, function)
    s = "#include <cstdlib>\n"\
        "#include <stdio.h>\n" \
        "void* shift(void*ptr, int size){return (char*)ptr + size;}\n" \
        'int printd(int s){return printf("%d", s);}\n' +\
        '\n'.join(ctx.listing)
    return s
