from storm.checks import Checker
from storm.tokens import Token, IntegerType
from storm.utils import StrPaginator


def tokenize(string: str) -> list[Token]:
    return Tokenizer(string).parse()


class Tokenizer(Checker, StrPaginator):
    def __init__(self, string: str) -> None:
        self.tokens: list[Token] = []
        super().__init__(string)

    def parse(self) -> list[Token]:
        while self.not_reached_end:
            token = self.get_single_token()
            if token:
                self.tokens.append(token)
            self.move_to_next_non_empty()
        return self.tokens

    def get_single_token(self) -> Token | None:
        if self.int_check():
            return self.parse_number()
        self.goto_next_non_empty()

    def parse_number(self) -> Token:
        value = []
        while self.int_check():
            value.append(self.char)
            self.goto_next_non_empty()
        return Token(IntegerType, int(''.join(value)))
