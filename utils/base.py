#!/usr/bin/env python3
# coding=utf-8
# by nearg1e (nearg1e.com@gmail[dot]com)
""" File: utils/base.py """

import os

def project_path():
    """Return project path."""
    return os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
