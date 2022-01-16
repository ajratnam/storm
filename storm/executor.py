from storm.utils import enforce_type


class Executor:
    @enforce_type
    def __init__(self, code: str) -> None:
        self.code = code

    def execute(self):
        tokens = tokenize(self.code)
        for token in tokens:
            parse(token)
