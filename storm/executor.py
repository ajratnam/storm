from storm.tokenzier import tokenize
from storm.utils import enforce_type


class Executor:
    @enforce_type
    def __init__(self, code: str) -> None:
        self.code: str = code

    def execute(self) -> None:
        tokens = tokenize(self.code)
        for token in tokens:
            parse(token)
