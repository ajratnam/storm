from typing import Collection

from storm.collection import *
from storm.utils import StrPaginator


class Check:
    def __init__(self, parent: StrPaginator, container: Collection) -> None:
        self.container: Collection = container
        self.parent: StrPaginator = parent
        
    def __call__(self) -> bool:
        return bool(self.parent.char) and self.parent.char in self.container


class Checker(StrPaginator):
    def __init__(self, string: str) -> None:
        super().__init__(string)
        self.int_check: Check = Check(self, DIGITS)
        self.char_check: Check = Check(self, ALPHABETS)
        self.base_operator_check: Check = Check(self, BASE_OPERATORS)
