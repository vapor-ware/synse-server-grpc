""" Convenience method to get out the version, as defined in the python package.
"""

from __future__ import print_function

import os
import re


def find_version():
    """Find the version of synse_plugin.
    """
    dir_path = os.path.dirname(os.path.realpath(__file__))
    with open(os.path.join(dir_path, 'synse_plugin', '__init__.py')) as f:
        contents = f.read()

    version = re.search(r'^__version__ = [\'"]([^\'"]*)[\'"]', contents, re.M)
    if version:
        return version.group(1)
    raise RuntimeError('Unable to find version in __init__ file.')

if __name__ == '__main__':
    print(find_version())
