from collections import namedtuple

from dockerphile.errors import DockerphileError


VOLUME_t = namedtuple('VOLUME', ['volume_specs'])


def VOLUME(volume_specs):
    """Create a Dockerfile VOLUME instruction.

    Args:
        volume_specs: A list or tuple of strings each containing a valid
            Dockerfile volume specifier. The volume specifiers will be
            rendered in the JSON array format in resulting Dockerfiles
            and enclosed in double quotes.

    Returns:
        An instance of the VOLUME namedtuple.

    Raises:
        DockerphileError: raised when `volume_specs` argument is misspecified.
    """
    msg = ''
    if not isinstance(volume_specs, (list, tuple)):
        msg = 'VOLUME instruction requires list or tuple, not %s' % (
            type(volume_specs)
        )
    elif not volume_specs:
        msg = 'VOLUME instruction must have at least 1 volume specifier.'
    if msg:
        raise DockerphileError(msg)
    return VOLUME_t(volume_specs=volume_specs)
