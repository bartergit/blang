import parse.parse_expression as p_expr
from ast_def import Call
from parse.parse_other import parse_identifier
from parser_definition import Parser


def parse_call(parser: Parser) -> Call:
    params = []
    function_name = parse_identifier(parser).data
    parser.expect("(")
    if parser.lookahead() == ")":
        parser.eat()
        return Call(function_name, params)
    while True:
        expr = p_expr.parse_expression(parser)
        # status, expr = parser.safe_wrap(lambda: p_expr.parse_expression(parser))
        # if not status:
        #     status, expr = parser.safe_wrap(lambda: parse_type(parser))
        #     if not status:
        #         parser.syntax_error("expression or typed parameter")
        params.append(expr)
        token = parser.lookahead()
        if token == ",":
            parser.eat()
            continue
        parser.expect(")")
        return Call(function_name, params)
