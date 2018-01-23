#!/usr/bin/env python3
# coding=utf-8
# by nearg1e (nearg1e.com@gmail[dot]com)
"""about version.
thx. aploium
"""

from distutils.version import LooseVersion
from utils.common import remove_blank

from utils.common import IS_PY3
from utils.log import LOGGER as logger


def str2version(version):
    """to version"""
    if IS_PY3:
        str_types = str
    else:
        str_types = (unicode, str, basestring)
    
    if isinstance(version, str_types):
        return LooseVersion(remove_blank(version))

    return version


def make_operator(real_hash, fingerprint_hash):
    """return a set of compare operator. like ('>=')."""
    operators = set()
    if real_hash:
        if real_hash == fingerprint_hash:
            operators.add('>=')
        else:
            if fingerprint_hash:
                operators.add('!=')
            else:
                operators.add('>')
    else:
        if fingerprint_hash:
            operators.add('<')
        else:
            operators.add('<=')
    return operators


def make_version(static_map, fingerprint_map):
    """return version expression."""
    version_compare_lst = []
    key_lst = fingerprint_map.keys()
    version_lst = sorted([str2version(ver_) for ver_ in key_lst], reverse=True)
    last = version_lst[0]
    # compare to each version fingerprint.
    # make compare expressions. like [(">=", 'v2.3.3.3')]
    for version in version_lst:
        fingerprint = fingerprint_map.get(version.vstring)
        for path, filehash in fingerprint:
            real_hash = static_map.get(path)
            operators = make_operator(real_hash, filehash)
    return version_compare_lst
