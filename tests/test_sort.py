#!/usr/bin/env python3
# coding=utf-8
# by nearg1e (nearg1e.com@gmail[dot]com)
""" File: tests/test_sort.py """


import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))


from observer.version import str2version
from functools import cmp_to_key


def version_compare_sort(prev_, next_):
    """
    version compare sort cmp function.
    compare version first and operate next.
    """
    prev_ver = str2version(prev_[1])
    next_ver = str2version(next_[1])
    if prev_ver > next_ver:
        return 1
    elif prev_ver < next_ver:
        return -1
    else:
        # next_ver == prev_ver
        if prev_[0].strip('=') == '>':
            return -1
        else:
            return 1


def _main():
    lst = [('<', '1.1.0'), ('>=', '1.1.0'), ('>=', '1.1.1'), ('<=', '1.1.1')]
    lst.reverse()
    print(sorted(lst, key=cmp_to_key(version_compare_sort)))


if __name__ == '__main__':
    _main()
