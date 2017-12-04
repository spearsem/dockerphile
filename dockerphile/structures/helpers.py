from dockerphile.errors import DockerphileError


def _check_format(instruction, arg, argname):
    """Helper to repeat argument validation for an instruction format."""
    msg = ''
    if not isinstance(arg, (list, tuple)):
        msg = '%s %s requires list or tuple of strings, not %s' % (
            instruction,
            argname,
            type(arg)
        )
    if not len(arg) >= 1:
        msg = '%s %s requires at least one parameter.' % (
            instruction,
            argname
        )
    if msg:
        raise DockerphileError(msg)
