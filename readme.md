# VER-OBSERVER

[![GitHub issues](https://img.shields.io/github/issues/neargle/ver-observer.svg?style=flat-square)](https://github.com/neargle/ver-observer/issues)
[![](https://img.shields.io/github/commits-since/neargle/ver-observer/0.1.0.svg?style=flat-square)](https://github.com/neargle/ver-observer/commits/master)
[![Python 3.x](https://img.shields.io/badge/python-3.x-yellow.svg?style=flat-square)](https://www.python.org/) 
[![GitHub license](https://img.shields.io/badge/license-GPLv3-blue.svg?style=flat-square)](https://github.com/neargle/ver-observer/blob/master/LICENSE)

Detection version of Web framework or CMS or dev-dependence on target website.

[中文文档看这里](http://blog.neargle.com/2018/01/29/ver-observer-a-tool-about-version-detection/)

## INSTALL

```bash
git clone https://github.com/neargle/ver-observer.git
cd ver-observer
pip install -r requirements.txt
python3 vobserver.py
```

## EXAMPLE

for django v2.0.1:

> python vobserver.py -u https://www.xxx.com/ -d django

![](http://ww1.sinaimg.cn/large/005y7Ba5ly1fnxbwmiawrj31c70w4gsj.jpg)

for django v1.9:

> python vobserver.py -u https://www.xxx.com/ -d django -v

![](http://ww1.sinaimg.cn/large/005y7Ba5ly1fnxjltmhxvj30py0bf417.jpg)

New a plugin of framework or CMS. You should clone it to the local first. For example: clone django project to /tmp/django. And: 

> python vobserver.py new -d /tmp/django -s /tmp/django/django/contrib/admin/static -w /static/

More info:

> python vobserver.py new -h

### VIDEO

New a django website and ver-observer it.

```bash
python vobserver.py -a
pip freeze | grep Django
django-admin startproject vobserver_test
python vobserver_test/manage.py runserver > /dev/null 2>&1 &
python vobserver.py -u http://127.0.0.1:8000/ -d django -v
```

[![asciicast](https://asciinema.org/a/ua1WOqMkUummi25QxImlFRNpN.png)](https://asciinema.org/a/ua1WOqMkUummi25QxImlFRNpN)

New a plugin of django.

```
python vobserver.py -a
git clone https://github.com/django/django.git /tmp/django_git_project
python vobserver.py -v new -n django -d /tmp/django_git_project -s /tmp/django_git_project/django/contrib/admin/static -w /static/ --alias django-framework django-admin --dis-suffix php asp
python vobserver.py -a
```

[![asciicast](https://asciinema.org/a/eJUPNOKzIA9imNnlLs8hoYU04.png)](https://asciinema.org/a/eJUPNOKzIA9imNnlLs8hoYU04)

## USAGE & HELP

```bash

                        _
                       | |
__   _____ _ __    ___ | |__  ___  ___ _ ____   _____ _ __
\ \ / / _ \ '__|  / _ \| '_ \/ __|/ _ \ '__\ \ / / _ \ '__|
 \ V /  __/ |    | (_) | |_) \__ \  __/ |   \ V /  __/ |
  \_/ \___|_|     \___/|_.__/|___/\___|_|    \_/ \___|_|

                            github.com/neargle/ver-observer
                                                v0.1.0 beta


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
```

## THIRD-PARTY 

Third-party from great developer and friends in [etx/](https://github.com/neargle/ver-observer/tree/master/ext).

- err_hunter & version_utils by @aploium
- terminaltables by @robpol86

