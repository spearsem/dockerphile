from collections import namedtuple

from dockerphile.errors import DockerphileError
from dockerphile.structures.add_t import ADD_t
from dockerphile.structures.arg_t import ARG_t
from dockerphile.structures.cmd_t import CMD_t
from dockerphile.structures.copy_t import COPY_t
from dockerphile.structures.entrypoint_t import ENTRYPOINT_t
from dockerphile.structures.env_t import ENV_t
from dockerphile.structures.expose_t import EXPOSE_t
from dockerphile.structures.healthcheck_t import HEALTHCHECK_t
from dockerphile.structures.label_t import LABEL_t
from dockerphile.structures.run_t import RUN_t
from dockerphile.structures.shell_t import SHELL_t
from dockerphile.structures.stopsignal_t import STOPSIGNAL_t
from dockerphile.structures.user_t import USER_t
from dockerphile.structures.volume_t import VOLUME_t
from dockerphile.structures.workdir_t import WORKDIR_t


ONBUILD_t = namedtuple('ONBUILD', ['instruction'])
VALID_TYPES = (ADD_t, ARG_t, CMD_t, COPY_t, ENTRYPOINT_t, ENV_t, EXPOSE_t,
               HEALTHCHECK_t, LABEL_t, RUN_t, SHELL_t, STOPSIGNAL_t, USER_t,
               VOLUME_t, WORKDIR_t)


def ONBUILD(instruction):
    """Create a Dockerfile ONBUILD instruction.

    ONBUILD instructions must be instances of valid dockerphile types that are
    permitted to serve as an ONBUILD parameter in a Dockerfile. For example, if
    you seek to trigger a COPY instruction with an ONBUILD trigger, then you
    must create an instance of `dockerphile.structures.copy_t.COPY_t`, and pass
    this object as the instruction argument to ONBUILD. Note that FROM_t,
    COMMENT_t and ONBUILD_t are not valid parameters for ONBUILD, and these
    result in exceptions. Additionally, since ESCAPE maps to a parser directive,
    not a instruction, and it must appear in a Dockerfile prior to any
    instructions, ESCAPE is also considered invalid for ONBUILD.

    Args:
        instruction: An instance of a valid dockerphile instruction. FROM and
            ONBUILD are invalid to appear as the parameter for an ONBUILD
            instruction, but any other Dockerfile instruction can appear. Since
            COMMENT and ESCAPE do not refer to triggerable instructions, they
            are also not part of the valid instruction set for ONBUILD.

    Returns:
        An instance of the ONBUILD namedtuple.

    Raises:
        DockerphileError: raised if `instruction` is a dockerphile instruction
            type that is invalid for ONBUILD or if `instruction` is not an
            instance of a dockerphile instruction.
    """
    msg = ''
    if not isinstance(instruction, VALID_TYPES):
        msg = 'ONBUILD instruction parameter received disallowed type %s.' % (
            type(instruction)
        )
    if msg:
        raise DockerphileError(msg)
    return ONBUILD_t(instruction=instruction)
