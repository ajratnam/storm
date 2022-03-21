from abc import ABC
from typing import Generic, Any, TypeVar

from storm.errors import ReverseTypeError

DT = TypeVar('DT')


class Object(Generic[DT]):
    def __init__(self, value: DT):
        self._value: DT = self._convert(value)

    @property
    def value(self) -> DT:
        return self._value

    @value.setter
    def value(self, value: DT) -> None:
        self._value = value

    @value.deleter
    def value(self) -> None:
        raise AttributeError('Cannot be deleted')

    @staticmethod
    def _convert(value: Any) -> DT:
        return value

    def __add__(self, other: 'Object') -> 'Object':
        raise TypeError(f'Object {self.__class__.__name__} cannot be added')

    def __radd__(self, other: 'Object') -> 'Object':
        raise ReverseTypeError(f'Object {self.__class__.__name__} cannot be added in reverse')

    def __sub__(self, other: 'Object') -> 'Object':
        raise TypeError(f'Object {self.__class__.__name__} cannot be subtracted')

    def __rsub__(self, other: 'Object') -> 'Object':
        raise ReverseTypeError(f'Object {self.__class__.__name__} cannot be subtracted in reverse')

    def __mul__(self, other: 'Object') -> 'Object':
        raise TypeError(f'Object {self.__class__.__name__} cannot be multiplied')

    def __rmul__(self, other: 'Object') -> 'Object':
        raise ReverseTypeError(f'Object {self.__class__.__name__} cannot be multiplied in reverse')

    def __div__(self, other: 'Object') -> 'Object':
        raise TypeError(f'Object {self.__class__.__name__} cannot be divided')

    def __rdiv__(self, other: 'Object') -> 'Object':
        raise ReverseTypeError(f'Object {self.__class__.__name__} cannot be divided in reverse')

    def __repr__(self) -> str:
        return f'<{self.__class__.__name__} value={self.value}>'


class FrontAddable(Object):
    def __add__(self, other: Object) -> Object:
        raise NotImplementedError(f'Object {self.__class__.__name__} cannot be added')


class ReverseAddable(Object):
    def __radd__(self, other: Object) -> Object:
        raise NotImplementedError(f'Object {self.__class__.__name__} cannot be added in reverse')


class Addable(FrontAddable, ReverseAddable, ABC):
    pass


class FrontSubtractable(Object):
    def __sub__(self, other: Object) -> Object:
        raise NotImplementedError(f'Object {self.__class__.__name__} cannot be subtracted')


class ReverseSubtractable(Object):
    def __rsub__(self, other: Object) -> Object:
        raise NotImplementedError(f'Object {self.__class__.__name__} cannot be subtracted in reverse')


class Subtractable(FrontSubtractable, ReverseSubtractable, ABC):
    pass


class FrontMultipliable(Object):
    def __mul__(self, other: Object) -> Object:
        raise NotImplementedError(f'Object {self.__class__.__name__} cannot be multiplied')


class ReverseMultipliable(Object):
    def __rmul__(self, other: Object) -> Object:
        raise NotImplementedError(f'Object {self.__class__.__name__} cannot be multiplied in reverse')


class Multipliable(FrontMultipliable, ReverseMultipliable, ABC):
    pass


class FrontDividable(Object):
    def __div__(self, other: Object) -> 'Object':
        raise NotImplementedError(f'Object {self.__class__.__name__} cannot be divided')


class ReverseDividable(Object):
    def __rdiv__(self, other: Object) -> 'Object':
        raise NotImplementedError(f'Object {self.__class__.__name__} cannot be divided')


class Dividable(FrontDividable, ReverseDividable, ABC):
    pass
