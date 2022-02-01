from storm.utils import enforce_type


class TokenType:
    @enforce_type
    def __init__(self, name: str) -> None:
        self.name: str = name


class Token:
    @enforce_type
    def __init__(self, token_type: TokenType) -> None:
        self.type: TokenType = token_type

    @property
    def name(self) -> str:
        return self.type.name
