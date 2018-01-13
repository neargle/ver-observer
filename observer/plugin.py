#!/usr/bin/env python3
# coding=utf-8
# by nearg1e (nearg1e.com@gmail[dot]com)
""" File: observer/plugin.py """

import os
import json
from collections import Counter

from utils.var import PLUGIN_PATH as plugin_path
from utils.common import project_path


def all_plugin():
    """return all plugins and their info"""
    plugins = []
    abs_plugin_path = os.path.join(project_path(), plugin_path)
    for (root, _, filenames) in os.walk(abs_plugin_path, followlinks=False):
        for filename in filenames:
            if filename.endswith(".json"):
                plugin_file = os.path.join(root, filename)
                plugins.append(load(plugin_file))
    return plugins


def load(filepath):
    """return plugin info"""
    with open(filepath, 'r') as _fp:
        return json.load(_fp, encoding='utf-8')


def search(alias):
    """return plugin with alias info"""
    for plugin in all_plugin():
        if alias in plugin.get("alias"):
            return plugin


def file_distribute(plugin_info):
    """
    Return file path and it's weight. Like {2:['n/e/a/r/g/l/e.css']}

    :param plugin_info: plugin info dictionary.
    """
    all_filepath_in_fingerprint = []
    distribution = {}
    fingerprint = plugin_info.get('fingerprint')
    for (_, version_fp) in fingerprint.items():
        filepath_lst = version_fp.keys()
        all_filepath_in_fingerprint.extend(filepath_lst)
    counter_fp = Counter(all_filepath_in_fingerprint)
    for filepath, weight in counter_fp.items():
        distribution.setdefault(weight, set()).add(filepath)
    return distribution
