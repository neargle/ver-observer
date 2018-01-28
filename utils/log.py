#!/usr/bin/env python3
# coding=utf-8
# by nearg1e (nearg1e.com@gmail[dot]com)
""" File: utils/log.py """

import os
import ext.err_hunter as err_hunter

from .base import project_path
from .var import DEFAULT_LOGGING_LEVEL, DEFAULT_FILEPATH


LOGGER_LEVELS = {
    'CRITICAL': 50,
    'ERROR': 40,
    'WARNING': 30,
    'INFO': 20,
    'VERBOSE': 15,
    'DEBUG': 10,
    'TRACE': 8,
    'NOISE': 6,
    'LOWEST': 1
}


def init_log(level=DEFAULT_LOGGING_LEVEL, logfile=DEFAULT_FILEPATH):
    """init logger."""
    logfile = os.path.join(project_path(), logfile)
    if isinstance(level, str):
        level = LOGGER_LEVELS.get(level.upper())
    err_hunter.basicConfig(
        level,
        logfile=logfile,
        file_level=err_hunter.VERBOSE,
        maxBytes=1024 * 1024 * 5, backupCount=3, color=True
    )


LOGGER = err_hunter.getLogger()
