#!/usr/bin/env python3
# coding=utf-8
from __future__ import unicode_literals
import sys
import inspect

if sys.version_info[0] == 3:
    _unwrap = inspect.unwrap
    
    
    def getblock(lines):
        """Extract the block of code at the top of the given list of lines."""
        blockfinder = inspect.BlockFinder()
        try:
            tokens = inspect.tokenize.generate_tokens(iter(lines).__next__)
            for _token in tokens:
                blockfinder.tokeneater(*_token)
        except (inspect.EndOfBlock, IndentationError):
            pass
        return lines  # different to builtin inspect is here

else:
    # copied from python3.6 inspect
    def _unwrap(func, stop=None):
        if stop is None:
            def _is_wrapper(f):
                return hasattr(f, '__wrapped__')
        else:
            def _is_wrapper(f):
                return hasattr(f, '__wrapped__') and not stop(f)
        f = func  # remember the original func for error reporting
        memo = {id(f)}  # Memoise by id to tolerate non-hashable objects
        while _is_wrapper(func):
            func = func.__wrapped__
            id_func = id(func)
            if id_func in memo:
                raise ValueError('wrapper loop when unwrapping {!r}'.format(f))
            memo.add(id_func)
        return func
    
    
    # from python 2.7 inspect
    def getblock(lines):
        """Extract the block of code at the top of the given list of lines."""
        blockfinder = inspect.BlockFinder()
        try:
            inspect.tokenize.tokenize(iter(lines).next, blockfinder.tokeneater)
        except (inspect.EndOfBlock, IndentationError):
            pass
        return lines


def getsourcelines(obj):
    obj = _unwrap(obj)
    lines, lnum = inspect.findsource(obj)
    
    if inspect.ismodule(obj):
        return lines, 0
    else:
        return getblock(lines[lnum:]), lnum + 1
