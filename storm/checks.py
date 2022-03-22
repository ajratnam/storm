from typing import Collection

from storm.collection import *
from storm.utils import Paginator


class Check:
    def __init__(self, parent: Paginator, container: Collection) -> None:
        self.container: Collection = container
        self.parent: Paginator = parent
        
    def __call__(self) -> bool:
        return bool(self.parent.obj) and self.parent.obj in self.container


class Checker(Paginator):
    def __init__(self, sequence: str) -> None:
        super().__init__(sequence)
        self.int_check: Check = Check(self, DIGITS)
        self.char_check: Check = Check(self, ALPHABETS)
        self.base_operator_check: Check = Check(self, BASE_OPERATORS)
        self.string_check: Check = Check(self, STRING_PARENS)
