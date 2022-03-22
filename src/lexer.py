import subprocess
import sys
from tokenize import TokenInfo

from ast_def import Program
from ast_pretty import ast_pretty
from cpp_codegen.generate_program import generate_program
from linter.lint_program import lint_program
from parse.parse_function import parse_function
from parse.parse_macro import parse_macro, expand_macros
from parse.parse_struct import parse_struct
from parser_definition import Parser
from tokenizer import tokenize


def lexer(tokens: list[TokenInfo]) -> Program:
    parser = Parser(0, tokens)
    current = parser.lookahead()
    while True:
        if current != "macro":
            break
        parse_macro(parser)
        current = parser.lookahead()
    expand_macros(parser)
    current = parser.lookahead()
    program = Program()
    while current is not None:
        if current == "func":
            program.functions.append(parse_function(parser))
        elif current == "struct":
            program.structs.append(parse_struct(parser))
        elif current == "macro":
            parser.syntax_error("macro defined before functions and structures")
        else:
            parser.syntax_error("func or struct")
        current = parser.lookahead()
    return program