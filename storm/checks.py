from typing import Callable
import string as collection
from storm.utils import StrPaginator


class Checker(StrPaginator):
    def __init__(self, string: str) -> None:
        super().__init__(string)
        self.int_check: Callable[[], bool] = self.check_in(collection.digits)
        self.char_check: Callable[[], bool] = self.check_in(collection.ascii_letters)
