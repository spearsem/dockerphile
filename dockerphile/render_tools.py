import json

from dockerphile import structures
from dockerphile.errors import DockerphileError


def render_instruction(instruction):
    """Render a string format of a dockerphile instruction.

    Args:
        instruction: A dockerphile instruction type from dockerphile.structures.

    Returns:
        A string containing the rendered output of the given instruction.

    Raises:
        DockerphileError: raised when the input is not a valid dockerphile
            instruction type.
    """
    if isinstance(instruction, structures.ADD_t):
        result = "ADD"
        for resource in instruction.resources:
            result = result + ' "%s"' % resource
        return result
    if isinstance(instruction, structures.ARG_t):
        result = "ARG %s" % instruction.key
        if instruction.default_value is not None:
            result = result + "=%s" % default_value
        return result
    if isinstance(instruction, structures.CMD_t):
        result = "CMD"
        if instruction.shell_form is not None:
            for c in instruction.shell_form:
                result = result + " %s" % c
            return result
        elif instruction.exec_form is not None:
            commands = json.dumps(instruction.exec_form)
        else:
            commands = json.dumps(instruction.default_form)
        return result + " " + commands
    if isinstance(instruction, structures.COMMENT_t):
        return "# %s" % instruction.comment
    if isinstance(instruction, structures.COPY_t):
        result = "COPY"
        if instruction.from_ is not None:
            result = result + " --from=%s" % instruction.from_
        for resource in instruction.resources:
            result = result + ' "%s"' % resource
        return result
    if isinstance(instruction, structures.ENTRYPOINT_t):
        result = "ENTRYPOINT"
        if instruction.shell_form is not None:
            for c in instruction.shell_form:
                result = result + " %s" % c
            return result
        else:
            commands = json.dumps(instruction.exec_form)
            return result + " " + commands
    if isinstance(instruction, structures.ENV_t):
        return "ENV %s %s" % (instruction.key, instruction.value)
    if isinstance(instruction, structures.ESCAPE_t):
        return "# escape=%s" % instruction.character
    if isinstance(instruction, structures.EXPOSE_t):
        result = "EXPOSE"
        for port_spec in instruction.port_specs:
            result = result + " %s" % port_spec
        return result
    if isinstance(instruction, structures.FROM_t):
        result = "FROM %s" % instruction.base_image
        if instruction.as_ is not None:
            result = result + " AS %s" % instruction.as_
        return result
    if isinstance(instruction, structures.HEALTHCHECK_t):
        result = "HEALTHCHECK"
        if instruction.interval is not None:
            result = result + " \\\n  --interval=%s" % instruction.interval
        if instruction.timeout is not None:
            result = result + " \\\n  --timeout=%s" % instruction.timeout
        if instruction.start_period is not None:
            result = result + " \\\n  --start-period=%s" % instruction.start_period
        if instruction.retries is not None:
            result = result + " \\\n  --retries=%s" % instruction.retries
        if instruction.cmd is not None:
            result = result + " \\\n  CMD"
            if isinstance(instruction.cmd, str):
                return result + " %s" % instruction.cmd
            else:
                for c in instruction.cmd:
                    result = result + " %s" % c
                return result
    if isinstance(instruction, structures.LABEL_t):
        return "LABEL %s=%s" % (instruction.key, instruction.value)
    if isinstance(instruction, structures.ONBUILD_t):
        return "ONBUILD %s" % render_instruction(instruction.instruction)
    if isinstance(instruction, structures.RUN_t):
        result = "RUN"
        if instruction.shell_form is not None:
            for c in instruction.shell_form:
                result = result + " %s" % c
            return result
        else:
            commands = json.dumps(instruction.exec_form)
            return result + " " + commands
    if isinstance(instruction, structures.SHELL_t):
        return "SHELL " +  json.dumps(instruction.shell_spec)
    if isinstance(instruction, structures.STOPSIGNAL_t):
        return "STOPSIGNAL %s" % instruction.signal
    if isinstance(instruction, structures.USER_t):
        result = "USER %s" % instruction.user
        if instruction.group is not None:
            result = result + ":%s" % instruction.group
        return result
    if isinstance(instruction, structures.VOLUME_t):
        return "VOLUME " + json.dumps(instruction.volume_specs)
    if isinstance(instruction, structures.WORKDIR_t):
        return "WORKDIR %s" % instruction.workdir
    raise DockerphileError(
        "Unrecognized or invalid instruction type %s" % instruction
    )
