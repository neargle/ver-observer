#!/usr/bin/env python3
# coding=utf-8
# by nearg1e (nearg1e.com@gmail[dot]com)
""" File: utils/log.py """

import os
import ext.err_hunter as err_hunter
from .common import project_path


filepath = os.path.join(project_path(), 'django-scan.log')
err_hunter.basicConfig("DEBUG", logfile=filepath, file_level="DEBUG",
                       maxBytes=1024 * 1024 * 5, backupCount=3, color=True
                      )

logger = err_hunter.getLogger()
