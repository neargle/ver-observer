# ver-observer

一定程度上能检测 Web 站点所用的依赖或者框架的版本。太晚了文档和图片明天换。

## example

> python vobserver.py -u https://www.xxx.com/ -d django -v

![](http://ww1.sinaimg.cn/large/005y7Ba5ly1fnwuf9pjzjj31cf0lktap.jpg)

## usage & help

```bash
> python vobserver.py -h                                                                                                           master [ad62f1c] untracked
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



