from typing import Collection

from storm.checks import Checker
from storm.collection import OPERATORS, OPERATOR_PRIORITY_ORDER
from storm.tokens import *
from storm.utils import Paginator, strip, extend


def tokenize(string: str) -> list[Token]:
    return Tokenizer(string).parse()


class Tokenizer(Checker, Paginator):
    def __init__(self, sequence: str) -> None:
        self.tokens: list[Token] = []
        super().__init__(sequence)

    def parse(self) -> list[Token]:
        while self.not_reached_end:
            token = self.get_token()
            if token:
                extend(self.tokens, token)
            self.move_to_next_non_empty()
        self.final_parse()
        return self.tokens

    def final_parse(self) -> None:
        self.combine_prefix()
        self.squash_operators()

    def combine_prefix(self) -> None:
        tokens = Paginator(self.tokens)
        while tokens.not_reached_end:
            if tokens.obj.type is PrefixType and tokens.next():
                tokens.obj = PrefixedToken(tokens.pop().value, tokens.obj.value)
            tokens.next()
        self.tokens = tokens.sequence

    def squash_operators(self) -> None:
        for operators in OPERATOR_PRIORITY_ORDER:
            tokens = Paginator(self.tokens)
            while tokens.not_reached_end:
                if tokens.obj.type is OperatorType and tokens.obj.value in operators and tokens.next():
                    tokens.obj = SquashedOperatorToken(tokens.pop(), tokens.pop().value, tokens.obj)
                tokens.next()
            self.tokens = tokens.sequence

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
            value += self.obj
            self.goto_next_non_empty()
        return Token(IntegerType, int(value))

    def parse_variable(self) -> Token:
        value = ''
        while self.char_check():
            value += self.obj
            self.goto_next_non_empty()
        return Token(VariableType, value)

    def parse_operator(self) -> Collection[Token] | Token:
        starting_index = self.index
        value = ''
        while self.base_operator_check():
            value += self.obj
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
