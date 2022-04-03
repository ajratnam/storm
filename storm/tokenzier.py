from typing import Collection

from storm.checks import Checker
from storm.collection import OPERATORS, OPERATOR_PRIORITY_ORDER, PREFIXES
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
        self.fix_print()

    def combine_prefix(self) -> None:
        tokens = Paginator(self.tokens)
        while tokens.not_reached_end:
            if tokens.obj.type is PrefixType and tokens.next():
                tokens.obj = PrefixedToken(tokens.pop(), tokens.obj.value)
            tokens.next()
        self.tokens = tokens.sequence

    def squash_operators(self) -> None:
        for operators in OPERATOR_PRIORITY_ORDER:
            tokens = Paginator(self.tokens)
            while tokens.not_reached_end:
                if tokens.obj.type is OperatorType and tokens.obj.value in operators and tokens.next():
                    tokens.obj = SquashedOperatorToken(roper := tokens.pop(), tokens.pop().value, loper := tokens.obj)
                    if loper.type in UnOperatable:
                        for val in tokens.obj.value:
                            if val not in PREFIXES:
                                raise SyntaxError(f'Unknown Prefix {val}')
                        tokens.obj = PrefixedToken(roper, tokens.obj.value)
                        tokens.sequence.insert(tokens.index, loper)
                        tokens.next()
                    elif roper.type is UnOperatable:
                        raise SyntaxError(f'No roperand {loper.value}{tokens.obj.value}')
                tokens.next()
            self.tokens = tokens.sequence

    def fix_print(self) -> None:
        tokens = Paginator(self.tokens)
        while tokens.not_reached_end:
            if tokens.obj.type is PrintType and tokens.next():
                tokens.obj.value = tokens.pop()
            tokens.next()
        self.tokens = tokens.sequence

    def get_token(self) -> Collection[Token] | Token | None:
        if self.int_check():
            return self.parse_number()
        elif self.char_check():
            return self.parse_variable()
        elif self.print_check():
            return self.parse_print()
        elif self.base_operator_check():
            return self.parse_operator()
        elif self.prefix_check():
            return self.parse_prefix()
        elif self.string_check():
            return self.parse_string()
        elif self.line_break_check():
            return self.break_line()
        self.goto_next_non_empty()

    def break_line(self) -> Token:
        self.goto_next_non_empty()
        return Token(LineBreak, ';')

    def parse_number(self) -> Token:
        value = ''
        checks = [self.int_check, self.period_check]

        def check_decimal() -> bool:
            for pos, check in enumerate(checks):
                if check():
                    if pos > 0:
                        checks.pop(pos)
                    return True
            return False

        while check_decimal():
            value += self.obj
            self.goto_next_non_empty()
        return Token(NumberType, value)

    def parse_variable(self) -> Token:
        value = ''
        while self.char_check():
            value += self.obj
            self.goto_next_non_empty()
        return Token(VariableType, value)

    def parse_operator(self) -> Collection[Token] | Token:
        value = ''
        while self.base_operator_check():
            value += self.obj
            if value not in OPERATORS:
                value = value[:-1]
                break
            self.goto_next_non_empty()
        res = [Token(OperatorType, value), self.parse_prefix()]
        return strip(res, '')

    def parse_prefix(self) -> Token | str:
        value = ''
        while self.prefix_check():
            value += self.obj
            self.goto_next_non_empty()
        return value and Token(PrefixType, value)

    def parse_string(self) -> Token:
        value = ''
        starting_paren = self.obj
        while self.not_reached_end:
            self.next()
            value += self.obj
            if self.obj == starting_paren:
                self.goto_next_non_empty()
                if self.string_check():
                    value += self.parse_string().value
                return Token(StringType, value[:-1])
        else:
            raise SyntaxError("Unclosed string")

    def parse_print(self) -> Token:
        self.goto_next_non_empty(2)
        return Token(PrintType, None)
