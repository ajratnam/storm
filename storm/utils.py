from functools import wraps, reduce
from inspect import getfullargspec
from itertools import chain
from operator import or_
from types import GenericAlias, UnionType, NoneType
from typing import Callable, TypeVar, Sequence, Generic, Any, Union, Optional

DT = TypeVar('DT')


def enforce_type(func: Callable[..., DT]) -> Callable[..., DT]:
    spec = getfullargspec(func)
    get = spec.annotations.get
    name = func.__name__

    @wraps(func)
    def enforcer(*args, **kwargs) -> DT:
        for kwarg, value in chain(kwargs.items(), zip(spec.args, args)):
            if not check_instance(value, get(kwarg, object)):
                raise SystemError(f'Expected type {get(kwarg)} for parameter {kwarg} but got {get_type_repr(value)}')
        res = func(*args, **kwargs)
        if not check_instance(res, get('return', object)):
            raise SystemError(f'Expected return type {get("return")} for function {name} but got {get_type_repr(res)}')
        return res

    return enforcer


def get_type(obj: Any) -> type:
    obj_type = type(obj)
    if check_instance(obj, Sequence, str):
        types = tuple(get_type(elm) if elm is not obj else obj_type for elm in obj)
        return obj_type[reduce(or_, types)]
    return obj_type


def get_type_repr(obj: Any) -> str:
    if check_instance(obj, Sequence, str):
        return repr(get_type(obj))
    return get_type(obj).__name__


def check_instance(obj: Any, types: type | Sequence[type], not_types: Optional[type | Sequence[type]] = None) -> bool:
    if not_types and check_instance(obj, not_types):
        return False
    if isinstance(types, UnionType):
        types = types.__args__
    if isinstance(types, GenericAlias):
        origin = types.__origin__
        if not isinstance(obj, origin):
            return False
        if origin in [list, tuple, set]:
            obj: list | tuple | set
            for elm in obj:
                if not check_instance(elm, types.__args__):
                    return False
        else:
            raise NotImplementedError(f'Instance checking for type {origin} is not implemented yet')
    elif isinstance(types, type) or types in [Sequence]:
        if not isinstance(obj, types):
            return False
    elif isinstance(types, Sequence):
        for obj_type in types:
            if check_instance(obj, obj_type):
                return True
        return False
    else:
        raise NotImplementedError(f'Instance checking for type {types} is not implemented yet')
    return True


class Paginator(Generic[DT]):
    def __init__(self, obj: Sequence[DT]):
        self.obj: Sequence[DT] = obj
        self.index: int = 0

    def __next__(self) -> DT:
        return self.next()

    def next(self, num: int = 1) -> DT:
        self.index += num
        return self.obj[self.index]

    def prev(self, num: int = 1) -> DT:
        return self.next(-num)
