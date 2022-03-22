from __future__ import annotations

from dataclasses import dataclass, field
from tokenize import TokenInfo
from typing import Union

import b_type


@dataclass
class Param:
    type: b_type.BType
    name: str


@dataclass
class StringLiteral:
    data: str


@dataclass
class Macro:
    name: str
    params: list[str]
    content: list[TokenInfo]


class Block:
    pass


@dataclass
class Function:
    function_name: str
    return_type: b_type.BType
    params: list[Param]
    block: Block


@dataclass
class Struct:
    struct_name: str
    fields: list[Param]


class Expression:
    pass


@dataclass
class VariableDeclaration:
    var_type: b_type.BType
    var_name: str
    expr: Expression
    tokens: list[TokenInfo] = field(default_factory=list, repr=False)


@dataclass
class Return:
    expr: Expression
    tokens: list[TokenInfo] = field(default_factory=list, repr=False)


@dataclass
class Assign:
    assign_to: Expression
    expr: Expression
    tokens: list[TokenInfo] = field(default_factory=list, repr=False)


@dataclass
class Condition:
    expr: Expression
    block: Block
    tokens: list[TokenInfo] = field(default_factory=list, repr=False)


@dataclass
class Loop:
    expr: Expression
    block: Block
    tokens: list[TokenInfo] = field(default_factory=list, repr=False)


@dataclass
class SquareBracketOperator:
    data: Expression


@dataclass
class Identifier:
    data: str


@dataclass
class Number:
    data: int


class BinOperator:
    operators_order = [("and", "or"), ("==", "!="), ("<", "<=", ">", ">="), ("+", "-"), ('*', '/'), ('as',), ('.',),
                       ('[]',)]

    def __init__(self, data: str):
        self.data = data
        self.content = []
        self.type: b_type.BType = None
        self.order = None
        for i, operators in enumerate(list(reversed(self.operators_order))):
            if data in operators:
                self.order = i + 1
                break
        if self.order is None:
            assert 0, data

    def __repr__(self):
        return str(self)

    def __str__(self):
        return f'BinOperator -> {self.type.type if self.type else None}({self.data}, {self.content})'


@dataclass
class UnaryOperator:
    data: str
    content: Union[Expression, None] = None
    order: int = field(repr=False, default=0)
    type: b_type.BType = field(default=None)


def is_operator(token) -> bool:
    return type(token) in (UnaryOperator, BinOperator)


@dataclass
class Bool:
    data: str


@dataclass
class Call:
    name: str
    params: list[Expression]
    type: b_type.BType = field(default=None)


@dataclass
class Expression:
    data: list[Number | Identifier | BinOperator | UnaryOperator | Bool | Call | Expression]


@dataclass
class Block:
    statements: list[VariableDeclaration | Return | Assign | Condition | Loop | Expression]


@dataclass
class Program:
    structs: list[Struct] = field(default_factory=list)
    functions: list[Function] = field(default_factory=list)


bin_operators = ("[]", ".", "*", "/", "+", "-", "<", "<=", ">", ">=", "==", "!=", "and", "or", "as")

unary_operators = ("-", "!", "*")
