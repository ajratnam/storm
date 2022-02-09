from typing import Any
from storm.utils import enforce_type


class TokenType:
    @enforce_type
    def __init__(self, name: str) -> None:
        self.name: str = name


class Token:
    @enforce_type
    def __init__(self, token_type: TokenType, value: Any) -> None:
        self.type: TokenType = token_type
        self.value = value

    @property
    @enforce_type
    def name(self) -> str:
        return self.type.name

    @enforce_type
    def __repr__(self) -> str:
        return f'<{self.name} value={self.value}>'


IntegerType = TokenType('Integer')
