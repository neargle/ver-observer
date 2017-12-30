#!/usr/bin/env python3
# coding=utf-8
from __future__ import absolute_import, unicode_literals
import logging
import logging.handlers
from .third_party import logzero
from .mylogger import MultiprocessRotatingFileHandler
import inspect

# 更多logging的level
#   注释掉的是标准level
# CRITICAL = 50
# ERROR = 40
# WARNING = 30
# INFO = 20
VERBOSE = 15
# DEBUG = 10
TRACE = 8
NOISE = 6
LOWEST = 1

FILE_LOG_FORMAT = "%(asctime)s - %(filename)s:%(lineno)s - %(levelno)s %(levelname)s %(pathname)s %(module)s %(funcName)s %(created)f %(thread)d %(threadName)s %(process)d %(name)s - %(message)s"

_level_installed = False


def _install_custom_levels():
    global _level_installed
    if _level_installed:
        return
    logging.addLevelName(VERBOSE, "VERBOSE")
    logging.addLevelName(TRACE, "TRACE")
    logging.addLevelName(NOISE, "NOISE")
    logging.addLevelName(LOWEST, "LOWEST")


def _lower_level(*levels):
    lowest = 0
    for level in levels:
        if not isinstance(level, int):
            level = logging.getLevelName(level)
        if level < lowest:
            lowest = level
    return lowest


def basicConfig(level=logging.INFO, color=False, handler=None, formatter=None,
                logfile=None, file_level=None, maxBytes=0, backupCount=0,
                file_format=FILE_LOG_FORMAT, multi_process=False,
                ):
    _install_custom_levels()
    
    logging._acquireLock()
    try:
        if len(logging.root.handlers) != 0:
            return
        handler = handler or logging.StreamHandler()
        formatter = formatter or logzero.LogFormatter(color=color)
        handler.setFormatter(formatter)
        logging.root.addHandler(handler)
        
        if logfile:
            if multi_process:
                file_handler_class = MultiprocessRotatingFileHandler
            else:
                file_handler_class = logging.handlers.RotatingFileHandler
            file_handler = file_handler_class(logfile, maxBytes=maxBytes, backupCount=backupCount)
            file_formatter = logging.Formatter(file_format)
            file_handler.setFormatter(file_formatter)
            logging.root.addHandler(file_handler)
            
            if file_level is not None:
                file_handler.setLevel(file_level)
                _root_level = _lower_level(level, file_level)
                handler.setLevel(level)
                logging.root.setLevel(_root_level)
        
        if file_level is None:
            logging.root.setLevel(level)
    
    finally:
        logging._releaseLock()


def colorConfig(level=logging.INFO, handler=None, formatter=None, **kwargs):
    basicConfig(level=level, color=True, handler=handler, formatter=formatter, **kwargs)


def _get_outframe_main(frame):
    outframe = frame.f_back
    return outframe.f_globals["__name__"]


def getLogzeroLogger(name=None, logfile=None, level=logging.NOTSET,
                     formatter=None, maxBytes=0, backupCount=0, fileLoglevel=None):
    name = name or _get_outframe_main(inspect.currentframe())
    
    return logzero.setup_logger(
        name=name, logfile=logfile, level=level, formatter=formatter,
        maxBytes=maxBytes, backupCount=backupCount, fileLoglevel=fileLoglevel,
    )


class EnhancedLogger(logging.Logger):
    def verbose(self, msg, *args, **kwargs):
        """高于 DEBUG, 低于 INFO 的级别"""
        if self.isEnabledFor(VERBOSE):
            self._log(VERBOSE, msg, args, **kwargs)
    
    def trace(self, msg, *args, **kwargs):
        """比 DEBUG 低一层的级别"""
        if self.isEnabledFor(TRACE):
            self._log(TRACE, msg, args, **kwargs)
    
    def noise(self, msg, *args, **kwargs):
        """比 DEBUG 低两层的级别"""
        if self.isEnabledFor(NOISE):
            self._log(NOISE, msg, args, **kwargs)
    
    def lowest(self, msg, *args, **kwargs):
        """最低级别的log"""
        if self.isEnabledFor(LOWEST):
            self._log(LOWEST, msg, args, **kwargs)


def getLogger(name=None):
    """

    Args:
        name (str|int): 若不指定则会自动获取

    Returns:
        EnhancedLogger: 比标准logger多了一些级别
        
    :rtype: EnhancedLogger
    """
    name = name or _get_outframe_main(inspect.currentframe())
    
    _old_cls = logging.Logger.manager.loggerClass
    try:
        logging.Logger.manager.loggerClass = EnhancedLogger
        
        logger = logging.getLogger(name)  # type: EnhancedLogger
    finally:
        logging.Logger.manager.loggerClass = _old_cls
    
    return logger  # type: EnhancedLogger
