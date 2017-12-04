from collections import namedtuple

from dockerphile.errors import DockerphileError
from dockerphile.structures.helpers import _check_format


CMD_t = namedtuple('CMD', ['exec_form', 'default_form', 'shell_form'])


def CMD(exec_form=None, default_form=None, shell_form=None):
    """Create a Dockerfile CMD instruction.

    Docker CMD instructions have multiple forms that are rendered in
    different ways in Dockerfiles. This instruction can accept inputs that
    are compatible with each of the different CMD forms. Exception handling
    is performed to ensure that only one CMD form is specified in a single
    call to this CMD instruction, and that required properties of the input
    format are satisfied. When using either the exec or default forms of CMD
    inputs, the result is rendered as a JSON array of strings in any
    Dockerfile. For the shell form, the result is rendered as a series of
    unquoted literals directly following the CMD instruction.

    Args:
        exec_form: The exec form of input to the Dockerfile CMD instruction.
            This input must be a list or tuple of strings. The first entry
            specifies an executable and the remaining entries serve as the
            parameters to that executable.
        default_form: The form of CMD instruction input that provides default
            parameters to the ENTRYPOINT of the Docker image. This form must
            also be a list or tuple or strings, but all entries are expected
            to be parameters (not executable) that are implicitly passed to
            the Docker image's ENTRYPOINT executable.
        shell_form: The form of input to the CMD instruction that implicitly
            uses a shell context (not the Docker context) to execute an
            instruction with parameters. This argument must be a list or tuple
            of strings. The first entry must name an executable and the
            remaining entries serve as parameters.

    Returns:
        An instance of the CMD namedtuple.

    Raises:
        DockerphileError: raised for any errors when specifying the CMD form
            arguments.

    """
    kwargs = {"exec_form": exec_form,
              "default_form": default_form,
              "shell_form": shell_form}
    if sum(v is not None for k, v in kwargs.items()) != 1:
        raise DockerphileError('Exactly 1 CMD argument format must be used.')
    for arg_name, arg_value in kwargs.items():
        if arg_value is not None:
            _check_format("CMD", arg_value, arg_name)
    return CMD_t(**kwargs)
