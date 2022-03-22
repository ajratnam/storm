from typing import Generator

from storm import tokens
from storm.generic_types import Object
from storm.handlers import handle_operation, handle_prefix
from storm.tokenzier import tokenize
from storm.derived_types import Number, String
from storm.utils import Paginator


class Executor(Paginator[tokens.Token]):
    def __init__(self, code: str) -> None:
        self.code: list[tokens.Token] = tokenize(code)
        super().__init__(self.code)

    def execute(self) -> Generator[Object | None, None, None]:
        while self.not_reached_end:
            yield self.parse(self.obj)
            self.next()

    def parse(self, token):
        match token.type:
            case tokens.NumberType:
                return Number(token.value)
            case tokens.SquashedOperatorType:
                token: tokens.SquashedOperatorToken
                left, right = self.parse(token.loperand), self.parse(token.roperand)
                return handle_operation(left, right, token.value)
            case tokens.PrefixedType:
                token: tokens.PrefixedToken
                return handle_prefix(self.parse(token.value), token.prefix)
            case tokens.StringType:
                return String(token.value)
            case other:
                raise ValueError(f'Execution for token type {other} not created!!')
