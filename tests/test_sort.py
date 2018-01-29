#!/usr/bin/env python3
# coding=utf-8
# by nearg1e (nearg1e.com@gmail[dot]com)
""" File: tests/test_sort.py """


import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))


from observer.version import str2version
from functools import cmp_to_key
from observer.version import version_compare_sort


def _main():
    lst = [('<', '1.1.0'), ('>=', '1.1.0'), ('>=', '1.1.1'), ('<=', '1.1.1')]
    lst.reverse()
    print(sorted(lst, key=cmp_to_key(version_compare_sort)))


if __name__ == '__main__':
    _main()
