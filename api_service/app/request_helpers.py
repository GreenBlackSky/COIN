"""Some helper methods."""

from functools import wraps


def parse_request_args(request_proxy, arg_names=None, kargs_names=None):
    """Parse arguments from json part of request."""
    request_data = request_proxy.get_json()
    if (
        (arg_names is not None or kargs_names is not None)
        and request_data is None
    ):
        raise Exception(f"no json data")

    args, kargs = [], {}
    if arg_names:
        args = [request_data.get(key) for key in arg_names]
    if kargs_names:
        kargs = {
            key: request_data.get(key, default)
            for key, default in kargs_names.items()
        }

    missing_keys = []
    if arg_names:
        missing_keys = [
            key
            for key, val in zip(arg_names, args)
            if val is None
        ]

    if missing_keys:
        raise Exception(
            f"incomplete request data: {' '.join(missing_keys)}"
        )
    # kargs have default values and might be missing, no biggie

    return args, kargs
