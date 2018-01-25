#!/usr/bin/env python3
# coding=utf-8
"""
用于版本字符串的转换、比较、范围匹配

用法请看 `test__version_range` 这个函数
"""
from __future__ import absolute_import, division, print_function, unicode_literals
import re
import sys
import operator
from distutils.version import Version as BaseVersion
from distutils.version import LooseVersion as Version

PY3 = sys.version_info[0] == 3
if PY3:
    string_types = str
else:
    # noinspection PyUnresolvedReferences
    string_types = (unicode, str, basestring)

RE_SPLIT_COMPARISON = re.compile(r"^\s*(<=|>=|<|>|!=|==)\s*([^\s,]+)\s*$")
RE_REMOVE_BLANK = re.compile(r"\s*")
COMPMAP = {"<": operator.lt, "<=": operator.le, "==": operator.eq,
           ">": operator.gt, ">=": operator.ge, "!=": operator.ne}


def to_version(version):
    if isinstance(version, string_types):
        return Version(remove_blank(version))
    else:
        return version


def remove_blank(txt):
    """移除空白字符"""
    return RE_REMOVE_BLANK.sub("", txt)


class VersionCond(object):
    def __init__(self, op, version):
        self.version = to_version(version)
        
        if isinstance(op, string_types):
            op = COMPMAP[op]
        self.op = op
    
    def match(self, version):
        if not version or not isinstance(version, (string_types, BaseVersion)):
            return False
        version = to_version(version)
        return self.op(version, self.version)
    
    @classmethod
    def from_str(cls, cond_str):
        m = RE_SPLIT_COMPARISON.search(cond_str)
        if m is not None:
            op = m.group(1)
            version = m.group(2)
        else:
            # 若没有找到操作符, 则认为需要完全匹配版本串
            op = "=="
            version = remove_blank(cond_str)
        
        return cls(op, version)
    
    def __str__(self):
        return "{}({} {})".format(self.__class__.__name__, self.op.__name__, self.version.vstring)


class _CondAll(object):
    """表示匹配任意版本"""
    
    def match(self, version):
        return True


_condall = _CondAll()


class VersionRange(object):
    def __init__(self, ranges):
        if ranges == "all" or ranges is None:
            self.ranges = [[_condall]]
        elif isinstance(ranges, string_types):
            self.ranges = [self.parse_range_str(ranges)]
        elif "all" in ranges or None in ranges:
            self.ranges = [[_condall]]
        else:
            self.ranges = [self.parse_range_str(x) for x in ranges]
    
    def match(self, version):
        version = to_version(version)
        
        for conds in self.ranges:
            if all(cond.match(version) for cond in conds):
                return True
        return False
    
    @staticmethod
    def parse_range_str(range_str):
        split = range_str.split(",")
        return [VersionCond.from_str(x) for x in split]


def test__version_cond():
    for cond in (
            VersionCond(">", "1.5"),
            VersionCond.from_str(">1.5"),
            VersionCond.from_str(">=1.5"),
            VersionCond.from_str(">=1.9"),
            VersionCond.from_str(">=1.10"),
    ):
        assert cond.match("10.0")
        assert cond.match("1.10")
        assert cond.match("1.4.9a1") is False
        assert cond.match("0.9.1p7") is False
    
    for cond in (
            VersionCond("<", "1.5"),
            VersionCond.from_str("<1.5 "),
            VersionCond.from_str("<= 1.5"),
            VersionCond.from_str("<= 1.9"),
            VersionCond.from_str("<=1.4.9b1"),
            VersionCond.from_str(" <1.4.9b1"),
            VersionCond.from_str("<= 1.4.10 "),
            VersionCond.from_str(" <= 1.4.9a1 "),
    ):
        assert cond.match("10.0") is False
        assert cond.match("1.10") is False
        assert cond.match("1.4.9a1")
        assert cond.match("0.9.1p7")
    
    for cond in (
            VersionCond("==", "1.4"),
            VersionCond.from_str(" 1.4 "),
            VersionCond.from_str("== 1.4"),
            VersionCond.from_str("!=1.5"),
    ):
        assert cond.match("1.4")
        assert cond.match("1.5") is False
    
    assert _condall.match("any thing!")


def test__version_range():
    for vr in (
            VersionRange(["1.4", "1.4.1", "1.4.2", "1.5.0", "1.5.1", "1.5.2", "1.6"]),
            VersionRange([">=1.4, <=1.4.2 ", " >=1.5, <1.5.3 ", "==1.6"]),  # 允许空格
            VersionRange([">=1.4, <=1.4.1 ", "1.4.2", " >=1.5, <1.5.3 ", "1.6"]),
            VersionRange("!=1.4.3,!=1.2.3"),
            VersionRange(["!=1.4.3, !=1.2.3"]),
    ):
        assert vr.match("1.4.1")
        assert vr.match("1.4.2")
        assert vr.match("1.4.3") is False
        assert vr.match("1.2.3") is False
        assert vr.match("1.5.0 ")  # 允许空格
        assert vr.match("1.5.1")
        assert vr.match(" 1.5.2")
        assert vr.match("1.6")
    
    vr = VersionRange([">1.5, <1.11", "2.5"])
    assert vr.match("1.10")
    assert vr.match("2.5")
    assert vr.match("1.10.b")  # 允许各种奇怪的版本号
    assert vr.match("1.10+")
    assert vr.match("1.10c")
    assert vr.match("1.9c")
    assert vr.match("1.9.x")
    assert vr.match("1.9.*")
    assert vr.match("1.4z") is False
    assert vr.match("2016") is False
    assert vr.match(None) is False
    assert vr.match(1.11) is False
    assert vr.match(object()) is False
    
    vr = VersionRange(">=2016, <2017")
    assert vr.match("2016春节版")
    vr = VersionRange(">=2016, <2017.1")
    assert vr.match("2016春节版")
    
    # all 和 None 表示匹配所有东西
    for vr in (
            VersionRange(None),
            VersionRange([None]),
            VersionRange("all"),
            VersionRange(["all"]),
    ):
        assert vr.match("match anything!")


if __name__ == "__main__":
    test__version_cond()
    test__version_range()
    
    print("all tests passed!")
