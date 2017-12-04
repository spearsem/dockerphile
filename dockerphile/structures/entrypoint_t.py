from collections import namedtuple

from dockerphile.errors import DockerphileError
from dockerphile.structures.helpers import _check_format


ENTRYPOINT_t = namedtuple('ENTRYPOINT', ['exec_form', 'shell_form'])


def ENTRYPOINT(exec_form=None, shell_form=None):
    """Create a Dockerfile ENTRYPOINT instruction.

    Docker ENTRYPOINT instructions have multiple forms that are rendered in
    different ways in Dockerfiles. This instruction can accept inputs that
    are compatible with each of the different ENTRYPOINT forms. Exception
    handling is performed to ensure that only one ENTRYPOINT format is
    specified in a single call to this ENTRYPOINT instruction, and that
    required properties of the input format are satisfied. When using the
    exec form of ENTRYPOINT inputs, the result is rendered as a JSON array
    of strings in any Dockerfile. For the shell form, the result is rendered
    as a series of unquoted literals directly following the ENTRYPOINT
    instruction.

    Args:
        exec_form: The exec form of input to the Dockerfile ENTRYPOINT
            instruction. This input must be a list or tuple of strings. The
            first entry specifies an executable and the remaining entries
            serve as the parameters to that executable.
        shell_form: The form of input to the ENTRYPOINT instruction that
            implicitly uses a shell context (not the Docker context) to execute
            an instruction with parameters. This argument must be a list or
            tuple of strings. The first entry must name an executable and the
            remaining entries serve as parameters.

    Returns:
        An instance of the ENTRYPOINT namedtuple.

    Raises:
        DockerphileError: raised for any errors when specifying the ENTRYPOINT
            form arguments.
    """
    kwargs = {"exec_form": exec_form, "shell_form": shell_form}
    if sum(v is not None for k, v in kwargs.items()) != 1:
        raise DockerphileError(
            'Exactly 1 ENTRYPOINT argument format must be used.'
        )
    for arg_name, arg_value in kwargs.items():
        if arg_value is not None:
            _check_format("ENTRYPOINT", arg_value, arg_name)
    return ENTRYPOINT_t(**kwargs)
