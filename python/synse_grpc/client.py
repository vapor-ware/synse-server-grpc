"""A client wrapper around the auto-generated GRPC code."""

import os

import grpc

from . import synse_pb2, synse_pb2_grpc, utils

DEFAULT_SOCK_PATH = '/tmp/synse'


class PluginClientBase:
    """Base class for all Synse GRPC clients for interfacing with plugins.

    These GRPC clients are convenience wrappers around the auto-generated
    GRPC python code to make it easier for the client consumer to use.

    Args:
        address (str): The address of the plugin to connect to.
        protocol (str): The network protocol to use. This must be one of:
            'tcp', 'unix'.
        timeout (int): The default timeout to use for the GRPC client.
        tls (str): The path to the TLS cert to use. If not using TLS,
            this can be left as None. (default: None)

    Raises:
        ValueError: An unsupported network protocol was specified.
    """

    # Define the supported transport protocols for the grpc client connection.
    __protocols__ = ('tcp', 'unix')

    # Define an empty message type that can be used for all routes that take
    # an empty request.
    empty = synse_pb2.Empty()

    def __init__(self, address, protocol, timeout=None, tls=None):
        self.address = address
        self.protocol = protocol.lower()
        self.timeout = timeout
        self.tls = tls

        if self.protocol not in self.__protocols__:
            raise ValueError(
                'Invalid protocol specified for GRPC client: {} '
                '(must be one of: {})'.format(protocol, self.__protocols__)
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

    def make_grpc_client(self):
        """Initialize a new Synse v3 GRPC client to communicate with the plugin."""
        return synse_pb2_grpc.V3PluginStub(self.make_channel())

    def devices(self, device_id=None, tags=None):
        """Get devices that the plugin manages.

        Args:
            device_id (str): The ID of the device to get information on. If this
                argument is specified, the ``tags`` argument is ignored.
            tags (list[str]): The tags matching the devices to get information
                on. If this is empty and ``id`` is not specified, all devices
                are returned.

        Yields:
            synse_pb2.V3Device: The plugin-managed device(s) matching the provided
                filter parameters. If no parameters are given, all devices are
                returned.
        """
        request = synse_pb2.V3DeviceSelector()
        if device_id:
            request.id = device_id
        elif tags:
            request.tags = [utils.str_to_tag(tag) for tag in tags]

        # TODO (etd): try and figure out the return type of client.Devices..
        #  is it a list? generator? depending on what it is, we could yield
        #  in a more sane way.
        for device in self.client.Devices(request, timeout=self.timeout):
            yield device

    def health(self):
        """Get the health status of the plugin.

        Returns:
            synse_pb2.V3Health: The health status of the plugin.
        """

        return self.client.Health(self.empty, timeout=self.timeout)

    def metadata(self):
        """Get the static plugin meta-information.

        Returns:
            synse_pb2.V3Metadata: The static plugin meta-information.
        """

        return self.client.Metadata(self.empty, timeout=self.timeout)

    def read(self, device_id=None, tags=None, system_of_measure=None):
        """Get readings from specified plugin devices.

        Args:
            device_id (str): The ID of the device to get information on. If this
                argument is specified, the ``tags`` argument is ignored.
            tags (list[str]): The tags matching the devices to get information
                on. If this is empty and ``id`` is not specified, all devices
                are returned.
            system_of_measure (str): The system of measure to convert the read
                responses to. (default: "metric")

        Yields:
            synse_pb2.V3Reading: The reading(s) from the specified device(s).
        """
        request = synse_pb2.V3ReadRequest(
            systemOfMeasure=system_of_measure or 'metric',
        )
        if device_id:
            request.selector = synse_pb2.V3DeviceSelector(
                id=device_id
            )
        elif tags:
            request.selector = synse_pb2.V3DeviceSelector(
                tags=[utils.str_to_tag(tag) for tag in tags]
            )

        for reading in self.client.Read(request, timeout=self.timeout):
            yield reading

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
            synse_pb2.V3Reading: The cached reading values for plugin devices.
        """

        request = synse_pb2.V3Bounds(
            start=start or '',
            end=end or '',
        )

        for reading in self.client.ReadCache(request, timeout=self.timeout):
            yield reading

    def test(self):
        """Check whether the plugin is reachable and ready.

        Returns:
            synse_pb2.V3TestStatus: The test status of the plugin.
        """

        return self.client.Test(self.empty, timeout=self.timeout)

    def transaction(self, transaction_id):
        """Get the status of a write transaction for an asynchronous write action.

        Args:
            transaction_id (str): The ID of the transaction to check.

        TODO (etd): does this need to return a stream? won't this just be returning
          a single transaction status per ID...?

        Yields:
            synse_pb2.V3TransactionStatus: The transaction status for the
        """

        request = synse_pb2.V3TransactionSelector(
            id=transaction_id,
        )

        for status in self.client.Transaction(request, timeout=self.timeout):
            yield status

    def version(self):
        """Get the version information for the plugin.

        Returns:
            synse_pb2.V3Version: The version information for the plugin.
        """

        return self.client.Version(self.empty, timeout=self.timeout)

    def write_async(self, device_id, data):
        """Write data to the specified plugin device. A transaction ID is returned
        so the write status can be checked asynchronously.

        Args:
            device_id (str): The device to write to.
            data (): The data to write to the device.
        """

        # TODO (etd): write util to convert list/dict of data to the appropriate
        #  data type for the write payload.
        request = synse_pb2.V3WritePayload(
            selector=synse_pb2.V3DeviceSelector(
                id=device_id,
            ),
        )
        return self.client.WriteAsync(request, timeout=self.timeout)

    def write_sync(self, device_id, data):
        """Write data to the specified plugin device. This request blocks until
        the write resolves so no asynchronous checking is required.

        Args:
            device_id (str): The device to write to.
            data (): The data to write to the device.
        """

        # TODO (etd): write util to convert list/dict of data to the appropriate
        #  data type for the write payload.
        request = synse_pb2.V3WritePayload(
            selector=synse_pb2.V3DeviceSelector(
                id=device_id,
            ),
        )
        # TODO: figure out how to do this so it blocks until resolved.
        return self.client.WriteSync(request, timeout=self.timeout)
