from dockerfile import parse_file

from dockerphile import structures
from dockerphile.errors import DockerphileError
from dockerphile.parse_tools import parse_escape_directive, to_instruction
from dockerphile.render_tools import render_instruction
from dockerphile.run_block import RunBlock


def new_dockerfile(source=None):
    """Create a blank Dockerfile object.

    The blank document can have Dockerfile command representation appended to
    it sequentially using the `dockerphile.Dockerfile` interface. Optionally,
    if a path to a local source Dockerfile is specified with the `source`
    option, then `dockerphile.Dockerfile` is initialized with the commands from
    that source file.

    Note that comment strings are ignored and are not converted into comment
    instructions in a `dockerphile.Dockerfile` initialized from a source file,
    except that if the first non-blank line of the file contains a use of the
    `escape` parser directive, this comment line is retained. Comments are not
    converted because the underlying `dockerfile` [1] library does not support
    parsing them.

    [1]: https://github.com/asottile/dockerfile

    Args:
        source: optional string naming a path to a source Dockerfile on disk
            used to initialize the `dockerphile.Dockerfile` commands.

    Returns:
        An empty `dockerphile.dockerfile_tools.Dockerfile` instance. Optionally
        returns an instance of `dockerphile.dockerfile_tools.Dockerfile` that
        has been initialized with commands from a Dockerfile source file.

    Raises:
        Nothing.

    """
    return Dockerfile(source=source)


class Dockerfile:
    """Programmatically create, modify and render Dockerfiles."""

    def __init__(self, source=None):
        """Create a new Dockerfile.

        Optionally parse a source Dockerfile and populate the new Dockerfile
        instance with the source Dockerfile commands.

        Args:
            source: optional string naming a path to a source Dockerfile on
                disk used to initialize the `dockerphile.Dockerfile` commands.

        Returns:
            Nothing. Instantiates `self` attributes for class instance created.

        Raises:
            Nothing.

        """
        self.sequence = []
        if source is not None:
            escape_directive = parse_escape_directive(source)
            if escape_directive is not None:
                self.sequence.append(escape_directive)
            for command in parse_file(source):
                instruction = to_instruction(command)
                if instruction is None:
                    continue
                elif isinstance(instruction, list):
                    self.sequence.extend(instruction)
                else:
                    self.sequence.append(instruction)

    def __repr__(self):
        """Commit contents of self.sequence to string."""
        return "\n".join(map(render_instruction, self.sequence)) + "\n"

    def add(self, *uris):
        """add_t"""
        self.sequence.append(structures.ADD(uris))

    def arg(self, key, value=None):
        """arg_t."""
        self.sequence.append(structures.ARG(key, default_value=value))

    def cmd(self, cmd, form='exec'):
        """cmd_t."""
        if form not in {'exec', 'default', 'shell'}:
            raise DockerphileError(
                'Invalid format specifier for CMD instruction %s' % form
            )
        self.sequence.append(
            structures.CMD(**{("%s_form" % form): cmd})
        )

    def comment(self, comment):
        """comment_t"""
        self.sequence.append(structures.COMMENT(comment))

    def copy(self, *paths, from_=None):
        """copy_t"""
        self.sequence.append(structures.COPY(paths, from_=from_))

    def entrypoint(self, entrypoint, form='exec'):
        """entrypoint_t"""
        if form not in {'exec', 'shell'}:
            raise DockerphileError(
                'Invalid format specifier for ENTRYPOINT instruction %s' % form
            )
        self.sequence.append(
            structures.ENTRYPOINT(**{("%s_form" % form): entrypoint})
        )

    def env(self, key, value):
        """env_t"""
        self.sequence.append(structures.ENV(key, value=value))

    def escape(self, character):
        """escape_t"""
        self.sequence.append(structures.ESCAPE(character))

    def expose(self, *port_specs):
        """expose_t"""
        self.sequence.append(structures.EXPOSE(port_specs))

    def from_(self, image, as_=None):
        """from_t"""
        self.sequence.append(structures.FROM(image, as_=as_))

    def healthcheck(self, interval=None, timeout=None,
                    start_period=None, retries=None, cmd=None):
        """healthcheck_t"""
        self.sequence.append(
            structures.HEALTHCHECK(
                interval=interval,
                timeout=timeout,
                start_period=start_period,
                retries=retries,
                cmd=cmd
            )
        )

    def label(self, key, value):
        """label_t"""
        self.sequence.append(structures.LABEL(key, value))

    def onbuild(self, instruction):
        """onbuild_t"""
        self.sequence.append(structures.ONBUILD(instruction))

    def run(self, command, form='shell'):
        """run_t"""
        if form not in {'exec', 'shell'}:
            raise DockerphileError(
                'Invalid format specifier for RUN instruction %s' % form
            )
        self.sequence.append(
            structures.RUN(**{("%s_form" % form): command})
        )

    def run_block(self, form='shell'):
        """Syntactiv sugar for RUN block."""
        if form not in {'exec', 'shell'}:
            raise DockerphileError(
                'Invalid format specifier for RUN instruction %s' % form
            )
        return RunBlock(self, form=form)

    def save(self, filename):
        """Commit contents of Dockerfile to a file on disk."""
        with open(filename, 'w') as output:
            output.write(str(self))

    def shell(self, shell_spec):
        """shell_t"""
        self.sequence.append(structures.SHELL(shell_spec))

    def stopsignal(self, signal):
        """stopsignal_t"""
        self.sequence.append(structures.STOPSIGNAL(signal))

    def user(self, user, group=None):
        """user_t"""
        self.sequence.append(structures.USER(user, group=group))

    def volume(self, *volume_specs):
        """volume_t"""
        self.sequence.append(structures.VOLUME(volume_specs))

    def workdir(self, workdir):
        """workdir_t"""
        self.sequence.append(structures.WORKDIR(workdir))
