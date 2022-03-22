from ast_def import Loop
from parser_definition import Parser

from parse.parse_expression import parse_expression


def parse_while(parser: Parser) -> Loop:
    from parse.parse_block import parse_block
    parser.expect("while")
    expr = parse_expression(parser)
    block = parse_block(parser)
    return Loop(expr, block)
