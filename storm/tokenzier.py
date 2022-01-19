from storm.tokens import TokenType


class Token:
    def __init__(self, token_type: TokenType) -> None:
        self.type: TokenType = token_type

    @property
    def name(self) -> str:
        return self.type.name
