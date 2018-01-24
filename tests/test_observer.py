#!/usr/bin/env python3
# coding=utf-8
# by nearg1e (nearg1e.com@gmail[dot]com)
""" File: tests/test_observer.py """

import os
import sys
import json
import inspect

sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))

from observer.plugin import file_distribute, search
from utils.log import LOGGER as logger
from utils.common import file_md5, byte_md5
from observer.scan import static_hash_map
import config

try:
    from test_data import target_website
except ImportError:
    target_website = 'http://google.com'


def file_distribute_test():
    """
    Return like:
    {1: {'/static/admin/admin/js/vendor/jquery/LICENSE-JQUERY.txt'},
    2: {'/static/admin/admin/img/sorting-icons.gif',
    '/static/admin/admin/img/tooltag-add.svg',
    '/static/admin/admin/js/vendor/select2/i18n/gl.js',
    '/static/admin/admin/js/vendor/select2/i18n/ru.js',
    '/static/admin/admin/img/LICENSE',
    '/static/admin/admin/js/vendor/select2/i18n/km.js',
    '/static/admin/admin/img/tool-left.gif',
    '/static/admin/admin/js/vendor/select2/i18n/da.js',
    '/static/admin/admin/img/tooltag-add.png',
    '/static/admin/admin/js/vendor/select2/i18n/sv.js',
    '/static/admin/admin/img/icon-changelink.svg',
    '/static/admin/admin/fonts/Roboto-Bold-webfont.woff',
    '/static/admin/admin/img/gis/move_vertex_off.svg',
    '/static/admin/admin/img/icon_deletelink.gif',
    '/static/admin/admin/img/gis/move_vertex_on.svg',
    '/static/admin/admin/img/tooltag-add.gif',
    '/static/admin/admin/js/vendor/select2/i18n/es.js',
    '/static/admin/admin/js/vendor/select2/i18n/pt.js',
    '/static/admin/admin/img/icon-no.gif',
    '/static/admin/admin/js/autocomplete.js',
    '/static/admin/admin/img/icon_error.gif',
    '/static/admin/admin/js/vendor/select2/i18n/pt-BR.js',
    '/static/admin/admin/img/chooser_stacked-bg.gif',
    '/static/admin/admin/img/icon-unknown.svg',
    '/static/admin/admin/js/vendor/select2/select2.full.js',
    '/static/admin/admin/js/vendor/select2/LICENSE-SELECT2.md',
    '/static/admin/admin/js/vendor/select2/i18n/hi.js',
    '/static/admin/admin/img/sorting-icons.svg',
    '/static/admin/admin/img/chooser-bg.gif',
    '/static/admin/admin/js/getElementsBySelector.js',
    '/static/admin/admin/js/vendor/select2/i18n/zh-TW.js',
    '/static/admin/admin/img/selector-icons.svg',
    '/static/admin/admin/img/tooltag-arrowright.svg',
    '/static/admin/admin/js/vendor/select2/i18n/hu.js',
    '/static/admin/admin/js/vendor/select2/i18n/sr.js',
    '/static/admin/admin/img/icon_clock.gif',
    '/static/admin/admin/css/responsive_rtl.css',
    '/static/admin/admin/js/vendor/select2/i18n/lv.js',
    '/static/admin/admin/img/search.svg',
    '/static/admin/admin/img/icon-clock.svg',
    '/static/admin/admin/img/deleted-overlay.gif',
    '/static/admin/admin/js/vendor/select2/i18n/vi.js',
    '/static/admin/admin/js/vendor/select2/i18n/ar.js',
    '/static/admin/admin/js/cancel.js',
    '/static/admin/admin/css/responsive.css',
    '/static/admin/admin/img/tooltag-arrowright.gif',
    '/static/admin/admin/js/vendor/select2/i18n/ja.js',
    '/static/admin/admin/js/popup_response.js',
    '/static/admin/admin/js/vendor/select2/i18n/eu.js',
    '/static/admin/admin/css/fonts.css',
    '/static/admin/admin/js/vendor/select2/i18n/he.js',
    '/static/admin/admin/js/vendor/select2/i18n/ko.js',
    '/static/admin/admin/fonts/Roboto-Light-webfont.woff',
    '/static/admin/admin/js/vendor/select2/i18n/pl.js',
    '/static/admin/admin/js/vendor/jquery/jquery.js',
    '/static/admin/admin/img/gis/move_vertex_on.png',
    '/static/admin/admin/js/vendor/select2/i18n/ms.js',
    '/static/admin/admin/img/icon_calendar.gif',
    '/static/admin/admin/img/tooltag-add_over.gif',
    '/static/admin/admin/js/vendor/select2/i18n/tr.js',
    '/static/admin/admin/js/admin/ordering.js',
    '/static/admin/admin/js/vendor/select2/i18n/th.js',
    '/static/admin/admin/js/vendor/xregexp/xregexp.min.js',
    '/static/admin/admin/css/autocomplete.css',
    '/static/admin/admin/img/tool-right.gif',
    '/static/admin/admin/js/vendor/select2/i18n/lt.js',
    '/static/admin/admin/js/vendor/select2/i18n/az.js',
    '/static/admin/admin/img/icon-addlink.svg',
    '/static/admin/admin/js/vendor/xregexp/xregexp.js',
    '/static/admin/admin/js/LICENSE-JQUERY.txt',
    '/static/admin/admin/img/changelist-bg_rtl.gif',
    '/static/admin/admin/img/icon-alert.svg',
    '/static/admin/admin/fonts/Roboto-Regular-webfont.woff',
    '/static/admin/admin/js/vendor/select2/i18n/id.js',
    '/static/admin/admin/img/nav-bg-selected.gif',
    '/static/admin/admin/js/vendor/select2/i18n/fi.js',
    '/static/admin/admin/css/vendor/select2/LICENSE-SELECT2.md',
    '/static/admin/admin/js/vendor/select2/i18n/sr-Cyrl.js',
    '/static/admin/admin/img/tool-left_over.gif',
    '/static/admin/admin/js/vendor/select2/i18n/it.js',
    '/static/admin/admin/img/icon-unknown.gif',
    '/static/admin/admin/js/compress.py',
    '/static/admin/admin/js/vendor/select2/i18n/cs.js',
    '/static/admin/admin/img/icon-deletelink.svg',
    '/static/admin/admin/img/tool-right_over.gif',
    '/static/admin/admin/js/vendor/select2/i18n/ro.js',
    '/static/admin/admin/js/vendor/select2/i18n/fa.js',
    '/static/admin/admin/img/icon-no.svg',
    '/static/admin/admin/js/vendor/select2/i18n/ca.js',
    '/static/admin/admin/img/icon_success.gif',
    '/static/admin/admin/css/vendor/select2/select2.min.css',
    '/static/admin/admin/js/vendor/select2/i18n/bg.js',
    '/static/admin/admin/js/vendor/xregexp/LICENSE-XREGEXP.txt',
    '/static/admin/admin/img/icon-yes.svg',
    '/static/admin/admin/js/vendor/select2/i18n/hr.js',
    '/static/admin/admin/js/vendor/select2/i18n/zh-CN.js',
    '/static/admin/admin/img/selector-search.gif',
    '/static/admin/admin/img/icon-unknown-alt.svg',
    '/static/admin/admin/js/vendor/select2/i18n/en.js',
    '/static/admin/admin/js/vendor/select2/i18n/nb.js',
    '/static/admin/admin/img/nav-bg-grabber.gif',
    '/static/admin/admin/js/vendor/select2/i18n/mk.js',
    '/static/admin/admin/img/README.txt',
    '/static/admin/admin/js/vendor/select2/i18n/sk.js',
    '/static/admin/admin/img/gis/move_vertex_off.png',
    '/static/admin/admin/img/selector-icons.gif',
    '/static/admin/admin/js/vendor/select2/select2.full.min.js',
    '/static/admin/admin/img/icon-yes.gif',
    '/static/admin/admin/js/prepopulate_init.js',
    '/static/admin/admin/js/vendor/select2/i18n/el.js',
    '/static/admin/admin/img/icon_addlink.gif',
    '/static/admin/admin/img/tooltag-arrowright.png',
    '/static/admin/admin/img/calendar-icons.svg',
    '/static/admin/admin/js/vendor/select2/i18n/fr.js',
    '/static/admin/admin/js/vendor/select2/i18n/uk.js',
    '/static/admin/admin/img/tooltag-arrowright_over.gif',
    '/static/admin/admin/js/related-widget-wrapper.js',
    '/static/admin/admin/img/icon-calendar.svg',
    '/static/admin/admin/img/icon_alert.gif',
    '/static/admin/admin/css/vendor/select2/select2.css',
    '/static/admin/admin/img/inline-delete.svg',
    '/static/admin/admin/js/vendor/select2/i18n/is.js',
    '/static/admin/admin/js/vendor/select2/i18n/de.js',
    '/static/admin/admin/fonts/README.txt',
    '/static/admin/admin/js/vendor/select2/i18n/et.js',
    '/static/admin/admin/js/vendor/select2/i18n/nl.js',
    '/static/admin/admin/img/icon_changelink.gif'},
    3: {'/static/admin/admin/img/inline-delete.png',
    '/static/admin/admin/js/vendor/jquery/jquery.min.js',
    '/static/admin/admin/fonts/LICENSE.txt',
    '/static/admin/admin/img/inline-restore-8bit.png',
    '/static/admin/admin/js/change_form.js',
    '/static/admin/admin/img/changelist-bg.gif',
    '/static/admin/admin/img/icon_searchbox.png',
    '/static/admin/admin/css/ie.css',
    '/static/admin/admin/img/default-bg.gif',
    '/static/admin/admin/js/timeparse.js',
    '/static/admin/admin/img/inline-restore.png',
    '/static/admin/admin/img/inline-delete-8bit.png',
    '/static/admin/admin/img/inline-splitter-bg.gif',
    '/static/admin/admin/img/nav-bg.gif',
    '/static/admin/admin/img/default-bg-reverse.gif',
    '/static/admin/admin/img/nav-bg-reverse.gif'},
    4: {'/static/admin/admin/js/jquery.init.js',
    '/static/admin/admin/css/login.css',
    '/static/admin/admin/css/dashboard.css',
    '/static/admin/admin/js/prepopulate.js',
    '/static/admin/admin/js/jquery.js',
    '/static/admin/admin/js/collapse.js',
    '/static/admin/admin/js/jquery.min.js'},
    5: {'/static/admin/admin/js/prepopulate.min.js',
    '/static/admin/admin/js/SelectBox.js'},
    6: {'/static/admin/admin/css/changelists.css',
    '/static/admin/admin/css/rtl.css',
    '/static/admin/admin/js/urlify.js'},
    7: {'/static/admin/admin/js/collapse.min.js',
    '/static/admin/admin/js/calendar.js'},
    8: {'/static/admin/admin/js/actions.min.js',
    '/static/admin/admin/js/actions.js',
    '/static/admin/admin/js/inlines.js'},
    9: {'/static/admin/admin/js/SelectFilter2.js',
    '/static/admin/admin/js/inlines.min.js',
    '/static/admin/admin/css/forms.css'},
    10: {'/static/admin/admin/css/widgets.css',
    '/static/admin/admin/js/core.js',
    '/static/admin/admin/css/base.css'},
    11: {'/static/admin/admin/js/admin/DateTimeShortcuts.js'},
    14: {'/static/admin/admin/js/admin/RelatedObjectLookups.js'}}
    """
    django = search('django')
    distri = file_distribute(django)
    logger.info(distri)


