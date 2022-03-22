from ast_def import Param, Function
from parser_definition import Parser

from parse.parse_block import parse_block
from parse.parse_other import parse_type, parse_identifier

def parse_params(parser: Parser) -> list[Param]:
    params = []
    parser.expect("(")
    if parser.lookahead() == ")":
        parser.eat()
        return []
    while True:
        typeof = parse_type(parser)
        name = parse_identifier(parser).data
        params.append(Param(typeof, name))
        token = parser.lookahead()
        if token == ",":
            parser.eat()
            continue
        parser.expect(")")
        return params


def parse_function(parser: Parser) -> Function:
    parser.expect('func')
    func_name = parse_identifier(parser).data
    params = parse_params(parser)
    parser.expect('->')
    return_type = parse_type(parser)
    return Function(func_name, return_type, params, parse_block(parser))
