from collections import namedtuple

from dockerphile.errors import DockerphileError


LABEL_t = namedtuple('LABEL', ['key', 'value'])


def LABEL(key, value):
    """Create a Dockerfile LABEL instruction.

    Args:
        key: string that names Dockerfile label key.
        value: string containing the label value to set.

    Returns:
        An instance of the LABEL namedtuple.

    Raises:
        DockerphileError: raised for any errors when specifying `key` or
        `value`.

    """
    msg = ''
    if not isinstance(key, str):
        msg = 'LABEL instruction key requires string, not %s' % type(key)
    elif not isinstance(value, str):
        msg = 'LABEL instruction value requires string, not %s' % type(value)
    if msg:
        raise DockerphileError(msg)
    return LABEL_t(key=key, value=value)
