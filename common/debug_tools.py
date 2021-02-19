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
        if print_args and kargs:
            input_data = f"{print_args}, {kargs}"
        elif print_args:
            input_data = print_args
        elif kargs:
            input_data = kargs
        else:
            input_data = ''
        logging.debug(f">>> {name} {input_data}")
        ret = method(*args, **kargs)
        logging.debug(f"<<< {name} {ret}")
        return ret
    return _wrapper


def log_request(method):
    """Decorate flask request for logging ints input and output."""
    @wraps(method)
    def _wrapper(*args, **kargs):
        assert 'request' in method.__globals__, "no 'request' in globals of logged request"
        name = method.__name__
        request = method.__globals__['request']
        print_args = {}
        if request.headers:
            print_args['H'] = request.headers
        if request.get_json():
            print_args['J'] = request.get_json()
        if request.args:
            print_args['A'] = request.args
        logging.debug(f">>> {name} {print_args} request")
        ret = method(*args, **kargs)
        logging.debug(f"<<< {name} {ret}")
        return ret
    return _wrapper
