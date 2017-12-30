#!/usr/bin/env python3
# coding=utf-8
from __future__ import absolute_import, unicode_literals

from logging import (
    CRITICAL, FATAL, ERROR, WARNING,
    WARN, INFO, DEBUG, NOTSET,
)

from .traceback2 import format_exc, print_exc
from .mylogger import MyHTTPHandler, apply_handler, MultiprocessRotatingFileHandler
from .mylogging import (
    basicConfig, colorConfig, getLogger, FILE_LOG_FORMAT,
    VERBOSE, TRACE, NOISE, LOWEST,
)

VERSION = (0, 7, 2, 2)
VERSION_STR = "{}.{}.{}.{}".format(*VERSION)

__version__ = VERSION
__author__ = "Aploium<i@z.codes>"
