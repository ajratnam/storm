from storm.tokenzier import tokenize


class Executor:
    def __init__(self, code: str) -> None:
        self.code: str = code

    def execute(self) -> None:
        tokens = tokenize(self.code)
        for token in tokens:
            parse(token)
