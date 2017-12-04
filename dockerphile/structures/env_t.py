from collections import namedtuple


ENV_t = namedtuple('ENV', ['key', 'value'])


def ENV(key, value):
    """Create a Dockerfile ENV instruction.

    Args:
        key: string that names Dockerfile environment variable.
        value: string containing the environment variable value to set.

    Returns:
        An instance of the ENV namedtuple.

    Raises:
        DockerphileError: raised for any errors when specifying `key` or
        `value`.
    """
    msg = ''
    if not isinstance(key, str):
        msg = 'ENV instruction key requires string, not %s' % type(key)
    elif not isinstance(value, str):
        msg = 'ENV instruction value requires string, not %s' % type(value)
    if msg:
        raise DockerphileError(msg)
    return ENV_t(key=key, value=value)
