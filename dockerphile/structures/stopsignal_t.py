from collections import namedtuple

from dockerphile.errors import DockerphileError


STOPSIGNAL_t = namedtuple('STOPSIGNAL', ['signal'])


def STOPSIGNAL(signal):
    """Create a Dockerfile STOPSIGNAL instruction.

    Args:
        signal: a string naming a valid signal identifier according to the
            Dockerfile STOPSIGNAL instruction specification.

    Returns:
        An instance of the STOPSIGNAL namedtuple.

    Raises:
        DockerphileError: raised for any errors when specifying `signal`.
    """
    msg = ''
    if not isinstance(signal, str):
        msg = 'STOPSIGNAL instruction signal requires string, not %s' % (
            type(signal)
        )
    if msg:
        raise DockerphileError(msg)
    return STOPSIGNAL_t(signal=signal)
