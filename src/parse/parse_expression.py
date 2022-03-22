from ast_def import Expression, Number, Bool, Identifier, BinOperator, UnaryOperator, bin_operators, \
    unary_operators, StringLiteral
from parse.parse_call import parse_call
from parser_definition import Parser


def unflatten_expression(expression: Expression) -> Expression:
    tmp = []
    to_skip = False
    current = expression.data
    i = len(current)
    for token in current[::-1]:
        i -= 1
        if type(token) == UnaryOperator:
            token.content = tmp.pop()
        tmp.append(token)
    tmp.reverse()
    current = tmp.copy()
    tmp.clear()
    for order in range(1, len(BinOperator.operators_order) + 1):
        for i, token in enumerate(current):
            if to_skip:
                to_skip = False
                continue
            # if type(token) == UnaryOperator and order == 0:
            #     to_skip = True
            #     next_token = current[i + 1]
            #     token.content = next_token
            if type(token) == BinOperator and token.order == order:
                to_skip = True
                assert len(current) > i + 1, current
                next_token = current[i + 1]
                token.content = [tmp.pop(), next_token]
            tmp.append(token)
        current = tmp.copy()
        tmp.clear()
    assert len(current) == 1, (current, expression.data, len(current))
    return Expression(current)


def parse_expression(parser: Parser) -> Expression:
    data = []
    while True:
        token = parser.lookahead_token()
        symbol = token.string
        if type(symbol) == Expression:  # macro expand. not very nice ??
            parser.eat()
            data.append(symbol)
        elif token.type == 3:  # escaped string
            parser.eat()
            data.append(StringLiteral(symbol[1:-1]))
        elif symbol == "(":
            parser.eat()
            data.append(parse_expression(parser))
            parser.expect(")")
        elif symbol.isdigit():
            data.append(Number(int(symbol)))
            parser.eat()
        elif symbol in ("true", "false"):
            data.append(Bool(symbol))
            parser.eat()
        elif symbol in unary_operators and (len(data) == 0 or type(data[-1]) in (BinOperator, UnaryOperator)):
            data.append(UnaryOperator(symbol))
            parser.eat()
        elif symbol in bin_operators and type(data[-1]) not in (BinOperator, UnaryOperator):
            data.append(BinOperator(symbol))
            parser.eat()
        elif symbol == "[":
            parser.eat()
            data.append(BinOperator("[]"))
            data.append(parse_expression(parser))
            parser.expect("]")
        elif symbol.isidentifier() and parser.lookahead(1) == '(':
            data.append(parse_call(parser))
        elif symbol.isidentifier() and parser.lookahead(1) != '(':
            data.append(Identifier(symbol))
            parser.eat()
        elif (next_token := parser.lookahead(1)) is not None and \
                symbol + next_token in bin_operators and \
                symbol + next_token not in (BinOperator, UnaryOperator):
            data.append(BinOperator(symbol + next_token))
            parser.eat()
            parser.eat()
        elif symbol in (",", "]", ")", "}", "{", "=", ";"):
            return unflatten_expression(Expression(data))
        else:
            parser.syntax_error("expected expression", token)
