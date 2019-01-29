"""A client wrapper around the auto-generated GRPC code."""

import os
import grpc

from . import synse_pb2, synse_pb2_grpc

# FIXME: map out a complete fs layout for synse to make sure it is all cohesive
DEFAULT_SOCK_PATH = '/etc/synse/plugin/socket'


class PluginClientBase:
    """Base class for all Synse GRPC clients for interfacing with plugins.

    These GRPC clients are convenience wrappers around the auto-generated
    GRPC python code to make it easier for the client consumer to use.

    Args:
        address (str): The address of the plugin to connect to.
        protocol (str): The network protocol to use. This must be one of:
            'tcp', 'unix'.
        tls (str): The path to the TLS cert to use. If not using TLS,
            this can be left as None. (default: None)

    Raises:
        ValueError: An unsupported network protocol was specified.
    """

    __protocols__ = ('tcp', 'unix')

    def __init__(self, address, protocol, timeout=None, tls=None):
        if protocol.lower() not in self.__protocols__:
            raise ValueError(
                'Invalid protocol specified for GRPC client: {} '
                '(must be one of: {})'.format(protocol, self.__protocols__)
            )

        self.address = address
        self.protocol = protocol.lower()
        self.timeout = timeout
        self.tls = tls

        self.client = self.make_grpc_client()

    def get_address(self):
        """Get the correctly formatted plugin address, based on the network
        protocol set for the client.

        Returns:
            str: The plugin address for the client to connect to.
        """
        if self.protocol == 'tcp':
            return self.address
        elif self.protocol == 'unix':
            return 'unix:{}'.format(os.path.join(DEFAULT_SOCK_PATH, self.address))

    def make_channel(self):
        """Make the channel for the GRPC client.

        Returns:
            grpc.Channel: The channel over which the client will communicate with
            the plugin.
        """
        if self.tls:
            with open(self.tls, 'rb') as f:
                cert = f.read()
            credentials = grpc.ssl_channel_credentials(root_certificates=cert)
            return grpc.secure_channel(self.get_address(), credentials)
        else:
            return grpc.insecure_channel(self.get_address())

    def make_grpc_client(self):
        """Initialize a new GRPC client to communicate with the plugin."""
        # Each subclassed client should implement this on its own so it is using the
        # correct version of the client.
        raise NotImplementedError


class PluginClientV3(PluginClientBase):
    """Synse v3 GRPC client for interfacing with plugins."""

    # FIXME: should all streamed responses be returned as a generator? e.g. yielded

    def make_grpc_client(self):
        """Initialize a new Synse v3 GRPC client to communicate with the plugin."""
        return synse_pb2_grpc.V3PluginStub(self.make_channel())

    def devices(self):
        """Get all devices that the plugin manages."""

        request = synse_pb2.V3DeviceSelector()
        return [r for r in self.client.Devices(request, timeout=self.timeout)]

    def health(self):
        """Get the health status of the plugin."""

        request = synse_pb2.Empty()
        return self.client.Health(request, timeout=self.timeout)

    def metadata(self):
        """Get the static plugin meta-information."""

        request = synse_pb2.Empty()
        return self.client.Metadata(request, timeout=self.timeout)

    def read(self):
        """Get readings from specified plugin devices."""

        request = synse_pb2.V3DeviceSelector()
        return [r for r in self.client.Read(request, timeout=self.timeout)]

    def read_cache(self):
        """Get the cached readings from the plugin. If the plugin is not configured
        to cache readings, a snapshot of the current reading state for all devices
        is returned.
        """

        request = synse_pb2.V3Bounds()
        for reading in self.client.ReadCache(request, timeout=self.timeout):
            yield reading

    def test(self):
        """Check whether the plugin is reachable and ready."""

        request = synse_pb2.Empty()
        return self.client.Test(request, timeout=self.timeout)

    def transaction(self):
        """Get the status of a write transaction for an asynchronous write action."""

        request = synse_pb2.V3TransactionSelector()
        return [r for r in self.client.Transaction(request, timeout=self.timeout)]

    def version(self):
        """Get the version information for the plugin."""

        request = synse_pb2.Empty()
        return self.client.Version(request, timeout=self.timeout)

    def write_async(self):
        """Write data to the specified plugin device. A transaction ID is returned
        so the write status can be checked asynchronously.
        """

        request = synse_pb2.V3WritePayload()
        return self.client.WriteAsync(request, timeout=self.timeout)

    def write_sync(self):
        """Write data to the specified plugin device. This request blocks until
        the write resolves so no asynchronous checking is required.
        """

        request = synse_pb2.V3WritePayload()
        # TODO: figure out how to do this so it blocks until resolved.
        return self.client.WriteSync(request, timeout=self.timeout)
