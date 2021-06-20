"""Usefull debug tools."""

import logging
from functools import wraps


def log_function(function):
    """Decorate function for logging its input and output."""
    ret = function
    if __debug__:
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
        ret = _wrapper
    return ret


def log_method(method):
    """Decorate method of class for logging its input and output."""
    ret = method
    if __debug__:
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
        ret = _wrapper
    return ret


def log_request(request_proxy):
    """Request decorator."""
    def _decorator(method):
        ret = method
        if __debug__:
            @wraps(method)
            def _wrapper():
                name = method.__name__
                request_data = request_proxy.get_json()
                logging.debug(f">>> {name} {request_data} request")
                try:
                    ret = method()
                    logging.debug(f"<<< {name} {ret}")
                    return ret
                except Exception as e:
                    logging.debug(f"<!< {name} {str(e)}")
                    return {'status': 'error'}, 500
            ret = _wrapper
        return ret
    return _decorator
