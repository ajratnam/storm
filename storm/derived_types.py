from storm.converters import number
from storm.generic_types import *


class Number(Addable, Subtractable, Multipliable, Dividable, Object):
    value: float

    def __init__(self, value: Any) -> None:
        super().__init__(value)

    @staticmethod
    def _convert(value: Any) -> float:
        return number(value)

    def __add__(self, other: Object) -> 'Number':
        return Number(self.value + self._convert(other.value))

    def __radd__(self, other: Object) -> 'Number':
        return Number(self._convert(other.value) + self.value)

    def __sub__(self, other: Object) -> 'Number':
        return Number(self.value - self._convert(other.value))

    def __rsub__(self, other: Object) -> 'Number':
        return Number(self._convert(other.value) - self.value)

    def __mul__(self, other: Object) -> 'Number':
        return Number(self.value * self._convert(other.value))

    def __rmul__(self, other: Object) -> 'Number':
        return Number(self._convert(other.value) * self.value)

    def __div__(self, other: Object) -> 'Number':
        return Number(self.value / self._convert(other.value))

    def __rdiv__(self, other: Object) -> 'Number':
        return Number(self._convert(other.value) / self.value)

    @property
    def is_integer(self):
        return self.value.is_integer()

    def __repr__(self) -> str:
        value = str(self.value)
        return value[:-2] if self.is_integer else value
