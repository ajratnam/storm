from typing import Callable
from storm.collection import DIGITS
from storm.utils import StrPaginator


class Checker(StrPaginator):
    def __init__(self, string: str) -> None:
        super().__init__(string)
        self.int_check: Callable[[], bool] = self.check_in(DIGITS)
