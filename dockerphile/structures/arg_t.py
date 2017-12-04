from collections import namedtuple

from dockerphile.errors import DockerphileError


ARG_t = namedtuple('ARG', ['key', 'default_value'])


def ARG(key, default_value=None):
    """Create a Dockerfile ARG instruction.

    Args:
        key: string that names the Dockerfile build ARG.
        default_value: string supplying the ARG default value (e.g. `key=value`)
            in the Dockerfile.

    Returns:
        An instance of the ARG namedtuple.

    Raises:
        DockerphileError: raised for any errors when specifying `key` or
        `default_value`.
    """
    msg = ''
    if not isinstance(key, str):
        msg = 'ARG instruction key requires string, not %s' % type(key)
    elif not isinstance(default_value, (str, type(None))):
        msg = 'ARG instruction default_value requires string, not %s' % (
            type(default_value)
        )
    if msg:
        raise DockerphileError(msg)
    return ARG_t(key=key, default_value=default_value)
