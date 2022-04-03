from math import modf, copysign
from typing import Literal

from storm.converters import *
from storm.generic_types import *
from storm.runtime import Scope, get_scope
from storm.utils import Substitute


class Number(Addable, Subtractable, Multipliable, Dividable, Negatable, Positable, Object):
    value: float

    def __init__(self, value: Any, convert: bool = False) -> None:
        super().__init__(value, convert)

    @property
    def value(self) -> float | int:
        return int(self._value) if self.is_integer() else self._value

    @staticmethod
    def _base_convert(value: Any) -> float:
        return number(value)

    @staticmethod
    def _convert(value: Any) -> float:
        return force_number(value)

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

    def __neg__(self) -> 'Number':
        return Number(-self.value)

    def __pos__(self) -> 'Number':
        return self

    def is_integer(self) -> bool:
        return self._value.is_integer()

    def reciprocal(self):
        return Number(1 / self.value)

    def __repr__(self) -> str:
        return str(self.value)


class String(Addable, Subtractable, Multipliable, Dividable, Negatable, Positable, Object):
    value: str

    def __init__(self, value: Any, convert: bool = False) -> None:
        super().__init__(value, convert)

    @staticmethod
    def _base_convert(value: Any) -> str:
        return string(value)

    @staticmethod
    def _convert(value: Any) -> str:
        return force_string(value)

    def __add__(self, other: Object) -> 'String':
        return String(self.value + self._convert(other.value))

    def __radd__(self, other: Object) -> 'String':
        return String(self._convert(other.value) + self.value)

    def __sub__(self, other: Object) -> 'String':
        return String(self.value.replace(self._convert(other.value), ''))

    def __rsub__(self, other: Object) -> 'String':
        return String(self._convert(other.value).replace(self.value, ''))

    def __mul__(self, other: Object) -> 'String':
        decimal, integer = modf(Number(other.value, True).value)
        value = self.value
        if copysign(1, integer) < 0:
            value = value[::-1]
        decimal, integer = abs(decimal), int(abs(integer))
        return String(value * integer + value[:int(len(value) * decimal)])

    def __rmul__(self, other: Object) -> 'String':
        decimal, integer = modf(Number(self.value, True).value)
        value = self._convert(other.value)
        if copysign(1, integer) < 0:
            value = value[::-1]
        decimal, integer = abs(decimal), int(abs(integer))
        return String(value * integer + value[:int(len(value) * decimal)])

    def __div__(self, other: Object) -> 'String':
        return self * Number(other.value, True).reciprocal()

    def __rdiv__(self, other: Object) -> 'String':
        return String(other.value) * Number(self, True).reciprocal()

    def __neg__(self) -> 'String':
        return String(self.value.lower())

    def __pos__(self) -> 'String':
        return String(self.value.upper())

    def __repr__(self) -> str:
        return self.value


class Pointer:
    def __init__(self, parent: 'Variable') -> None:
        self.parent: Variable = parent

    @property
    def value(self):
        return self
    
    @value.setter
    def value(self, value):
        self.parent.pointer = value

    def get(self) -> Object | Substitute:
        return self.parent.globals.get(self.parent.name, self.parent._value)

    @property
    def pointer(self):
        return self.get()

    def set(self, value: Object) -> None:
        if self.parent.unknown:
            self.parent._value.assign(value)
        else:
            self.parent.__set_val__(value)

    def fset(self, value: Object) -> None:
        self.parent.globals[self.parent.name] = value


class Variable:
    def __init__(self, name: str) -> None:
        self.name: str = name
        self._value: Substitute = Substitute(self)
        self.globals: Scope = get_scope()
        if not self.pointer:
            self.pointer: Pointer = Pointer(self)

    @property
    def pointer(self) -> Pointer | None:
        return self.globals.__pointers__.get(self.name)
    
    @pointer.setter
    def pointer(self, value: Pointer) -> None:
        self.globals.__pointers__[self.name] = value

    @property
    def value(self) -> Object | Substitute:
        return self.pointer.get()

    @value.setter
    def value(self, value: Object) -> None:
        self.pointer.set(value)

    @property
    def unknown(self):
        return self.value is not self._value

    def __set_val__(self, value: Object) -> None:
        self.pointer.fset(value)

    def __getattr__(self, attr: str) -> Any:
        return getattr(self.value, attr)

    def __repr__(self) -> str:
        return repr(self.value)
