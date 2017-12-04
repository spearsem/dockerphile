from collections import namedtuple

from dockerphile.errors import DockerphileError


USER_t = namedtuple('USER', ['user', 'group'])


def USER(user, group=None):
    """Create a Dockerfile USER instruction.

    Args:
        user: string containing username or UID for Dockerfile USER instruction.
        group: Optional string containing a group name or ID for the user.

    Returns:
        An instance of the USER namedtuple.

    Raises:
        DockerphileError: raised for any errors when specifying `user` or
        `group`.
    """
    msg = ''
    if not isinstance(user, str):
        msg = 'USER parameter `user` requires string, not %s' % type(user)
    elif not isinstance(group, (str, type(None))):
        msg = 'USER parameter `group` requires string, not %s' % type(group)
    if msg:
        raise DockerphileError(msg)
    return GROUP_t(user=user, group=group)
