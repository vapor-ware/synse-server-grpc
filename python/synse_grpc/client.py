"""A client wrapper around the auto-generated gRPC code."""

import os

import grpc as grpclib

from synse_grpc import api, errors, grpc, utils

DEFAULT_SOCK_PATH = '/tmp/synse'


class PluginClientBase:
    """Base class for all Synse gRPC clients for interfacing with plugins.

    These gRPC clients are convenience wrappers around the auto-generated
    gRPC python code to make it easier for the client consumer to use.

    Args:
        address (str): The address of the plugin to connect to.
        protocol (str): The network protocol to use. This must be one of:
            'tcp', 'unix'.
        timeout (int): The default timeout to use for the gRPC client.
        tls (str): The path to the TLS cert to use. If not using TLS,
            this can be left as None. (default: None)

    Raises:
        ValueError: An unsupported network protocol was specified.
    """

    # Define the supported transport protocols for the grpc client connection.
    _protocols = ('tcp', 'unix')

    # Define an empty message type that can be used for all routes that take
    # an empty request.
    empty = api.Empty()

    def __init__(self, address, protocol, timeout=None, tls=None):
        self.address = address
        self.protocol = protocol.lower()
        self.timeout = timeout
        self.tls = tls

        if self.protocol not in self._protocols:
            raise ValueError(
                'Invalid protocol specified for gRPC client: {} '
                '(must be one of: {})'.format(protocol, self._protocols)
            )

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
            # FIXME: is this the right way to go about this? forcing default path?
            return 'unix:{}'.format(os.path.join(DEFAULT_SOCK_PATH, self.address))

    def make_channel(self):
        """Make the channel for the gRPC client.

        Returns:
            grpclib.Channel: The channel over which the client will communicate with
            the plugin.
        """
        if self.tls:
            with open(self.tls, 'rb') as f:
                cert = f.read()
            credentials = grpclib.ssl_channel_credentials(root_certificates=cert)
            return grpclib.secure_channel(self.get_address(), credentials)
        else:
            return grpclib.insecure_channel(self.get_address())

    def make_grpc_client(self):
        """Initialize a new gRPC client to communicate with the plugin."""
        # Each subclassed client should implement this on its own so it is using the
        # correct version of the client.
        raise NotImplementedError


