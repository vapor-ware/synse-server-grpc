"""Convenience method to get out the version, as defined in setup.py.
"""

from __future__ import print_function

import os
import re


def find_version():
    """Find the version of synse_plugin.
    """
    dir_path = os.path.dirname(os.path.realpath(__file__))
    with open(os.path.join(dir_path, 'setup.py')) as f:
        contents = f.read()

    version = re.search(r'^version = [\'"]([^\'"]*)[\'"]', contents, re.M)
    if version:
        return version.group(1)
    raise RuntimeError('Unable to find version in setup.py file.')


if __name__ == '__main__':
    print(find_version())
