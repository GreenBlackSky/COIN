"""Some tools for working with requests."""


def parse_request(request, keys):
    """
    Parse given requests json data with given keys.

    If keys is iterable, return list with values from request.
    If keys is not iterable - treat it as a key
     and return one value by that key from request.
    """
    request_data = request.get_json()
    if request_data is None:
        raise Exception('no json data')

    if isinstance(keys, (list, tuple)):
        ret = [request_data.get(key) for key in keys]
        missing_keys = [key for key, val in zip(keys, ret) if val is None]
        if missing_keys:
            raise Exception(f"incomplete data: {' '.join(missing_keys)}")
    else:
        ret = request_data.get(keys)
        if ret is None:
            raise Exception(f"incomplete data: {keys}")
    return ret
