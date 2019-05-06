
import pytest
from grpc import RpcError, StatusCode

from synse_grpc import errors


class MockError(RpcError):
    """Mock RpcError as it would be returned from the gRPC server.

    Unfortunately, the Python gRPC code is not straightforward and
    the process by which exceptions are created and raised is not
    straightforward. This mock error will expose the fields that we
    expect to have when we get an error back from the server.
    """

    def __init__(self, status_code):
        self._code = status_code

    def code(self):
        return self._code


@pytest.mark.parametrize('exception,expected', [
    (ValueError(), ValueError),
    (MockError(StatusCode.NOT_FOUND), errors.NotFound),
    (MockError(StatusCode.INVALID_ARGUMENT), errors.BadArguments),
    (MockError(StatusCode.UNKNOWN), errors.PluginError),
    (MockError(StatusCode.UNAUTHENTICATED), MockError),
])
def test_wrap_and_raise(exception, expected):
    """Wrap and re-raise an exception."""

    with pytest.raises(expected):
        errors.wrap_and_raise(exception)
