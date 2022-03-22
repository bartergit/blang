from ast_def import Identifier
from b_type import BType
from parser_definition import Parser


def parse_identifier(parser: Parser) -> Identifier:
    identifier = parser.peek()
    assert identifier.isidentifier(), f"wrong identifier `{identifier}`"
    return Identifier(identifier)


def parse_type(parser: Parser) -> BType:
    var_type = ""
    while parser.lookahead() == "*":
        var_type += "*"
        parser.eat()
    var_type += parse_identifier(parser).data
    return BType(var_type)
