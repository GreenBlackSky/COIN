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


def log_request(request_proxy, user_proxy=None):
    """
    Log flask request input and output.

    Must be before any arguments handling.
    """
    def _decorator(method):
        if __debug__:
            name = method.__name__

            def log_input(print_user):
                request_data = request_proxy.get_json()
                if request_data and 'access_token' in request_data:
                    request_data.pop('access_token')
                logging.debug(f">>> {name} {request_data} as {print_user}")

            def log_output(print_user, ret):
                if isinstance(ret, dict):
                    print_ret = {
                        k: v for k, v in ret.items()
                        if k != 'access_token'
                    }
                elif isinstance(ret, tuple):
                    print_ret = {
                        k: v for k, v in ret[0].items()
                        if k != 'access_token'
                    }
                else:
                    print_ret = ret
                logging.debug(f"<<< {name} {print_ret} as {print_user}")

            def log_exception(print_user, e):
                logging.debug(f"<!< {name} {str(e)} as {print_user}")

            @wraps(method)
            def _wrapper(*args, **kargs):
                print_user = f"{user_proxy.id} ({user_proxy.name})" \
                    if user_proxy else \
                    'anonymous'
                log_input(print_user)
                try:
                    ret = method(*args, **kargs)
                    log_output(print_user, ret)
                    return ret
                except Exception as e:
                    log_exception(print_user, e)
                    return {'status': 'error'}, 500
            return _wrapper

        return method
    return _decorator
