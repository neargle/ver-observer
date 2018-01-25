#!/usr/bin/env python3
# coding=utf-8
# by nearg1e (nearg1e.com@gmail[dot]com)
""" File: tests/test_options.py """
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from observer.options import call_parser

def main():
    print(call_parser())

if __name__ == '__main__':
    main()