def mdf_of_file_and_byte_content_test():
    logger.warning('mdf_of_file_and_byte_content_test start!')
    filepath = './observer.py'
    fbyte = open(filepath, 'rb').read()
    assert (file_md5(filepath) == byte_md5(fbyte)) is True
    logger.info('mdf_of_file_and_byte_content_test pass!')


def static_hash_map_test():
    logger.warning('static_hash_map_test start!')
    django = search('django')
    distri = file_distribute(django)
    logger.info('file_distribute end.')
    target_website = 'http://127.0.0.1:8000/'
    map_ = static_hash_map(target_website, distri, depth=0)
    logger.info(json.dumps(map_, indent=4, sort_keys=True))
    logger.info('static_hash_map_test pass!')


def make_version_test():
    logger.warning('make_version_test start!')
    import ext.err_hunter as err_hunter
    from test_data import target_tmp_hash_map_all as target_tmp_hash_map
    from observer.version import make_version
    django = search('django')
    logger.critical(
        'make_version return: %s',
        make_version(target_tmp_hash_map, django.get('fingerprint'))
    )
    logger.critical(
        'make_version return: %s',
        make_version(target_tmp_hash_map, django.get('reverse_fingerprint'), False)
    )
    logger.info('make_version_test pass!')


def main():
    filter_word = ''
    try:
        filter_word = sys.argv[1]
    except IndexError:
        pass

    current_module = sys.modules[__name__]
    for member, module in inspect.getmembers(current_module):
        if member.endswith('_test') and filter_word in member:
            logger.noise("test function: %s, module: %s", member, str(module))
            getattr(current_module, member)()


if __name__ == '__main__':
    main()
