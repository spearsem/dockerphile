from collections import namedtuple

from dockerphile.errors import DockerphileError


FROM_t = namedtuple('FROM', ['base_image', 'as_'])


def FROM(base_image, as_=None):
    """Create a Dockerfile FROM instruction.

    Args:
        base_image: A string naming a base Docker image. The string can contain
            references to pre-FROM ARG variables in accordance with Dockerfile
            support for ARG variables appearing in FROM instructions.
        as_: Optional string declaring a name for the image for later reference
            during a multi-stage build.

    Returns:
        An instance of the FROM namedtuple.

    Raises:
        DockerphileError: raised when `base_image` or `as_` arguments are
        misspecified.

    """
    msg = ''
    if not isinstance(base_image, str):
        msg = 'FROM parameter `base_image` requires string, not %s' % (
            type(base_image)
        )
    elif not isinstance(as_, (str, type(None))):
        msg = 'FROM parameter `as_` requires string, not %s' % (type(as_))
    if msg:
        raise DockerphileError(msg)
    return FROM_t(base_image=base_image, as_=as_)
