import os
import subprocess
import sys

from ast_pretty import ast_pretty
from cpp_codegen.generate_program import generate_program
from lexer import lexer
from linter.lint_program import lint_program
from tokenizer import tokenize


def main() -> None:
    file_path = sys.argv[1] if len(sys.argv) > 1 else "resources/test_struct_ref.barter"
    with open(file_path, "r") as f:
        tokens = tokenize(f.read())
    program = lexer(tokens)
    lint_program(program)
    ast = ast_pretty(program.functions, -1)
    listing = generate_program(program)
    with open("target/output.cpp", "w") as f:
        f.write(listing)
    return_code = subprocess.call("g++ target/output.cpp -o target/output.exe")
    if return_code == 0:
        return_code = subprocess.call("target/output.exe")
        os.remove("target/output.exe")
        exit(return_code)


if __name__ == '__main__':
    main()
