"""Usefull debug tools."""

import logging
from functools import wraps


def log_method(method):
    """Decorate method for logging its input and output."""
    @wraps(method)
    def _wrapper(*args, **kargs):
        logging.debug(f"start {method.__name__}")
        ret = method(*args, **kargs)
        logging.debug(f"finish {method.__name__}")
        return ret
    return _wrapper
