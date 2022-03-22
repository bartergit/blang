from ast_def import Assign
from parser_definition import Parser
from parse.parse_expression import parse_expression
from parse.parse_other import parse_identifier


def parse_assign(parser: Parser) -> Assign:
    var_name = parse_expression(parser)
    parser.expect('=')
    expr = parse_expression(parser)
    parser.expect(';')
    return Assign(var_name, expr)

