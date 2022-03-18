from typing import Sequence

from storm.tokens import Token
from storm.tokenzier import tokenize
from storm.utils import check_instance


class Executor:
    def __init__(self, code: str | Sequence[Token]) -> None:
        self.code: str | Sequence[Token] = code

    def tokenize(self) -> None:
        if not check_instance(self.code, Sequence[Token]):
            self.code = tokenize(self.code)

    def execute(self) -> None:
        self.tokenize()
        for token in self.code:
            self.parse(token)

    def parse(self):
        pass
