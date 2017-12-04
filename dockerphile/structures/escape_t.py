from collections import namedtuple

from dockerphile.errors import DockerphileError


ESCAPE_t = namedtuple('ESCAPE', ['character'])


def ESCAPE(character):
    """Create a Dockerfile `# escape` parser directive.

    Args:
        character: a single-character string naming a valid character to serve
            as the escape character according to the `escape` parser directive
            specification for Dockerfiles.

    Returns:
        An instance of the ESCAPE namedtuple.

    Raises:
        DockerphileError: raised for any errors when specifying `character`.

    """
    msg = ''
    if not isinstance(character, str):
        msg = 'ESCAPE parameter must be a string, not %s' % (
            type(character)
        )
    elif len(character) != 1:
        msg = 'ESCAPE parameter must contain exactly 1 character.'
    if msg:
        raise DockerphileError(msg)
    return ESCAPE_t(character=character)
