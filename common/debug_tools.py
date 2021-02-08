"""Usefull debug tools."""

import logging
from functools import wraps


def log_method(method):
    """Decorate method for logging its input and output."""
    @wraps(method)
    def _wrapper(*args, **kargs):
        # BUG self is not self
        name = method.__name__
        self = getattr(method, '__self__', None)
        if args:
            if self and args[0] == self:
                print_args = args[1:]
            else:
                print_args = args
        else:
            print_args = []
        input_data = f"{print_args}, {kargs}"
        logging.debug(f"{name} >>> {input_data}")
        ret = method(*args, **kargs)
        logging.debug(f"{name} <<< {input_data}; {ret}")
        return ret
    return _wrapper


def log_request(method):
    """Decorate flask request for logging ints input and output."""
    @wraps(method)
    def _wrapper(*args, **kargs):
        assert 'request' in method.__globals__, "no 'request' in globals of logged request"
        name = method.__name__
        print_args = {
            k: v for k, v in method.__globals__['request'].args.items()
        }
        logging.debug(f"{name} >>> {print_args} request")
        ret = method(*args, **kargs)
        logging.debug(f"{name} <<< {print_args}; {ret}")
        return ret
    return _wrapper
