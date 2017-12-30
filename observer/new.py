#!/usr/bin/env python3
# coding=utf-8
# by nearg1e (nearg1e.com@gmail[dot]com)
""" File: observer/new.py """

import os
import re
import subprocess


class ProjectInfo(object):
    """Analyze git project infomation.

    :param project_path: project_path.
    :param static_path: static_path.
    """

    def __init__(self, target_project_path, static_path):
        self.target_project_path = os.path.realpath(target_project_path)
        if not os.path.isabs(static_path):
            static_path = os.path.join(self.target_project_path, static_path)
        self.static_path = static_path

    def all_version(self):
        """get all version of project by 'git tag'.
        """

        command = ('git', 'tag')
        output = subprocess.check_output(command, cwd=self.target_project_path)
        lines = output.decode().split('\n')
        # Some versions like Alpha(1.9a), Beta(1.9b) is out of consider.
        # Only return final version.
        pat = re.compile(r'^[1-9\.]+$')
        return sorted([to_version(ver_) for ver_ in lines if pat.match(ver_)])
