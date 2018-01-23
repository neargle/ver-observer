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
    operator = ""
    if real_hash:
        if real_hash == fingerprint_hash:
            operator = '>='
        else:
            if fingerprint_hash:
                operator = '!='
            else:
                operator = '>'
    else:
        if fingerprint_hash:
            operator = '<'
        else:
            operator = '<='
    logger.noise(
        'real hash: %s, fingerprint: %s. operator is %s',
        real_hash, fingerprint_hash, operator
    )
    return operator


def make_version(static_map, fingerprint_map):
    """return version expression."""
    version_compare_lst = []
    key_lst = fingerprint_map.keys()
    version_lst = sorted([str2version(ver_) for ver_ in key_lst], reverse=True)
    last = version_lst[0]
    # compare to each version fingerprint.
    # make compare expressions. like [(">=", 'v2.3.3.3')]
    for version in version_lst:
        operators = set()
        fingerprint = fingerprint_map.get(version.vstring)
        for path, filehash in fingerprint.items():
            real_hash = static_map.get(path)
            operators.add(make_operator(real_hash, filehash))
        logger.debug("version %s: operator %s", version.vstring, operators)
    return version_compare_lst
