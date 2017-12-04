from collections import namedtuple

from dockerphile.errors import DockerphileError


HEALTHCHECK_t = namedtuple(
    'HEALTHCHECK',
    ['interval', 'timeout', 'start_period', 'retries', 'cmd']
)


def HEALTHCHECK(interval=None, timeout=None, start_period=None,
                retries=None, cmd=None):
    """Create a Dockerfile HEALTHCHECK instruction.

    Args:
        interval: Optional string containing the duration to wait both prior
            to the first heathcheck invocation after container start and the
            interval to wait after a successful healthcheck for applying the
            next healthcheck.
        timeout: Optional string containing the duration of time afterwhich
            a running healthcheck will expire and be considered as failed.
        start_period: Optional string containing a duration of time to consider
            as a start-up phase for a container, a phase during which failed
            healthchecks don't count towards the maximum retries.
        retries: Optional string containing the number of retries to attempt
            before consecutive healthcheck failures result in an 'unhealthy'
            container state.
        cmd: Optional. Either a single string containing one command or else a
            list or tuple containing an executable in the first element and
            optional parameters in the remaining elements.

    Returns:
        An instance of the HEALTHCHECK namedtuple.

    Raises:
        DockerphileError: raised when arguments are misspecified.
    """
    parameters = {'interval': interval, 'timeout': timeout,
                  'start_period': start_period, 'retries': retries}
    for param, value in parameters.items():
        if not isinstance(value, (str, type(None))):
            raise DockerphileError(
                'HEALTHCHECK parameter %s requires string, not %s' % (
                    param,
                    type(value)
                )
            )
    if not isinstance(cmd, (str, list, tuple, type(None))):
        raise DockerphileError(
            ('HEALTHCHECK "CMD" option must be a string or a list/tuple of '
             'strings, not %s') % type(cmd)
        )
    if isinstance(cmd, (list, tuple)) and not cmd:
        raise DockerphileError(
            'HEALTHCHECK "CMD" exec format must have at least 1 executable.'
        )
    return HEALTHCHECK_t(
        interval=interval,
        timeout=timeout,
        start_period=start_period,
        retries=retries,
        cmd=cmd
    )
