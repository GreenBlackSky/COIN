"""Some tools for working with requests."""


def parse_request(request, keys):
    """Parse given requests json data with given keys."""
    request_data = request.get_json()
    if request_data is None:
        raise Exception('no json data')
    ret = []
    for key in keys:
        ret.append(request_data.get(key))
    if None in ret:
        missing_keys = [key for key, val in zip(keys, ret) if val is None]
        raise Exception(f"incomplete data: {' '.join(missing_keys)}")
    return ret
