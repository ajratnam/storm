from typing import Callable

from storm.derived_types import *
from storm.errors import ReverseTypeError


def handle_operation(left: Object, right: Object, operator: str) -> Object:
    handler: Callable[[Object, Object], Object] | None = operation_mapping.get(operator)
    if handler:
        return handler(left, right)
    raise NotImplementedError(f'Unknown Operator "{operator}"')


def do_reversible_operation(left: Object, right: Object, operation: str) -> Object:
    try:
        return getattr(left, f'__{operation}__')(right)
    except Exception as FirstException:
        try:
            return getattr(right, f'__r{operation}__')(left)
        except (NotImplementedError, ReverseTypeError):
            raise FirstException


def add(left: Addable, right: Object) -> Object:
    return do_reversible_operation(left, right, 'add')


def subtract(left: Subtractable, right: Object) -> Object:
    return do_reversible_operation(left, right, 'sub')


def multiply(left: Multipliable, right: Object) -> Object:
    return do_reversible_operation(left, right, 'mul')


def divide(left: Dividable, right: Object) -> Object:
    return do_reversible_operation(left, right, 'div')


def handle_prefix(obj: Object, prefixes: str) -> Object:
    for prefix in prefixes:
        handler: Callable[[Object], Object] | None = prefix_mapping.get(prefix)
        if not handler:
            raise NotImplementedError(f'Unknown Prefix "{prefix}"')
        obj = handler(obj)
    return obj


def posite(obj: Object) -> Object:
    return obj.__pos__()


def negate(obj: Object) -> Object:
    return obj.__neg__()


operation_mapping = {
    '+': add,
    '-': subtract,
    '*': multiply,
    '/': divide
}

prefix_mapping = {
    '+': posite,
    '-': negate
}
