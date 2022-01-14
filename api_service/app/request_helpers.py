"""Some helper methods."""

from functools import wraps
from typing import Iterable


def parse_request_args(request_proxy):
    """
    Parse arguments from request json data.

    Not compatible with *args and **kvargs in request signature.
    If called with arguments, does not pass them to the request.
    """

    def _decorator(method):
        @wraps(method)
        def _wrapper():
            request_data = request_proxy.get_json()
            if request_data and "access_token" in request_data:
                request_data.pop("access_token")
            return method(**request_data)

        return _wrapper

    return _decorator
