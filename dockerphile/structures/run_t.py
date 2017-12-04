from collections import namedtuple

from dockerphile.errors import DockerphileError
from dockerphile.structures.helpers import _check_format


RUN_t = namedtuple('RUN', ['shell_form', 'exec_form'])


def RUN(shell_form=None, exec_form=None):
    """Create a Dockerfile RUN instruction.

    Docker RUN instructions have multiple forms that are rendered in
    different ways in Dockerfiles. This instruction can accept inputs that
    are compatible with each of the different RUN forms. Exception
    handling is performed to ensure that only one RUN format is specified
    in a single call to this RUN instruction, and that required properties
    of the input format are satisfied. When using the exec form of RUN inputs,
    the result is rendered as a JSON array of strings in any Dockerfile. For
    the shell form, the result is rendered as a series of unquoted literals
    directly following the RUN instruction.

    Args:
        shell_form: The form of input to the RUN instruction that implicitly
            uses a shell context (not the Docker context) to execute an
            instruction with parameters. This argument must be a list or
            tuple of strings.
        exec_form: The exec form of input to the Dockerfile RUN instruction.
            This input must be a list or tuple of strings. The first entry
            specifies an executable and the remaining entries serve as the
            parameters to that executable.

    Returns:
        An instance of the RUN namedtuple.

    Raises:
        DockerphileError: raised for any errors when specifying the RUN form
            arguments.
    """
    kwargs = {"exec_form": exec_form, "shell_form": shell_form}
    if sum(v is not None for k, v in kwargs.items()) != 1:
        raise DockerphileError('Exactly 1 RUN argument format must be used.')
    for arg_name, arg_value in kwargs.items():
        if arg_value is not None:
            _check_format("RUN", arg_value, arg_name)
    return RUN_t(**kwargs)
