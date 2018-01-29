# VER-OBSERVER

Detection version of Web framework or CMS or dev-dependence on target website.

## EXAMPLE

> python vobserver.py -u https://www.xxx.com/ -d django -v

![](http://ww1.sinaimg.cn/large/005y7Ba5ly1fnxbwmiawrj31c70w4gsj.jpg)

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

[![asciicast](https://asciinema.org/a/2x0lpXDl9YjsYOMgwAQ8UNtjA.png)](https://asciinema.org/a/2x0lpXDl9YjsYOMgwAQ8UNtjA)

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

err_hunter & version_utils by @aploium
terminaltables by @robpol86