class PluginClientV3(PluginClientBase):
    """Synse v3 gRPC client for interfacing with plugins."""

    def make_grpc_client(self):
        """Initialize a new Synse v3 gRPC client to communicate with the plugin."""

        return grpc.V3PluginStub(self.make_channel())

    def devices(self, device_id=None, tags=None):
        """Get devices that the plugin manages.

        Args:
            device_id (str): The ID of the device to get information on. If this
                argument is specified, the ``tags`` argument is ignored.
            tags (list[str]): The tags matching the devices to get information
                on. If this is empty and ``id`` is not specified, all devices
                are returned.

        Yields:
            api.V3Device: The plugin-managed device(s) matching the provided
                filter parameters. If no parameters are given, all devices are
                returned.
        """

        request = api.V3DeviceSelector()
        if device_id:
            request.id = device_id
        elif tags:
            request.tags.extend([utils.tag_to_message(tag) for tag in tags])

        try:
            for device in self.client.Devices(request, timeout=self.timeout):
                yield device
        except Exception as e:
            errors.wrap_and_raise(e)

    def health(self):
        """Get the health status of the plugin.

        Returns:
            api.V3Health: The health status of the plugin.
        """

        try:
            return self.client.Health(self.empty, timeout=self.timeout)
        except Exception as e:
            errors.wrap_and_raise(e)

    def metadata(self):
        """Get the static plugin meta-information.

        Returns:
            api.V3Metadata: The static plugin meta-information.
        """

        try:
            return self.client.Metadata(self.empty, timeout=self.timeout)
        except Exception as e:
            errors.wrap_and_raise(e)

    def read(self, device_id=None, tags=None):
        """Get readings from specified plugin devices.

        Args:
            device_id (str): The ID of the device to get information on. If this
                argument is specified, the ``tags`` argument is ignored.
            tags (list[str]): The tags matching the devices to get information
                on. If this is empty and ``id`` is not specified, all devices
                are returned.

        Yields:
            api.V3Reading: The reading(s) from the specified device(s).
        """

        request = api.V3ReadRequest(
            selector=api.V3DeviceSelector()
        )

        if device_id:
            request.selector.id = device_id
        elif tags:
            request.selector.tags.extend([utils.tag_to_message(tag) for tag in tags])

        try:
            for reading in self.client.Read(request, timeout=self.timeout):
                yield reading
        except Exception as e:
            errors.wrap_and_raise(e)

    def read_cache(self, start=None, end=None):
        """Get the cached readings from the plugin. If the plugin is not configured
        to cache readings, a snapshot of the current reading state for all devices
        is returned.

        Args:
            start (str): An RFC3339 formatted timestamp which defines a starting
                bound on the cache data to return. If no timestamp is specified,
                there will not be a starting bound. (default: None)
            end (str): An RFC3339 formatted timestamp which defines an ending
                bound on the cache data to return. If no timestamp is specified,
                there will not be an ending bound. (default: None)

        Yields:
            api.V3Reading: The cached reading values for plugin devices.
        """

        request = api.V3Bounds(
            start=start or '',
            end=end or '',
        )

        try:
            for reading in self.client.ReadCache(request, timeout=self.timeout):
                yield reading
        except Exception as e:
            errors.wrap_and_raise(e)

    def test(self):
        """Check whether the plugin is reachable and ready.

        Returns:
            api.V3TestStatus: The test status of the plugin.
        """

        try:
            return self.client.Test(self.empty, timeout=self.timeout)
        except Exception as e:
            errors.wrap_and_raise(e)

    def transaction(self, transaction_id):
        """Get the status of a write transaction for an asynchronous write action.

        Args:
            transaction_id (str): The ID of the transaction to check.

        Returns:
            api.V3TransactionStatus: The transaction status for the
            asynchronous write.
        """

        request = api.V3TransactionSelector(
            id=transaction_id,
        )

        try:
            return self.client.Transaction(request, timeout=self.timeout)
        except Exception as e:
            errors.wrap_and_raise(e)

    def transactions(self):
        """Get all actively tracked transactions from the plugin.

        Yields:
            api.V3TransactionStatus: The transactions currently tracked
            by the plugin.
        """

        try:
            for status in self.client.Transactions(request=self.empty, timeout=self.timeout):
                yield status
        except Exception as e:
            errors.wrap_and_raise(e)

    def version(self):
        """Get the version information for the plugin.

        Returns:
            api.V3Version: The version information for the plugin.
        """

        try:
            return self.client.Version(self.empty, timeout=self.timeout)
        except Exception as e:
            errors.wrap_and_raise(e)

    def write_async(self, device_id, data):
        """Write data to the specified plugin device. A transaction ID is returned
        so the write status can be checked asynchronously.

        Args:
            device_id (str): The device to write to.
            data (list[dict] | dict): The data to write to the device.

        Yields:
            api.V3WriteTransaction: The transaction(s) generated for the
            asynchronous write request.
        """

        request = api.V3WritePayload(
            selector=api.V3DeviceSelector(
                id=device_id,
            ),
            data=utils.write_data_to_messages(data),
        )

        try:
            for txn in self.client.WriteAsync(request, timeout=self.timeout):
                yield txn
        except Exception as e:
            errors.wrap_and_raise(e)

    def write_sync(self, device_id, data):
        """Write data to the specified plugin device. This request blocks until
        the write resolves so no asynchronous checking is required.

        Args:
            device_id (str): The device to write to.
            data (list[dict] | dict): The data to write to the device.

        Returns:
            list[api.V3TransactionStatus]: The status of the transaction(s)
            associated with the write.
        """

        request = api.V3WritePayload(
            selector=api.V3DeviceSelector(
                id=device_id,
            ),
            data=utils.write_data_to_messages(data),
        )

        try:
            return [x for x in self.client.WriteSync(request, timeout=self.timeout)]
        except Exception as e:
            errors.wrap_and_raise(e)
