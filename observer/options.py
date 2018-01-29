#!/usr/bin/env python3
# coding=utf-8
# by nearg1e (nearg1e.com@gmail[dot]com)
""" option parse in command line """

import sys
import argparse

from utils.log import init_log
from utils.var import DEFAULT_FILEPATH, DEFAULT_LOGGING_LEVEL
from .new import option_interface
from .calls import show_all
from .vars import APP_TITLE_ASCII_ART


def call_parser():
    """call the args parser."""

    print(APP_TITLE_ASCII_ART)

    parser = make_parser()

    # show help message when no option is given
    if not sys.argv[1:]:
        parser.print_help()
        parser.exit()

    args = parser.parse_args()

    # set logger
    if args.verbose:
        args.level = 'verbose'
    init_log(args.level, args.logfile)

    # option: -a/-all
    if args.all:
        show_all()
        parser.exit()

    try:
        sub = getattr(args, 'which')
    except AttributeError:
        pass
    else:
        if sub == 'new':
            option_interface(
                framework_name=args.framework_name,
                target_project_path=args.dir,
                static_path=args.static_path,
                web_static_root=args.web_static_root,
                alias=args.alias,
                dis_suffix=args.dis_suffix
            )
        parser.exit()

    return args


def make_parser():
    """return the parser."""

    desc_text = '''
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
        help='logger level, select in '
        '"CRITICAL, ERROR, WARNING, INFO, VERBOSE, DEBUG, TRACE, NOISE, LOWEST"'
    )

    # new a plugin
    subparsers = parser.add_subparsers(help='sub-command help')
    new_parser = subparsers.add_parser(
        'new',
        help='add a new plugin infomation of framework or cms'
    )
    new_parser.set_defaults(which='new')
    new_parser.add_argument(
        '-n',
        '--framework-name',
        type=str,
        default='',
        help='name of web framework or CMS, like django'
    )
    new_parser.add_argument(
        '-d',
        '--dir',
        type=str,
        required=True,
        help='path to the git project of web framework'
    )
    new_parser.add_argument(
        '-s',
        '--static-path',
        type=str,
        required=True,
        help='the directory of static file (.css file, .ico file) in project'
    )
    new_parser.add_argument(
        '-w',
        '--web-static-root',
        type=str,
        default='/',
        help='file root path in real web file'
    )
    new_parser.add_argument(
        '--alias',
        nargs='+',
        type=str,
        help='set alias, usage: `--alias laravel-php laravel`'
    )
    new_parser.add_argument(
        '--dis-suffix',
        nargs='+',
        type=str,
        help='set file suffix that is not static file in web, usage: '
        '`--dis-suffix php asp`'
    )
    return parser
