import inspect
from functools import wraps, reduce
from inspect import getfullargspec
from itertools import chain
from operator import or_
from types import GenericAlias, UnionType
from typing import Callable, TypeVar, Sequence, Any, Optional, Collection, Generic

DT = TypeVar('DT')


def enforce_type(func: Callable[..., DT]) -> Callable[..., DT]:
    spec = getfullargspec(func)
    get = spec.annotations.get
    name = func.__name__

    @wraps(func)
    def enforcer(*args, **kwargs) -> DT:
        for kwarg, value in chain(kwargs.items(), zip(spec.args, args)):
            if not check_instance(value, get(kwarg, object)):
                raise SystemError(f'Expected type {get(kwarg)} for parameter {kwarg} but got {get_type(value)}')
        res = func(*args, **kwargs)
        if not check_instance(res, get('return', object)):
            raise SystemError(f'Expected return type {get("return")} for function {name} but got {get_type(res)}')
        return res

    return enforcer


def get_type(obj: Any) -> type:
    obj_type = type(obj)
    if check_instance(obj, Sequence, str):
        types = tuple(get_type(elm) if elm is not obj else obj_type for elm in obj)
        return obj_type[reduce(or_, types)]
    elif check_instance(obj, Callable):
        signature = inspect.signature(obj)
        param_types = [typehint if (typehint := param.annotation) != inspect._empty else Any for param in signature.parameters.values()]
        return_type = RT if (RT := signature.return_annotation) != inspect._empty else Any
        return Callable[[*param_types], return_type]
    return obj_type


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
    elif isinstance(types, type) or types in [Sequence, Callable, Collection]:
        if not isinstance(obj, types):
            return False
    elif types is Any:
        pass
    elif isinstance(types, Sequence):
        for obj_type in types:
            if check_instance(obj, obj_type):
                return True
        return False
    elif isinstance(types, Callable):
        *args, return_type = types.__args__
        signature = inspect.signature(obj)
        if len(signature.parameters) != len(args) or signature.return_annotation != return_type:
            return False
        for parameter, param_type in zip(signature.parameters.values(), args):
            if parameter == inspect._empty or parameter.annotation != param_type:
                return False
    elif obj is None:
        if types is not None:
            return False
    else:
        raise NotImplementedError(f'Instance checking for type {types} is not implemented yet')
    return True


class Paginator(Generic[DT]):
    ctx: DT

    def __init__(self, sequence: Sequence[DT]) -> None:
        self.sequence: list = list(sequence)
        self._index: int = 0

    @property
    def index(self) -> int:
        return self._index

    @index.setter
    def index(self, index: int) -> None:
        self._index = -1 if index < 0 else len(self) if index > len(self) else index

    def __len__(self) -> int:
        return len(self.sequence)

    def __next__(self) -> DT:
        return self.next()

    def pop(self) -> DT:
        self.prev()
        return self.sequence.pop(self.index+1)

    @property
    def obj(self) -> DT:
        return self.sequence[self.index] if self.not_reached_end and self.index >= 0 else ''

    @obj.setter
    def obj(self, value) -> None:
        self.sequence[self.index] = value

    @property
    def not_reached_end(self) -> bool:
        return self.index < len(self.sequence)

    @property
    def reached_end(self) -> bool:
        return not self.not_reached_end

    def next(self, step: int = 1) -> DT:
        self.index += step
        return self.obj

    def prev(self, step: int = 1) -> DT:
        return self.next(-step)

    def goto_next_non_empty(self, step: int = 1) -> DT:
        while self.next(step).isspace():
            pass
        return self.obj

    def goto_prev_non_empty(self, step: int = 1) -> DT:
        return self.goto_next_non_empty(-step)

    def move_to_next_non_empty(self, step: int = 1) -> DT:
        while self.obj.isspace():
            self.next(step)
        return self.obj

    def move_to_prev_non_empty(self, step: int = 1) -> DT:
        return self.move_to_next_non_empty(-step)

    def move_while_condition(self, condition: Callable[[DT], bool], step: int = 1) -> DT:
        while condition(self.obj):
            return self.move_to_next_non_empty(step)


def strip(objs: Collection[DT], denied: Any) -> Collection[DT] | str:
    if not check_instance(denied, Collection) or not denied:
        denied = [denied]
    filtered = (obj for obj in objs if obj not in denied)
    if isinstance(objs, str):
        return ''.join(filtered)
    return list(filtered)


def extend(obj_list: list, new_val: Any) -> list:
    if isinstance(new_val, (list, tuple)):
        obj_list.extend(new_val)
    else:
        obj_list.append(new_val)
    return obj_list


def make_error(name: str) -> type:
    return type(name, (Exception,), {})
