from storm.tokens import Token
from storm.utils import StrPaginator, enforce_type


@enforce_type
def tokenize(string: str) -> list[Token]:
    return Tokenizer(string).parse()


class Tokenizer(StrPaginator):
    @enforce_type
    def __init__(self, string: str) -> None:
        self.tokens: list[Token] = []
        super().__init__(string)

    @enforce_type
    def parse(self) -> list[Token]:
        while self.not_reached_end:
            token = self.get_single_token()
            if token:
                self.tokens.append(token)
            else:
                self.goto_next_non_empty()
        return self.tokens
