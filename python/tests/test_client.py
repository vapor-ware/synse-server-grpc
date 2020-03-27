
import os

import pytest

from synse_grpc import client


class TestPluginClientBase:
    """Unit tests for the PluginClientBase class."""

    def test_init_not_implemented(self):

        with pytest.raises(NotImplementedError):
            client.PluginClientBase('localhost', 'tcp')

    def test_init_ok(self, mocker):
        mock_make = mocker.patch('synse_grpc.client.PluginClientBase.make_grpc_client')

        c = client.PluginClientBase('localhost', 'TCP')

        assert c.address == 'localhost'
        assert c.protocol == 'tcp'
        assert c.timeout is None
        assert c.tls is None

        mock_make.assert_called_once()

    def test_init_bad_protocol(self):

        with pytest.raises(ValueError):
            client.PluginClientBase('localhost', 'unsupported-protocol')

    def test_get_address_tcp(self, mocker):
        mock_make = mocker.patch('synse_grpc.client.PluginClientBase.make_grpc_client')

        c = client.PluginClientBase('localhost:5001', 'TCP')
        assert c.get_address() == 'localhost:5001'

        mock_make.assert_called_once()

    def test_get_address_unix(self, mocker):
        mock_make = mocker.patch('synse_grpc.client.PluginClientBase.make_grpc_client')

        c = client.PluginClientBase('socket-name', 'UNIX')
        assert c.get_address() == 'unix:/tmp/synse/socket-name'

        mock_make.assert_called_once()

    def test_make_channel_insecure(self, mocker):
        mock_make = mocker.patch('synse_grpc.client.PluginClientBase.make_grpc_client')

        c = client.PluginClientBase('localhost:5678', 'tcp')
        chan = c.make_channel()
        assert chan is not None

        mock_make.assert_called_once()

    def test_make_channel_secure(self, mocker):
        mock_make = mocker.patch('synse_grpc.client.PluginClientBase.make_grpc_client')

        certs = os.path.join(os.path.dirname(__file__), 'data/certs/test.crt')
        c = client.PluginClientBase('localhost:5678', 'tcp', tls=certs)
        chan = c.make_channel()
        assert chan is not None

        mock_make.assert_called_once()
