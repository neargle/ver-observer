#!/usr/bin/env python3
# coding=utf-8
# by nearg1e (nearg1e.com@gmail[dot]com)
""" File: observer/scan.py """

from urllib.parse import urljoin, urlparse
import requests

from utils.log import LOGGER as logger
from utils.var import HTTP_HEADERS
from utils.common import repeat_when_false
from utils.process import call_multi_process

from .version import str2version
from . import byte_hash


@repeat_when_false(4)
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


def static_hash_map(origin, distri, depth=0):
    """
    return some hash string of files in website.

    :param origin: Such as: http://google.com, must
        start with scheme, like js url_object.origin.
    :param distri: Dictionary from plugin.file_distribute.
        :like: `{1:'filepath'}`.
    :param depth: Top `depth` weight to run.
    """
    all_weight = sorted(distri.keys(), reverse=True)
    if depth:
        enable_weight = all_weight[:depth]
    else:
        enable_weight = all_weight[:]

    def _gen_url():
        for path in enable_urls(distri, enable_weight):
            url = urljoin(origin, path)
            yield url

    result = call_multi_process(request_file_hash, _gen_url())
    for url_key in result:
        path = urlparse(url_key).path
        result[path] = result.pop(url_key)
    return result
