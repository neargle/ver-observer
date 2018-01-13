#!/usr/bin/env python3
# coding=utf-8
# by nearg1e (nearg1e.com@gmail[dot]com)
""" File: observer/new.py """

import os
import re
import json
import subprocess
from urllib.parse import urljoin

from utils.log import LOGGER as logger
from .version import str2version
from . import file_hash, byte_hash


class ProjectInfo(object):
    """
    Analyze git project infomation.

    Create file like below :
    {
        "framework": "",
        "alias": [],
        "versions": [],
        "fingerprint": {
            "version": {
                "filepath": "filehash"
            }
        }
    }

    :param project_path: project_path.
    :param static_path: static_path.
    """

    default_info_result = {
        'framework': '',
        'alias': [],
        'versions': [],
        'fingerprint': {}
    }

    def __init__(self, framework_name, target_project_path, static_path, web_static_root):

        target_project_path = os.path.expanduser(target_project_path)
        static_path = os.path.expanduser(static_path)
        web_static_root = os.path.expanduser(web_static_root)

        self.target_project_path = os.path.realpath(target_project_path)
        if not os.path.isabs(static_path):
            static_path = os.path.join(self.target_project_path, static_path)
        self.static_path = static_path
        self.web_static_root = web_static_root
        self.version_lst = self.all_version()
        self.make_result(framework_name)


    def make_result(self, framework_name):
        """Make info_result."""
        logger.info('functions has done. init the result and set the name and alias.')
        self.info_result = self.default_info_result
        self.info_result['framework'] = framework_name
        self.add_alias(framework_name)
        logger.info('set the all versions.')
        self.set_versions()
        logger.info('get hash string of all static file in last versions.')
        self.last_hash()
        logger.info('diff the file version by version and get the info of different file.')
        self.make_diff()


    def _git_exec(self, *args, decode=True):
        """Done 'git' command."""
        master_program = 'git'
        command_tup = (master_program, *args)
        output = subprocess.check_output(command_tup, cwd=self.target_project_path,
                                         stderr=subprocess.STDOUT)
        return output.decode() if decode else output


    def set_versions(self):
        """Set self.info_result['versions']."""
        self.info_result['versions'] = [version.vstring for version in self.version_lst]


    def all_version(self):
        """Get all version of project by 'git tag'."""
        cmd_result = self._git_exec('tag', decode=True)
        lines = cmd_result.split('\n')
        # Some versions like Alpha(1.9a), Beta(1.9b) is out of consider.
        # Only return final version.
        pat = re.compile(r'^[0-9\.]+$')
        versions = sorted([str2version(ver_) for ver_ in lines if pat.match(ver_)])
        versions.reverse()
        return versions


    def last_static(self):
        """all static files in last version."""
        static_files = []
        for (root, _, filenames) in os.walk(self.static_path, followlinks=False):
            for filename in filenames:
                static_files.append(os.path.join(root, filename))
        return static_files


    def last_hash(self):
        """Get all static file's hash string."""
        static_file_lst = self.last_static()
        last_ver = str(self.version_lst[0])
        _dic_link = self.info_result['fingerprint'][last_ver] = {}

        for filepath in static_file_lst:
            md5_string = file_hash(filepath)
            web_file = self.web_file_path(filepath)
            _dic_link[web_file] = md5_string


    def web_file_path(self, path_in_project):
        """Return filepath in web application."""
        if os.path.isabs(path_in_project):
            base_path_length = len(self.static_path)
        else:
            base_path_length = len(
                os.path.relpath(self.static_path, self.target_project_path)
            )
        relative_path = path_in_project[base_path_length:].strip(os.path.sep)
        return urljoin(self.web_static_root, relative_path)


    def make_diff(self):
        """Comparison between versions one by one."""
        for version, prev_version in zip(self.version_lst, self.version_lst[1:]):
            new, old = version.vstring, prev_version.vstring
            output = self._git_exec('diff', '--name-only', new, old,
                                    '--', self.static_path, decode=True)
            filelst = output.split()
            if not filelst:
                continue
            _dic_link = self.info_result['fingerprint'][old] = {}
            for filename in filelst:
                hash_string = self.ancestor_file(old, filename)
                web_file = self.web_file_path(filename)
                _dic_link[web_file] = hash_string


    def ancestor_file(self, vstring, filepath):
        """return the hash of file in one version."""
        args = ('show', '{}:{}'.format(vstring, filepath))
        try:
            output = self._git_exec(*args, decode=False)
        except subprocess.CalledProcessError as ex:
            logger.noise('this path is not exists on disk in version %s:%s', vstring, filepath)
            logger.noise('subprocess error message: %s', ex)
            logger.noise('stderr fatal message: %s', ex.output)
            return
        else:
            return byte_hash(output)


    def add_alias(self, *alias):
        """Add alias to info_result['alias']."""
        self.info_result['alias'].extend(alias)


    def dump_result(self, filename):
        """Dump info_result to file."""
        path = os.path.realpath(filename)
        with open(path, 'w') as _fp:
            json.dump(self.info_result, _fp, indent=4, sort_keys=True)

