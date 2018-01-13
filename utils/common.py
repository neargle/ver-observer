#!/usr/bin/env python3
# coding=utf-8
# by nearg1e (nearg1e.com@gmail[dot]com)
""" File: utils/common.py """

import re
import sys
import random
import hashlib
import functools
from string import digits, ascii_lowercase

from .log import LOGGER as logger

RE_REMOVE_BLANK = re.compile(r"\s*")
IS_PY3 = sys.version_info[0] == 3


def get_random_string(length=32, case_pool=digits+ascii_lowercase):
    """Return random string."""
    return ''.join([random.choice(case_pool) for _ in range(length)])

def remove_blank(txt):
    """Remove blank from text."""
    return RE_REMOVE_BLANK.sub("", txt)


def file_md5(filepath):
    """Get file's md5 hash string."""
    hash_md5 = hashlib.md5()
    with open(filepath, "rb") as file_:
        for chunk in iter(lambda: file_.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def byte_md5(bstr):
    """Return md5 string of byte string."""
    return hashlib.md5(bstr).hexdigest()


def repeat_when_false(times=3):
    """
    Decorator for retrying function that will be easy to false and
    easy to true by retry.
    """
    def _decorator(func):
        @functools.wraps(func)
        def _repeat_when_false(*args, **kwargs):
            ret = False
            for time in range(times):
                try:
                    logger.noise('try function: %s, time %s', func.__name__, str(time))
                    ret = func(*args, **kwargs)
                except Exception as ex:
                    logger.debug('exception in retry: %s', str(ex))
                    ret = False
                if ret:
                    break
            return ret
        return _repeat_when_false
    return _decorator
