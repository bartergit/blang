from b_type import BType
from cpp_codegen.code_context import CodeContext
from ast_def import Struct


def generate_struct(ctx: CodeContext, struct: Struct):
    ctx.add(f"struct {struct.struct_name} {{")
    fields = ';\n'.join([f"{field.type.cpp} {field.name}" for field in struct.fields])
    ctx.add(f"{fields};\n}};")