from ast_def import Block, Return
from parse.parse_expression import parse_expression
from parse.statement.assign import parse_assign
from parse.statement.condition import parse_if
from parse.statement.declaration import parse_declaration
from parse.statement.loop import parse_while
from parser_definition import Parser, dump


def parse_block(parser: Parser) -> Block:
    parser.expect('{')
    statements = []
    while True:
        before_i = parser.i
        current = parser.lookahead()
        if current == ";":
            parser.eat()
        elif current == "}":
            parser.eat()
            return Block(statements)
        elif current == "if":
            statements.append(parse_if(parser))
        elif current == "while":
            statements.append(parse_while(parser))
        elif current == "return":
            parser.eat()
            ret = Return(parse_expression(parser))
            statements.append(ret)
            parser.expect(";")
        else:
            def expr_lambda():
                expr = parse_expression(parser)
                parser.expect(";")
                return expr

            for f in (lambda: parse_declaration(parser), lambda: parse_assign(parser), expr_lambda):
                status, statement = parser.safe_wrap(f)
                if status:
                    statements.append(statement)
                    break
            if not status:
                # dump(parser.tokens[parser.i:])
                parser.syntax_error("statement")
        statements[-1].tokens = parser.tokens[before_i:parser.i]
