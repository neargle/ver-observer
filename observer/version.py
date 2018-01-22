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


def make_version(static_map, fingerprint):
    """return version expression."""
    version_compare_lst = []
    key_lst = fingerprint.keys()
    version_lst = sorted([str2version(ver_) for ver_ in key_lst], reverse=True)
    last = version_lst[0]
    # compare to last version
    def _is_last():
        last_fingerprint = fingerprint.get(last.vstring)
        for path in last_fingerprint.keys():
            hash_string = static_map.get(path, '')
            if not hash_string:
                continue
            if hash_string == last_fingerprint.get(path):
                yield True
            else:
                logger.noise(
                    'path %s, real hash: %s, hash in last: %s',
                    path, hash_string, last_fingerprint.get(path)
                )
                yield False

    if all(_is_last()):
        version_compare_lst.append((">=", last))
    return version_compare_lst
