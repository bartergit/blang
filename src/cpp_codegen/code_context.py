from dataclasses import dataclass, field


@dataclass
class CodeContext:
    listing: list[str] = field(default_factory=list)
    parameters: list[str] = field(default_factory=list)
    reg_counter: int = 0

    def add(self, s: str) -> None:
        self.listing.append(s)

    def add_reg(self):
        self.reg_counter += 1
        return self.reg

    @property
    def reg(self):
        return "r" + str(self.reg_counter)

    def pop(self):
        return self.parameters.pop()
