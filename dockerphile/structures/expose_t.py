from collections import namedtuple

from dockerphile.errors import DockerphileError


EXPOSE_t = namedtuple('EXPOSE', ['port_specs'])


def EXPOSE(port_specs):
    """Create a Dockerfile EXPOSE instruction.

    Args:
        port_specs: A list or tuple of strings each containing a valid
            Dockerfile port/protocol specifier.

    Returns:
        An instance of the EXPOSE namedtuple.

    Raises:
        DockerphileError: raised when `port_specs` argument is misspecified.

    """
    msg = ''
    if not isinstance(port_specs, (list, tuple)):
        msg = 'EXPOSE instruction requires list or tuple, not %s' % (
            type(port_specs)
        )
    elif not port_specs:
        msg = 'EXPOSE instruction must have at least 1 port specifier.'
    if msg:
        raise DockerphileError(msg)
    return EXPOSE_t(port_specs=port_specs)
