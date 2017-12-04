import re

from dockerphile import structures
from dockerphile.errors import DockerphileError


arg_default_value = re.compile(r"(.*)=(.*)$")
copy_from = re.compile(r"COPY\s+--from=(\S*)\s+.*$")
escape_directive = re.compile(r"\s*#\s+[Ee][Ss][Cc][Aa][Pp][Ee]=(\S)\s*$")
from_as = re.compile(r"FROM\s+(\S+)\s+AS\s+(\S+)\s*$")
healthcheck_arg_str = "HEALTHCHECK\s+.*--%s=(\S+)\s+.*$"
healthcheck_interval = re.compile(healthcheck_arg_str % "interval")
healthcheck_timeout = re.compile(healthcheck_arg_str % "timeout")
healthcheck_start_period = re.compile(healthcheck_arg_str % "start-period")
healthcheck_retries = re.compile(healthcheck_arg_str % "retries")
user_group = re.compile(r"USER\s+(\S+):(\S+)\s*$")


def parse_escape_directive(source):
    """Parse escape directive from a source Dockerfile's first non-empty line.

    Args:
        source: A source Dockerfile whose first non-empty line will be checked.

    Returns:
        A `dockerphile.structures.ESCAPE_t` type storing the escape directive.
        If an escape directive cannot be parsed from the first non-empty line
        of the source file, then `None` is returned.

    Raises:
        Nothing.
    """
    blank = True
    with open(source, 'r') as _file:
        for line in _file:
            blank = not line.strip()
            if not blank:
                break
    if not blank:
        parsed_escape = re.match(escape_directive, line)
        if parsed_escape is not None:
            return structures.ESCAPE(parsed_escape.groups()[0])
    return None


def to_instruction(parsed_instruction):
    """Map a parsed `dockerfile.Command` to a `dockerphile.structures` type.

    `dockerfile.Command` contains the original parsed string (with line
    continuations and all comments removed) and also contains a `value`
    attribute storing the part of the Dockerfile instruction non-inclusive
    of Dockerfile keywords.

    Known limitations include: (1) no parsing of comment lines; (2) no parsing
    of the `escape` parser directive; and (2) no direct parsing of the optional
    arguments for the HEALTHCHECK or COPY commands.

    Args:
        parsed_instruction: An instance of `dockerfile.Command`.

    Returns:
        Either an instance of a `dockerphile.structures` namedtuple representing
        the parsed command using `dockerphile` types, or a list of such types.
        Return value is None for any underlying commands that are not supported
        by `dockerphile` even if parsed correctly, such as `MAINTAINER` (since
        `dockerphile` requires following Docker best practices to use `LABEL`
        for a maintainer label.

    Raises:
        DockerphileError: raised if incorrect instruction type is provided or
            if the parsed `dockerfile.Command` object contains invalid
            Dockerfile syntax.
        dockerfile.GoParseError: raised if underlying `dockerfile` library
            Go parser encounters an unhandled parser error.
    """
    cmd, original = parsed_instruction.cmd, parsed_instruction.original
    uses_json, value = parsed_instruction.json, parsed_instruction.value
    if cmd == 'add':
        return structures.ADD(value)
    if cmd == 'arg':
        arg_string = value[0]
        parsed_arg = re.match(arg_default_value, arg_string)
        if parsed_arg is not None:
            key, default_value = parsed_arg.groups()
            return structures.ARG(key, default_value=default_value)
        else:
            return structures.ARG(arg_string)
    if cmd == 'cmd':
        return structures.CMD(**{
            ('exec_form' if uses_json else 'shell_form'): value
        })
    if cmd == 'copy':
        parsed_from = re.match(copy_from, original)
        from_ = parsed_from.groups()[0] if parsed_from is not None else None
        return structures.COPY(value, from_=from_)
    if cmd == 'entrypoint':
        return structures.ENTRYPOINT(**{
            ('exec_form' if uses_json else 'shell_form'): value
        })
    if cmd == 'env':
        if not value:
            raise DockerphileError("ENV command has no key or value.")
        if len(value) == 2:
            return structures.ENV(value[0], value[1])
        try:
            result = [structures.ENV(value[k], value[k+1])
                      for k in range(len(value))[::2]]
        except IndexError:
            raise DockerphileError(
                "Unpaired index when parsing %s to list of ENV types." % value
            )
        return result
    if cmd == 'expose':
        return structures.EXPOSE(value)
    if cmd == 'from':
        parsed_from = re.match(from_as, original)
        if parsed_from is not None:
            image, as_ = parsed_from.groups()
            return structures.FROM(image, as_=as_)
        if not value:
            raise DockerphileError(
                "FROM instruction requires non-empty base image."
            )
        return structures.FROM(value[0])
    if cmd == 'healthcheck':
        if value and value[0] != 'CMD':
            raise DockerphileError(
                'Invalid CMD specifier for HEALTHCHECK: %s' % value[0]
            )
        options = {
            'interval': re.match(healthcheck_interval, original),
            'timeout': re.match(healthcheck_timeout, original),
            'start_period': re.match(healthcheck_start_period, original),
            'retries': re.match(healthcheck_retries, original)
        }
        kwargs = {
            arg_name: (None if arg_match is None else arg_match.groups()[0])
            for arg_name, arg_match in options.items()
        }
        if len(value) == 2:
            kwargs['cmd'] = value[1]
        elif len(value) > 2:
            kwargs['cmd'] = value[1:]
        return structures.HEALTHCHECK(**kwargs)
    if cmd == 'label':
        if not value:
            raise DockerphileError("LABEL command has no key or value.")
        if len(value) == 2:
            return structures.LABEL(value[0], value[1])
        try:
            result = [structures.LABEL(value[k], value[k+1])
                      for k in range(len(value))[::2]]
        except IndexError:
            msg = "Unpaired index when parsing %s to list of LABEL types."
            raise DockerphileError(msg % value)
        return result
    if cmd == 'maintainer':
        return None
    if cmd == 'onbuild':
        if parsed_instruction.sub_cmd == 'onbuild':
            raise DockerphileError(
                "ONBUILD is not allowed as sub-command of ONBUILD."
            )
        sub_cmd_str = original.replace('ONBUILD', '')
        parsed_sub_cmd = dockerfile.parse_string(sub_cmd_str)[0]
        return structures.ONBUILD(to_instruction(parsed_sub_cmd))
    if cmd == 'run':
        return structures.RUN(**{
            ('exec_form' if uses_json else 'shell_form'): value
        })
    if cmd == "shell":
        if not uses_json:
            raise DockerphileError(
                "SHELL instruction requires used of JSON array option format."
            )
        if not value:
            raise DockerphileError(
                "SHELL instruction requires non-empty JSON array option format."
            )
        return structures.SHELL(value)
    if cmd == 'stopsignal':
        if not value:
            raise DockerphileError(
                "STOPSIGNAL instruction requires non-empty value."
            )
        return structures.STOPSIGNAL(value[0])
    if cmd == 'user':
        if not value:
            raise DockerphileError(
                "USER instruction requires non-empty value."
            )
        parsed_user_group = re.match(user_group, original)
        if parsed_user_group is not None:
            user, group = parsed_user_group.groups()
        else:
            user, group = value[0], None
        return structures.USER(user, group=group)
    if cmd == 'volume':
        return structures.VOLUME(value)
    if cmd == 'workdir':
        if not value:
            raise DockerphileError(
                "WORKDIR instruction requires non-empty value."
            )
        return structures.WORKDIR(value[0])
    raise DockerphileError(
        "Unrecognized dockerfile.Command parsed command %s" % cmd
    )
