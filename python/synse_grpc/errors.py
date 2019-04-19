
from grpc import RpcError, StatusCode


class PluginError(Exception):
    """Base class for all Plugin errors surfaced via the Synse gRPC API."""


class NotFound(PluginError):
    """A subclass of PluginError where a specified resource was not found."""


class BadArguments(PluginError):
    """A subclass of PluginError where bad arguments were provided for the request."""


def wrap_and_raise(exception):
    """Wrap the exception in a Synse gRPC client PluginError, if appropriate,
    and raise.

    If not appropriate, just raise the exception as-is.

    Args:
        exception (Exception): The exception to try and wrap before raising.
    """
    if isinstance(exception, RpcError):
        code = exception.code()
        if code == StatusCode.NOT_FOUND:
            raise NotFound from exception
        elif code == StatusCode.INVALID_ARGUMENT:
            raise BadArguments from exception
        elif code == StatusCode.UNKNOWN:
            raise PluginError from exception

    raise exception
