class RunBlock:

    def __init__(self, dockerfile, form='shell'):
        """Create a RunBlock context.

        The context manager is for coalescing multiple RUN instructions into a
        single RUN instruction with multiple commands chained together with
        '&& \' and rendered on sequential newlines.

        Args:
            dockerfile: A dockerphile.Dockerfile instance into which the
                coalesced RUN instruction will be added.
            form: Optional string naming which type of supported RUN format
                will be used (default 'shell' format).

        Returns:
            Nothing. A side-effect of the context manager will write the
            coalesced RUN instruction into the provided `dockerfile`.

        Raises:
            DockerphileError: raised if RUN instruction strings or format are
                not provided correctly as they are passed to the
                `dockerfile.run` command.
        """
        self.dockerfile = dockerfile
        self.form = form
        self.sequence = []

    def __enter__(self):
        """Set up the context manager with a sequence placeholder."""
        return self

    def __exit__(self, *args):
        """Write the coalesced RUN instruction to the Dockerfile on exit."""
        self.dockerfile.run(
            ["\\\n  " + " && \\\n  ".join(self.sequence)], 
            form=self.form
        )

    def run(self, command):
        """Append an isolated RUN instruction to a context manager.

        Args:
            command: A command string suitable for passing to `dockerfile.run`,
                which will have ' && \' appended to the end to use for chaining
                with additional RUN instructions before writing into a single
                RUN instruction in the provided `dockerfile`.

        Returns:
            Nothing. Appends RUN instructions to an internal list.

        Raises:
            Nothing.
        """
        self.sequence.append(command)
