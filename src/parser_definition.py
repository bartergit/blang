from __future__ import annotations

from dataclasses import dataclass, field
from tokenize import TokenInfo
from typing import Callable, Any

from rich.console import Console

from ast_def import Macro


def dump(tokens: list[TokenInfo]) -> None:
    print([x.string for x in tokens])


@dataclass
class Parser:
    i: int
    tokens: list[TokenInfo]
    macros: dict[str, Macro] = field(default_factory=dict)

    def syntax_error(self, expected: Any, got_token: TokenInfo = None):
        got_token = got_token or self.lookahead_token()
        console = Console(highlight=False, color_system="windows")
        start_row, start_col = got_token.start
        _, end_column = got_token.end
        before, exact, after = got_token.line[:start_col], \
                               got_token.line[start_col:end_column], \
                               got_token.line[end_column:]
        console.begin_capture()
        console.print(
            f"Syntax error: at line {start_row} expected: [b green]{expected}[/b green], got [b red]{got_token.string}[/b red]")
        console.print("\t" + f"{before}[b red]{exact}[/b red]{after}".strip())
        assert 0, console.end_capture()

    def safe_wrap(self, function: Callable) -> tuple[bool, Any]:
        before_i = self.i
        try:
            return True, function()
        except AssertionError:
            self.i = before_i
            return False, None

    def expect(self, *args) -> None:
        for expected in args:
            got = self.tokens[self.i]
            if expected != got.string:
                self.syntax_error(expected, got)
            # f"{self.tokens[self.i:]}"
            self.i += 1

    def peek_token(self) -> TokenInfo:
        if self.i >= len(self.tokens):
            assert 0, "unexpected end of file"
        token = self.tokens[self.i]
        self.i += 1
        return token

    def peek(self) -> str:
        return self.peek_token().string

    def lookahead(self, n=0) -> str:
        if (token := self.lookahead_token(n)) is not None:
            return token.string

    def lookahead_token(self, n=0) -> TokenInfo:
        ind = self.i + n
        return self.tokens[ind] if ind < len(self.tokens) else None

    def eat(self) -> None:
        self.i += 1
