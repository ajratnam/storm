from functools import wraps
from inspect import getfullargspec
from itertools import chain
from typing import Callable, TypeVar

RT = TypeVar('RT')


def enforce_type(func: Callable[..., RT]) -> Callable[..., RT]:
    spec = getfullargspec(func)
    get = spec.annotations.get

    @wraps(func)
    def enforcer(*args, **kwargs) -> RT:
        for kwarg, value in chain(kwargs.items(), zip(spec.args, args)):
            if not isinstance(value, get(kwarg, object)):
                raise SystemError('Got unexpected type')
        res = func(*args, **kwargs)
        if not isinstance(res, get('return', object)):
            raise SystemError('Returned unexpected type')
        return res

    return enforcer
