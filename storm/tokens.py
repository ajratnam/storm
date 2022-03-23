from typing import Any


class TokenType:
    def __init__(self, name: str) -> None:
        self.name: str = name

    def __repr__(self) -> str:
        return f'<{self.name}>'


class Token:
    def __init__(self, token_type: TokenType, value: Any) -> None:
        self.type: TokenType = token_type
        self.value: Any = value

    @property
    def name(self) -> str:
        return self.type.name

    def __repr__(self) -> str:
        return f'<{self.name} value="{self.value}">'


class PrefixedToken(Token):
    def __init__(self, value: Token, prefix: str) -> None:
        super().__init__(PrefixedType, value)
        self.prefix: str = prefix

    def __repr__(self) -> str:
        return f'<{self.name} prefix="{self.prefix}" value="{self.value}">'


class SquashedOperatorToken(Token):
    def __init__(self, roperand: Token, operator: Token, loperand: Token) -> None:
        super().__init__(SquashedOperatorType, operator)
        self.loperand: Token = loperand
        self.roperand: Token = roperand

    def __repr__(self) -> str:
        return f'<{self.name} loperand={self.loperand} operator="{self.value}" right={self.roperand}>'


NumberType = TokenType('Number')
VariableType = TokenType('Variable')
OperatorType = TokenType('OperatorType')
PrefixType = TokenType('PrefixType')
PrefixedType = TokenType('Prefixed')
SquashedOperatorType = TokenType('SquashedOperator')
StringType = TokenType('String')
