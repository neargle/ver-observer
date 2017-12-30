#!/usr/bin/env python3
# coding=utf-8
from __future__ import absolute_import, unicode_literals

import getpass
import inspect
import logging
import logging.handlers
import os
import platform
import sys
import traceback
import multiprocessing

import requests

from . import frame_operations
from . import traceback2

FORMAT = "[%(levelname)1.1s %(asctime)s %(module)s.%(funcName)s#%(lineno)d] %(message)s"


class MultiprocessRotatingFileHandler(logging.handlers.RotatingFileHandler):
    def __init__(self, *args, **kwargs):
        self._baseFilename = None
        super(MultiprocessRotatingFileHandler, self).__init__(*args, **kwargs)
    
    def format(self, record):
        result = super(MultiprocessRotatingFileHandler, self).format(record)
        result = result.replace("\r", r"\r").replace("\n", r"\n")
        return result
    
    @property
    def baseFilename(self):
        basepath, ext = os.path.splitext(self._baseFilename)
        cur_process = multiprocessing.current_process()
        return "{}.{}-{}{}".format(basepath, cur_process.name, cur_process.pid, ext)
    
    @baseFilename.setter
    def baseFilename(self, value):
        self._baseFilename = value


class MyHTTPHandler(logging.Handler):
    def __init__(self, url, interested=None,
                 method="POST", level=logging.WARNING, callback=None, timeout=10, req_kwargs=None,
                 source_path=None
                 ):
        super(MyHTTPHandler, self).__init__(level)
        
        self.url = url
        self.method = method
        self.req_kwargs = req_kwargs or {}
        self.session = requests.Session()
        self.callback = callback
        self.timeout = timeout
        self.interested = interested
        self.source_path = source_path or os.getcwd()
    
    def mapLogRecord(self, record):
        data = {}
        data.update(record.__dict__)
        
        data.update({
            "_cwd": os.getcwd(),
            "_username": getpass.getuser(),
            "_hostname": platform.node(),
            "_uname": str(platform.uname()),
            "_py_version": sys.version,
        })
        
        if record.levelno >= logging.ERROR:
            real_frame = frame_operations.real_frame_extract(
                inspect.currentframe(),
                filepath=data["pathname"],
                lineno=data["lineno"]
            )
            
            if real_frame is not None:
                data["_logframe"] = frame_operations.frame_format(real_frame, interested=self.interested)
        
        if sys.exc_info() != (None, None, None) and "_traceback" not in data:
            data["_traceback"] = traceback.format_exc()
            
            data["_traceback_frames"] = traceback2.format_exc(with_normal=False)
        
        return data
    
    def _emit(self, record):
        """:type record: logging.LogRecord"""
        
        kwargs = {"timeout": self.timeout, "allow_redirects": False}
        data = self.mapLogRecord(record)  # type: dict
        
        if self.method == "GET":
            kwargs["params"] = data
        else:
            kwargs["data"] = data
        
        kwargs.update(self.req_kwargs)
        resp = self.session.request(
            self.method, self.url, **kwargs
        )
        if self.callback is not None:
            self.callback(record, resp)
    
    def emit(self, record):
        try:
            self._emit(record)
        except:
            self.handleError(record)


def apply_handler(
        url,
        level=logging.WARNING,
        method="POST",
        interested=None,
        parent_name=None,
        callback=None,
        timeout=10,
        req_kwargs=None,
        source_path=None,
        lazy=False,
):
    if lazy:
        logging.basicConfig(
            format=FORMAT,
            level=logging.INFO,
        )
    
    handler = MyHTTPHandler(
        url, interested=interested,
        method=method, level=level,
        callback=callback, timeout=timeout,
        req_kwargs=req_kwargs,
        source_path=source_path,
    )
    handler.setFormatter(logging.Formatter())
    logging.getLogger(parent_name).addHandler(handler)
    return handler
