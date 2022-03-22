types = ['int', 'float', 'void', 'bool', 'byte']
special = types + ['for', 'while', 'if', 'func', 'struct', 'as']


class BType:
    @staticmethod
    def new(ctx: 'LintContext', s: str) -> 'BType':
        without_ptr = s.lstrip("*")
        assert without_ptr in types or without_ptr in ctx.struct_signatures and without_ptr.isidentifier(), s
        return BType(s)

    def __init__(self, s: str):
        without_ptr = s.lstrip("*")
        assert without_ptr.isidentifier(), without_ptr
        self.type = s

    def __str__(self):
        return self.type

    def __repr__(self):
        return str(self)

    def without_ptr(self) -> str:
        return self.type.lstrip("*")

    def is_struct(self):
        return self.without_ptr() not in types

    @property
    def cpp(self) -> str:
        without_ptr = self.without_ptr()
        n = len(self.type) - len(without_ptr)
        without_ptr = "char" if without_ptr == "byte" else without_ptr
        return without_ptr + "*" * n

    def __eq__(self, other) -> bool:
        return self.type == other.type

    def ref(self) -> 'BType':
        return BType("*" + self.type)

    def deref(self) -> 'BType':
        return BType(self.type[1:])

    def is_ref(self):
        return self.type[0] == "*"
