#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Synse Internal gRPC API python package setup."""

from setuptools import find_packages, setup

# Package metadata
name = 'synse_grpc'
description = 'Internal gRPC API for communication between plugins and Synse Server.'
url = 'https://github.com/vapor-ware/synse-server-grpc'
email = 'vapor@vapor.io'
author = 'Vapor IO'
version = '1.1.0'

# packages required for this module to run
required = [
    'grpcio>=1.8.6'
]

setup(
    name=name,
    version=version,
    description=description,
    author=author,
    author_email=email,
    url=url,
    packages=find_packages(),
    install_requires=required,
    include_package_data=True,
    license='GNU General Public License v3.0',
    classifiers=[
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
    ],
)
