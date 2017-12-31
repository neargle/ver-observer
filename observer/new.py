#!/usr/bin/env python3
# coding=utf-8
# by nearg1e (nearg1e.com@gmail[dot]com)
""" File: observer/new.py """

import os
import re
import subprocess
from urllib.parse import urljoin

from utils.common import file_md5
from .version import str2version


class ProjectInfo(object):
    """Analyze git project infomation.

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

    def __init__(self, target_project_path, static_path, web_static_root):
        self.target_project_path = os.path.realpath(target_project_path)
        if not os.path.isabs(static_path):
            static_path = os.path.join(self.target_project_path, static_path)
        self.static_path = static_path
        self.web_static_root = web_static_root
        self.version_lst = self.all_version()
        self.info_result = self.default_info_result


    def _git_exec(self, *args):
        """git command.
        """

        master_program = 'git'
        command_tup = (master_program, *args)
        output = subprocess.check_output(command_tup, cwd=self.target_project_path)
        return output.decode()


    def all_version(self):
        """get all version of project by 'git tag'.
        """

        cmd_result = self._git_exec('tag')
        lines = cmd_result.split('\n')
        # Some versions like Alpha(1.9a), Beta(1.9b) is out of consider.
        # Only return final version.
        pat = re.compile(r'^[1-9\.]+$')
        versions = sorted([str2version(ver_) for ver_ in lines if pat.match(ver_)])
        versions.reverse()
        return versions


    def last_static(self):
        """all static files in last version.
        """

        static_files = []
        for (root, _, filenames) in os.walk(self.static_path, followlinks=False):
            for filename in filenames:
                static_files.append(os.path.join(root, filename))
        return static_files


    def last_hash(self):
        """Get all static file's hash string.
        """

        static_file_lst = self.last_static()
        last_ver = str(self.version_lst[0])
        base_path_length = len(self.static_path)
        _dic_link = self.info_result['fingerprint'][last_ver] = {}

        for filepath in static_file_lst:
            md5_string = file_md5(filepath)
            relative_path = filepath[base_path_length:].strip(os.path.sep)
            print(relative_path)
            web_file_path = urljoin(self.web_static_root, relative_path)
            _dic_link[web_file_path] = md5_string
        return _dic_link


    def add_alias(self, *alias):
        """add alias to info_result['alias'].
        """

        self.info_result['alias'].extend(alias)
