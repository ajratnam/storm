from typing import Any


class TokenType:
    def __init__(self, name: str) -> None:
        self.name: str = name


class Token:
    def __init__(self, token_type: TokenType, value: Any) -> None:
        self.type: TokenType = token_type
        self.value = value

    @property
    def name(self) -> str:
        return self.type.name

    def __repr__(self) -> str:
        return f'<{self.name} value={self.value}>'


IntegerType = TokenType('Integer')
