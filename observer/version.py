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
        return operator


def make_version(static_map, fingerprint_map):
    """return version expression."""
    version_compare_lst = set()
    key_lst = fingerprint_map.keys()
    version_lst = sorted([str2version(ver_) for ver_ in key_lst], reverse=True)
    last = version_lst[0]
    # compare to each version fingerprint.
    # make compare expressions. like [(">=", 'v2.3.3.3')]
    for path, real_hash in static_map.items():
        for version in version_lst[1:]:
            logger.noise('version: %s, path: %s', version.vstring, path)
            fingerprint = fingerprint_map.get(version.vstring)
            fingerprint_hash = fingerprint.get(path)
            if fingerprint_hash is None:
                continue
            if real_hash == fingerprint_hash:
                operator = ('<=', version.vstring)
            else:
                operator = ('!=', version.vstring)
            version_compare_lst.add(operator)
            logger.noise(
                'real hash: %s, fingerprint: %s. operator is %s',
                real_hash, fingerprint_hash, operator
            )
    logger.debug("operator: %s", version_compare_lst)
    return version_compare_lst
