from ast_def import VariableDeclaration
from parse.parse_expression import parse_expression
from parse.parse_other import parse_identifier, parse_type
from parser_definition import Parser


def parse_declaration(parser: Parser) -> VariableDeclaration:
    var_type = parse_type(parser)
    var_name = parse_identifier(parser).data
    parser.expect('=')
    expr = parse_expression(parser)
    parser.expect(';')
    return VariableDeclaration(var_type, var_name, expr)
