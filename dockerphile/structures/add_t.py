from collections import namedtuple

from dockerphile.errors import DockerphileError


ADD_t = namedtuple('ADD', ['resources'])


def ADD(resources):
    """Create a Dockerfile ADD instruction.

    Args:
        resources: A list or tuple of N strings (N >= 2) such that the
            first N - 1 are treated as ADD source URIs and the Nth is
            treated as the destination URI in the image being built. All
            URI strings will be enclosed with double-quote characters in
            the rendered Dockerfile.

    Returns:
        An instance of the ADD namedtuple.

    Raises:
        DockerphileError: raised when `resources` argument is not specified
            in a compatible way.

    """
    msg = ''
    if not isinstance(resources, (list, tuple)):
        msg = 'ADD instruction requires list or tuple, not %s' % type(
            resources
        )
    elif len(resources) < 2:
        msg = 'ADD instruction must have at least 1 src and 1 dest URI.'
    if msg:
        raise DockerphileError(msg)
    return ADD_t(resources=resources)
