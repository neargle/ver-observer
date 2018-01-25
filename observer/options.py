#!/usr/bin/env python3
# coding=utf-8
# by nearg1e (nearg1e.com@gmail[dot]com)
""" option parse in command line """

import sys
import argparse


def call_parser():
    """call the args parser."""
    parser = make_parser()

    # show help message when no option is given
    if not sys.argv[1:]:
        parser.print_help()
        parser.exit()

    args = parser.parse_args()
    return args


def make_parser():
    """return the parser."""

    desc_text = '''\
    A tool to detect that which version of web framework \
    using on the target website. \
    '''
    parser = argparse.ArgumentParser(
        description=desc_text
    )
    parser.add_argument(
        '-u',
        '--url',
        required=True,
        help='target website url. like http://blog.neargle.com'
    )
    parser.add_argument(
        '-d',
        '--depend',
        required=True,
        help='the develop depend, web framework or cms name. like "django"'
    )
    parser.add_argument(
        '--depth',
        required=False,
        default=0,
        type=int,
        help='the greater the depth, the more URL will be scan, default 0 is the maximum'
    )
    return parser
