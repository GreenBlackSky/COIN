"""Usefull debug tools."""

import logging
from functools import wraps


def log_function(function):
    """Decorate function for logging its input and output."""
    @wraps(function)
    def _wrapper(*args, **kargs):
        name = function.__name__
        if args and kargs:
            input_data = f"{args}, {kargs}"
        elif args:
            input_data = args
        elif kargs:
            input_data = kargs
        else:
            input_data = ''
        logging.debug(f">>> {name} {input_data}")
        try:
            ret = function(*args, **kargs)
            logging.debug(f"<<< {name} {ret}")
            return ret
        except Exception as e:
            logging.debug(f"<!< {name} {str(e)}")
            raise e
    return _wrapper


def log_method(method):
    """Decorate method of class for logging its input and output."""
    @wraps(method)
    def _wrapper(self, *args, **kargs):
        name = type(self).__name__ + '.' + method.__name__
        if args and kargs:
            input_data = f"{args}, {kargs}"
        elif args:
            input_data = args
        elif kargs:
            input_data = kargs
        else:
            input_data = ''
        logging.debug(f">>> {name} {input_data}")
        try:
            ret = method(self, *args, **kargs)
            logging.debug(f"<<< {name} {ret}")
            return ret
        except Exception as e:
            logging.debug(f"<!< {name} {str(e)}")
            raise e
    return _wrapper


def log_request(method):
    """Request decorator."""
    @wraps(method)
    def _wrapper(*args, **kargs):
        name = method.__name__
        logging.debug(f">>> {name} {args} {kargs} request")
        try:
            ret = method(*args, **kargs)
            logging.debug(f"<<< {name} {ret}")
            return ret
        except Exception as e:
            logging.debug(f"<!< {name} {str(e)}")
            return {'status': 'error'}, 500
    return _wrapper
