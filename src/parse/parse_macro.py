from tokenize import TokenInfo

from ast_def import Macro
from parse.parse_expression import parse_expression
from parse.parse_other import parse_identifier, parse_type
from parser_definition import Parser, dump


def expand_macro(parser: Parser) -> list[TokenInfo]:
    params = []
    macro_name_token = parser.lookahead_token()
    macro_name = parse_identifier(parser).data
    parser.expect("(")
    if parser.lookahead() == ")":
        parser.eat()
    else:
        while True:
            before_i = parser.i
            status, expr = parser.safe_wrap(lambda: parse_expression(parser))
            if not status:
                status, expr = parser.safe_wrap(lambda: parse_type(parser))
                if not status:
                    parser.syntax_error("expression or typed parameter")
            params.append(parser.tokens[before_i:parser.i])
            if parser.lookahead() == ",":
                parser.eat()
                continue
            parser.expect(")")
            break
    macro = parser.macros[macro_name]
    if len(macro.params) != len(params):
        parser.syntax_error(f"params inconsistency: {len(macro.params)} != {len(params)} for macro {macro_name}",
                            macro_name_token)
    param_to_expr = dict(zip(macro.params, params))
    expanded_content = []
    for token in macro.content:
        if param := param_to_expr.get(token.string):
            expanded_content += param
        else:
            expanded_content.append(token)
    # dump(expanded_content)
    return expanded_content


def expand_macros(parser: Parser) -> None:
    tmp = []
    i = parser.i
    while True:
        token = parser.lookahead_token()
        if token is None:
            break
        if token.string in parser.macros:
            e = expand_macro(parser)
            tmp += e
        else:
            tmp.append(token)
            parser.eat()
    parser.tokens[i:] = tmp
    parser.i = i


def parse_macro(parser: Parser) -> None:
    parser.expect('macro')
    params = []
    macro_name = parse_identifier(parser).data
    parser.expect("(")
    if parser.lookahead() == ")":
        parser.eat()
    else:
        while True:
            params.append(parse_identifier(parser).data)
            token = parser.lookahead()
            if token == ",":
                parser.eat()
                continue
            parser.expect(")")
            break
    macro_content = []
    current = parser.peek_token()
    while current.string != "end":
        macro_content.append(current)
        current = parser.peek_token()
    parser.macros[macro_name] = Macro(macro_name, params, macro_content)
