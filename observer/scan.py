#!/usr/bin/env python3
# coding=utf-8
# by nearg1e (nearg1e.com@gmail[dot]com)
""" File: observer/scan.py """

from urllib.parse import urljoin
import requests

from utils.log import LOGGER as logger
from utils.var import HTTP_HEADERS
from . import byte_hash


def static_hash_map(origin, distri, depth=4):
    """
    return some hash string of files in website.

    :param origin: Such as: http://google.com, must
        start with scheme, like js url_object.origin.
    :param distri: Dictionary from plugin.file_distribute.
        :like: `{1:'filepath'}`.
    :param depth: Top `depth` weight to run.
    """
    file_hash_map = {}
    all_weight = sorted(distri.keys())
    all_weight.reverse()
    if depth:
        enable_weight = all_weight[:depth]
    else:
        enable_weight = all_weight[:]
    for path in enable_urls(distri, enable_weight):
        url = urljoin(origin, path)
        hashstr = request_file_hash(url)
        logger.info('%s: %s', path, hashstr)
        file_hash_map[path] = hashstr
    return file_hash_map


def request_file_hash(url):
    """Return hash string of file by request url."""
    logger.debug('request get url: %s', url)
    try:
        response = requests.get(url, verify=False,
                                allow_redirects=True, timeout=10, headers=HTTP_HEADERS)
        if response.status_code != 200:
            raise requests.RequestException('Status code error: {}'.format(response.status_code))
    except requests.RequestException as ex:
        logger.warning('request %s, exception: %s', url, str(ex))
        return ''
    else:
        cont = response.content
        return byte_hash(cont)


def enable_urls(distri, keys):
    """return urls for run."""
    urls = []
    for key in keys:
        urls.extend(distri.get(key))
    return urls
