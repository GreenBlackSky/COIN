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


def wrap_request(*arg_names, optional_arg_names=None):
    """
    Request decorator.

    Parse given args from json data from request.
    Also, log input and output.
    """
    if optional_arg_names is None:
        optional_arg_names = []

    def _decorator(method):
        @wraps(method)
        def _wrapper():
            assert 'request' in method.__globals__, \
                "no 'request' in globals of logged request"
            name = method.__name__
            request = method.__globals__['request']

            request_data = request.get_json()
            if (arg_names or optional_arg_names) and request_data is None:
                logging.debug(f">>> {name} request")
                logging.debug(f"<!< {name} no json data")
                return {'status': 'error'}, 500

            args = [request_data.get(key) for key in arg_names]
            missing_keys = [
                key
                for key, val in zip(arg_names, args)
                if val is None
            ]
            if missing_keys:
                logging.debug(f">>> {name} request")
                logging.debug(
                    f"<!< {name} incomplete data: {' '.join(missing_keys)}"
                )
                return {'status': 'error'}, 500
            args += [request_data.get(key) for key in optional_arg_names]

            logging.debug(f">>> {name} {args} request")
            try:
                ret = method(*args)
                logging.debug(f"<<< {name} {ret}")
                return ret
            except Exception as e:
                logging.debug(f"<!< {name} {str(e)}")
                return {'status': 'error'}, 500
        return _wrapper

    return _decorator
