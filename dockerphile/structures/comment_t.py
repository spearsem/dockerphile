from collections import namedtuple

from dockerphile.errors import DockerphileError


COMMENT_t = namedtuple('COMMENT', ['comment'])


def COMMENT(comment):
    """Create a Dockerfile comment line.

    Args:
        comment: a string containing a single line of comment text. `# `
            comment delimiter will be prepended when rendering the comment
            and so is unnecessary is the comment string. The string will
            be treated as a single line regardless of linebreaks or special
            characters inside.

    Returns:
        An instance of the COMMENT namedtuple.

    Raises:
        DockerphileError: raised for any errors when specifying `comment`.

    """
    msg = ''
    if not isinstance(comment, str):
        msg = 'COMMENT parameter `comment` requires string, not %s' % (
            type(comment)
        )
    if msg:
        raise DockerphileError(msg)
    return COMMENT_t(comment=comment)
