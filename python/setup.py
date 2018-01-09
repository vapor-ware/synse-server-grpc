""" Synse Internal gRPC API python package setup.
"""

from setuptools import setup, find_packages

version = '0.0.1'
description = 'Internal gRPC API for communication between plugins and Synse Server.'
author = 'Vapor IO'
author_email = 'vapor@vapor.io'
url = 'https://github.com/vapor-ware/synse-server-grpc'

setup(
    name='synse_plugin',
    version=version,
    description=description,
    url=url,
    author=author,
    author_email=author_email,
    license='Vapor IO Proprietary',  # fixme - will need to change eventually
    packages=find_packages()
)
