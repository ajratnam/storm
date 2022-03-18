from typing import Collection

from storm.checks import Checker
from storm.collection import OPERATORS
from storm.tokens import *
from storm.utils import StrPaginator, strip, extend


def tokenize(string: str) -> list[Token]:
    return Tokenizer(string).parse()


class Tokenizer(Checker, StrPaginator):
    def __init__(self, string: str) -> None:
        self.tokens: list[Token] = []
        super().__init__(string)

    def parse(self) -> list[Token]:
        while self.not_reached_end:
            token = self.get_token()
            if token:
                extend(self.tokens, token)
            self.move_to_next_non_empty()
        return self.tokens

    def get_token(self) -> Collection[Token] | Token | None:
        if self.int_check():
            return self.parse_number()
        elif self.char_check():
            return self.parse_variable()
        elif self.base_operator_check():
            return self.parse_operator()
        self.goto_next_non_empty()

    def parse_number(self) -> Token:
        value = ''
        while self.int_check():
            value += self.char
            self.goto_next_non_empty()
        return Token(IntegerType, int(value))

    def parse_variable(self) -> Token:
        value = ''
        while self.char_check():
            value += self.char
            self.goto_next_non_empty()
        return Token(VariableType, value)

    def parse_operator(self) -> Collection[Token] | Token:
        starting_index = self.index
        value = ''
        while self.base_operator_check():
            value += self.char
            self.goto_next_non_empty()
        other_operators = strip(value, '+-')
        if other_operators:
            if other_operators not in OPERATORS:
                raise SyntaxError(f"{value} is not an operator")
            value = other_operators + strip(value, other_operators)
        operator = ''
        if starting_index:
            for operator in OPERATORS:
                if value.startswith(operator):
                    break
        prefix = value[len(operator):]
        tokens = [operator and Token(OperatorType, operator), prefix and Token(PrefixType, prefix)]
        return strip(tokens, '')
