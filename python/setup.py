"""Setup and packaging for the Synse gRPC API client."""

import os

from codecs import open  # for consistent encoding
from setuptools import setup, find_packages


here = os.path.abspath(os.path.dirname(__file__))

# Load the package's __init__.py file as a dictionary
pkg = {}
with open(os.path.join(here, 'synse_grpc', '__init__.py'), 'r', 'utf-8') as f:
    exec(f.read(), pkg)

# Load the README
readme = ''
if os.path.exists('README.md'):
    with open('README.md', 'r', 'utf-8') as f:
        readme = f.read()

setup(
    name=pkg['__title__'],
    version=pkg['__version__'],
    description=pkg['__description__'],
    long_description=readme,
    url=pkg['__url__'],
    author=pkg['__author__'],
    author_email=pkg['__author_email__'],
    license=pkg['__license__'],
    packages=find_packages(),
    include_package_data=True,
    python_requires='>=3.6',
    zip_safe=False,
    install_requires=[
        'grpcio>=1.8.6',
        'protobuf',
    ],
    classifiers=[
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ]
)
