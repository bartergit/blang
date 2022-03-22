from ast_def import Struct, Param
from parser_definition import Parser

from parse.parse_other import parse_type, parse_identifier


def parse_struct(parser: Parser) -> Struct:
    parser.expect('struct')
    struct_name = parse_identifier(parser).data
    parser.expect('{')
    current = parser.lookahead()
    fields = []
    while current != "}":
        field_type = parse_type(parser)
        field_name = parse_identifier(parser).data
        parser.expect(";")
        fields.append(Param(field_type, field_name))
        current = parser.lookahead()
    parser.eat()
    return Struct(struct_name, fields)
