#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Setup and packaging for the synse_grpc API client."""

from setuptools import setup, find_packages


setup(
    name='exampke',
    packages=find_packages(),
    include_package_data=True,
    python_requires='>=3.6',
    zip_safe=False,
)
