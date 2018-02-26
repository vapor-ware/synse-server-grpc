""" Synse Internal gRPC API python package setup.
"""

from setuptools import setup, find_packages
import synse_plugin as pkg

setup(
    name='synse_plugin',
    version=pkg.__version__,
    description=pkg.__description__,
    url=pkg.__url__,
    author=pkg.__author__,
    author_email=pkg.__author_email__,
    license='GNU General Public License v2.0',
    packages=find_packages()
)
