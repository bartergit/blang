from ast_def import Condition
from parser_definition import Parser

from parse.parse_expression import parse_expression

def parse_if(parser: Parser) -> Condition:
    from parse.parse_block import parse_block
    parser.expect("if")
    expr = parse_expression(parser)
    block = parse_block(parser)
    return Condition(expr, block)

