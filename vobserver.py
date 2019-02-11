#!/usr/bin/env python3
# coding=utf-8
# by nearg1e (nearg1e.com@gmail[dot]com)
"""
                        _
                       | |
__   _____ _ __    ___ | |__  ___  ___ _ ____   _____ _ __
\ \ / / _ \ '__|  / _ \| '_ \/ __|/ _ \ '__\ \ / / _ \ '__|
 \ V /  __/ |    | (_) | |_) \__ \  __/ |   \ V /  __/ |
  \_/ \___|_|     \___/|_.__/|___/\___|_|    \_/ \___|_|

                            github.com/neargle/ver-observer


usage: vobserver.py [-h] [-u URL] [-d DEPEND] [--depth DEPTH] [-a] [-v]
                    [--logfile LOGFILE] [--level LEVEL]
                    {new} ...

A tool to detect that which version of web framework using on the target
website.

positional arguments:
  {new}                 sub-command help
    new                 add a new plugin infomation of framework or cms

optional arguments:
  -h, --help            show this help message and exit
  -u URL, --url URL     target website url. like http://blog.neargle.com
  -d DEPEND, --depend DEPEND
                        the develop depend, web framework or cms name. like
                        "django"
  --depth DEPTH         the greater the depth, the more URL will be scan,
                        default 0 is the maximum
  -a, --all             show all plugin introduction
  -v, --verbose         set logger level to "VERBOSE"
  --logfile LOGFILE     log file path
  --level LEVEL         logger level, select in "CRITICAL, ERROR, WARNING,
                        INFO, VERBOSE, DEBUG, TRACE, NOISE, LOWEST"
"""

from observer import run


if __name__ == '__main__':
    run()
