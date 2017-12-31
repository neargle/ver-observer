#!/usr/bin/env python3
# coding=utf-8
# by nearg1e (nearg1e.com@gmail[dot]com)
""" File: utils/common.py """

import os
import re
import sys
import random
from string import digits, ascii_lowercase

RE_REMOVE_BLANK = re.compile(r"\s*")
IS_PY3 = sys.version_info[0] == 3

def get_random_string(length=32, case_pool=digits+ascii_lowercase):
    return ''.join([random.choice(case_pool) for _ in range(length)])


def project_path():
    return os.path.dirname(os.path.dirname(os.path.realpath(__file__)))

def remove_blank(txt):
    """Remove blank from text."""
    return RE_REMOVE_BLANK.sub("", txt)