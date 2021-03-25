"""Some tools for working with requests."""

from common.debug_tools import log_function

@log_function
def parse_request(request, keys, optional_keys=None):
    """
    Parse given requests json data with given keys.

    If keys is iterable, return list with values from request.
    If keys is not iterable - treat it as a key
     and return one value by that key from request.
    """
    if not isinstance(keys, (list, tuple)):
        keys = [keys]

    if optional_keys is None:
        optional_keys = []
    if not isinstance(optional_keys, (list, tuple)):
        optional_keys = [optional_keys]

    request_data = request.get_json()
    if request_data is None:
        raise Exception('no json data')

    args = [request_data.get(key) for key in keys]
    missing_keys = [key for key, val in zip(keys, args) if val is None]
    if missing_keys:
        raise Exception(f"incomplete data: {' '.join(missing_keys)}")
    optional_args = [request_data.get(key) for key in optional_keys]

    return args + optional_args
