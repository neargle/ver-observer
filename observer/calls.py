#!/usr/bin/env python3
# coding=utf-8
# by nearg1e (nearg1e.com@gmail[dot]com)
""" File: observer/calls.py """

from ext.terminaltables import AsciiTable
from utils.log import LOGGER as logger

from .plugin import all_plugin

def show_all():
    """show all plugin, --all/-a option."""
    logger.info('show all plugin introduction')
    table_lst = [
        ('framework name', 'tags')
    ]
    for plugin_info in all_plugin():
        tags = ', '.join(plugin_info.get('alias'))
        table_lst.append((plugin_info.get('framework'), tags))
    table = AsciiTable(table_lst)
    show_output(table.table)


def show_output(msg):
    """show result."""
    logger.critical('result: \n\n%s\n', msg)
    # print('\n{}\n'.format(msg))
