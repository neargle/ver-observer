#!/usr/bin/env python3
# coding=utf-8
# by nearg1e (nearg1e.com@gmail[dot]com)
""" File: observer/__init__.py """

import sys
import json

from utils.log import LOGGER as logger
from utils.common import (
    file_md5 as file_hash,
    byte_md5 as byte_hash
)

from .plugin import search, file_distribute
from .options import call_parser
from .version import make_all
from .scan import static_hash_map
from .vars import APPNAME


def run():
    """main function."""
    args = call_parser()
    check_run_options(args)
    depend = args.depend
    logger.info('searching %s fingerprint infomation.....', depend)
    plugin_info = search(depend)
    if not plugin_info:
        logger.error('%s can not find a fingerprint of %s', APPNAME, depend)
        # logger.info('your can use --all to print all fingerprint supported.')
        # TODO: show the request fingerprint url in github
        sys.exit()
    logger.info('already found %s fingerprint.', depend)
    distri = file_distribute(plugin_info)
    logger.info('start to request hash map on %s in depth %d.', args.url, args.depth)
    hash_map = static_hash_map(args.url, distri, args.depth)
    logger.verbose('show the hash map: %s', json.dumps(hash_map, indent=4, sort_keys=True))
    logger.info('let\'s observer which version of %s.', depend)
    version_set = make_all(hash_map, plugin_info)
    


def check_run_options(args):
    """url(-u/--url) and frameworks name(-d/--depend) is required."""
    if not args.url or not args.depend:
        logger.error("url(-u/--url) and frameworks name(-d/--depend) is required")
        sys.exit()
