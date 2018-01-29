#!/usr/bin/env python3
# coding=utf-8
# by nearg1e (nearg1e.com@gmail[dot]com)
""" File: observer/vars.py """

from requests.packages import urllib3 as requests_ul3
requests_ul3.disable_warnings(requests_ul3.exceptions.InsecureRequestWarning)


APPNAME = 'ver-observer'
APP_TITLE_ASCII_ART = r'''
                        _                                  
                       | |                                 
__   _____ _ __    ___ | |__  ___  ___ _ ____   _____ _ __ 
\ \ / / _ \ '__|  / _ \| '_ \/ __|/ _ \ '__\ \ / / _ \ '__|
 \ V /  __/ |    | (_) | |_) \__ \  __/ |   \ V /  __/ |   
  \_/ \___|_|     \___/|_.__/|___/\___|_|    \_/ \___|_|   
                                                           
                            github.com/neargle/ver-observer
                                                v0.1.0 beta

'''
