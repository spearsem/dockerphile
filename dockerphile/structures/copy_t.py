from collections import namedtuple

from dockerphile.errors import DockerphileError


COPY_t = namedtuple('COPY', ['resources', 'from_'])


def COPY(resources, from_=None):
    """Create a Dockerfile COPY instruction.

    Args:
        resources: A list or tuple of N strings (N >= 2) such that the
            first N - 1 are treated as COPY source URIs and the Nth is
            treated as the destination URI in the image being built. All
            URI strings will be enclosed with double-quote characters in
            the rendered Dockerfile.
        from_: Optional string naming a Docker image or index to specify a
            source image from which to copy when using multi-stage builds.

    Returns:
        An instance of the COPY namedtuple.

    Raises:
        DockerphileError: raised when `resources` or `from` arguments are not
            specified in a compatible way.
    """
    msg = ''
    if not isinstance(resources, (list, tuple)):
        msg = 'COPY instruction requires list or tuple, not %s' % (
            type(resources)
        )
    elif len(resources) < 2:
        msg = 'COPY instruction must have at least 1 src and 1 dest URI.'
    elif not isinstance(from_, (str, type(None))):
        msg = 'COPY --from option must be a string, not %s' % type(from_)
    if msg:
        raise DockerphileError(msg)
    return COPY_t(resources=resources, from_=from_)
