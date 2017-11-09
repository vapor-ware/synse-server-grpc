""" Synse Server gRPC internal plugin API.
"""

from . import synse_pb2 as api
from . import synse_pb2_grpc as grpc


__title__ = 'synse_plugin'
__version__ = '0.0.1'

__description__ = 'Internal gRPC API for communication between plugins and Synse Server.'
__author__ = 'Vapor IO'
__author_email__ = 'vapor@vapor.io'
__url__ = 'https://github.com/vapor-ware/synse-server-grpc'
