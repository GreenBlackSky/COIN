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
    """Decorate flask request for logging ints input and output."""
    @wraps(method)
    def _wrapper(*args, **kargs):
        assert 'request' in method.__globals__, "no 'request' in globals of logged request"
        name = method.__name__
        request = method.__globals__['request']
        print_args = {}
        if request.headers:
            print_args['H'] = request.headers
        # if request.json:
        #     print_args['J'] = request.json
        if request.args:
            print_args['A'] = request.args
        logging.debug(f">>> {name} {print_args} request")
        try:
            ret = method(*args, **kargs)
            logging.debug(f"<<< {name} {ret}")
            return ret
        except Exception as e:
            logging.debug(f"<!< {name} {str(e)}")
            return {'status': 'error'}, 500
    return _wrapper
