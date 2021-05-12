"""Translate between db model and marshmallow schema objects."""

from functools import wraps


def transform_return(schema):
    """Transform return object into dict by given schema."""
    def _decorator(method):

        @wraps(method)
        def _wrapper(*args, **kargs):
            ret = method(*args, **kargs)
            if ret is None:
                return None
            if isinstance(ret, (list, tuple)):
                return [schema().dump(instance) for instance in ret]
            return schema().dump(ret)
        return _wrapper
    return _decorator
