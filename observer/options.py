#!/usr/bin/env python3
# coding=utf-8
# by nearg1e (nearg1e.com@gmail[dot]com)
""" option parse in command line """

import sys
import argparse

from utils.log import init_log
from utils.var import DEFAULT_FILEPATH, DEFAULT_LOGGING_LEVEL

from .calls import show_all


def call_parser():
    """call the args parser."""
    parser = make_parser()

    # show help message when no option is given
    if not sys.argv[1:]:
        parser.print_help()
        parser.exit()

    args = parser.parse_args()

    # option: -a/-all
    if args.all:
        show_all()
        parser.exit()

    # set logger
    if args.verbose:
        args.level = 'verbose'

    init_log(args.level, args.logfile)

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
        help='target website url. like http://blog.neargle.com'
    )
    parser.add_argument(
        '-d',
        '--depend',
        help='the develop depend, web framework or cms name. like "django"'
    )
    parser.add_argument(
        '--depth',
        required=False,
        default=0,
        type=int,
        help='the greater the depth, the more URL will be scan, default 0 is the maximum'
    )
    parser.add_argument(
        '-a',
        '--all',
        action='store_true',
        help='show all plugin introduction'
    )
    parser.add_argument(
        '-v',
        '--verbose',
        action='store_true',
        help='set logger level to "VERBOSE"'
    )
    parser.add_argument(
        '--logfile',
        type=str,
        default=DEFAULT_FILEPATH,
        help='log file path'
    )
    parser.add_argument(
        '--level',
        type=str,
        default=DEFAULT_LOGGING_LEVEL,
        help='logger level, select in "CRITICAL, ERROR, WARNING, INFO, VERBOSE, DEBUG, TRACE, NOISE, LOWEST"'
    )
    return parser
