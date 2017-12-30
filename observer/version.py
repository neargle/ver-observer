#!/usr/bin/env python3
# coding=utf-8
# by nearg1e (nearg1e.com@gmail[dot]com)
"""about version.
thx. aploium
"""

from distutils.version import LooseVersion
from utils.common import remove_blank

from utils.common import IS_PY3



def str2version(version):
    """to version"""
    if IS_PY3:
        str_types = str
    else:
        str_types = (unicode, str, basestring)
    
    if isinstance(version, str_types):
        return LooseVersion(remove_blank(version))

    return version
