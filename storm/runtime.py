import inspect
from typing import Optional, TextIO


class Scope(dict):
    def __init__(self, parent: Optional['Scope'] = None):
        super().__init__()
        self.__pointers__: dict = {}
        self.parent: Scope | None = parent

    def __getitem__(self, item):
        try:
            return dict.__getitem__(self, item)
        except KeyError:
            if self.parent:
                try:
                    return self.parent[item]
                except KeyError:
                    pass
            raise NameError(f'Unknown variable {item}')


def get_executor():
    frame = inspect.currentframe()
    while frame := frame.f_back:
        if inspect.getframeinfo(frame, 0).function == 'execute':
            return frame.f_locals['self']


def get_scope() -> Scope:
    return get_executor().scope


def get_stdout() -> TextIO:
    return get_executor().stdout
