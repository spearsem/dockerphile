from collections import namedtuple

from dockerphile.errors import DockerphileError


SHELL_t = namedtuple('SHELL', ['shell_spec'])


def SHELL(shell_spec):
    """Create a Dockerfile SHELL instruction.

    Args:
        shell_spec: A list or tuple of strings together containing a
            JSON / exec formatted shell executable to be set via the
            Dockerfile SHELL instruction.

    Returns:
        An instance of the SHELL namedtuple.

    Raises:
        DockerphileError: raised when `shell_spec` argument is misspecified.
    """
    msg = ''
    if not isinstance(shell_spec, (list, tuple)):
        msg = 'SHELL instruction requires list or tuple, not %s' % (
            type(shell_spec)
        )
    elif not shell_spec:
        msg = 'SHELL instruction parameter must have at least 1 entry.'
    if msg:
        raise DockerphileError(msg)
    return SHELL_t(shell_spec=shell_spec)
