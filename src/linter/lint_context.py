from dataclasses import dataclass, field
from typing import Union

from ast_def import Param, Number, Identifier, BinOperator, UnaryOperator, Bool, Call, Expression
from b_type import BType

FunctionSignature = tuple[BType, list[Param]]


@dataclass
class LintContext:
    vars: dict[str, BType] = field(default_factory=dict)
    function_signatures: dict[str, FunctionSignature] = field(default_factory=dict)
    struct_signatures: dict[str, list[Param]] = field(default_factory=dict)

    def lint_error(self, got, expected, message: str = "") -> None:
        # console = Console(highlight=False, color_system="windows")
        # console.begin_capture()
        # opt_for = f"for {opt_for}" if opt_for else ""
        # console.print(f"expected {expected}, got {got} {opt_for}")
        assert 0, f"LintError: {message} expected `{expected}`, got `{got}`"

    def check(self, got, expected, message: str = "") -> None:
        if expected != got:
            self.lint_error(got, expected, message)


ExprType = Number | Identifier | BinOperator | UnaryOperator | Bool | Call | Expression
