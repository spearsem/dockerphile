from collections import namedtuple

from dockerphile.errors import DockerphileError


WORKDIR_t = namedtuple('WORKDIR', ['workdir'])


def WORKDIR(workdir):
    """Create a Dockerfile WORKDIR instruction.

    Args:
        workdir: a string naming a valid path identifier according to the
            Dockerfile WORKDIR instruction specification.

    Returns:
        An instance of the WORKDIR namedtuple.

    Raises:
        DockerphileError: raised for any errors when specifying `workdir`.

    """
    msg = ''
    if not isinstance(workdir, str):
        msg = 'WORKDIR parameter `workdir` requires string, not %s' % (
            type(workdir)
        )
    if msg:
        raise DockerphileError(msg)
    return WORKDIR_t(workdir=workdir)
