#!/usr/bin/env python3
# coding=utf-8
from __future__ import unicode_literals

import inspect
import sys

from . import myinspect
from .attr import attributes

PY2 = (sys.version_info[0] == 2)


def real_frame_extract(subframe, filepath, lineno):
    """
    :type subframe: inspect.FrameInfo
    :rtype: inspect.FrameInfo
    """
    frames = inspect.getouterframes(subframe)
    for frame in frames:
        if PY2:
            if frame[1] == filepath and frame[2] == lineno:
                return frame[0]  # type: inspect.FrameInfo
        elif frame.filename == filepath and frame.lineno == lineno:
            return frame.frame  # type: inspect.FrameInfo
    
    return None


def frame_format(frame, interested=None, linerange=5, frame_lineno=None):
    abs_path = frame.f_code.co_filename
    func_name = frame.f_code.co_name
    
    global_vars = attributes(frame.f_globals, from_dict=True, interested=interested)
    local_vars = attributes(frame.f_locals, from_dict=True, interested=interested)
    
    frame_lineno = frame_lineno or frame.f_lineno
    source_lines, first_lineno = myinspect.getsourcelines(frame.f_code)
    
    running_line = source_lines[frame_lineno - first_lineno]
    if PY2:
        running_line = running_line.decode("utf8")
    
    source_lines[frame_lineno - first_lineno] = "--->" \
                                                + running_line.rstrip("\r\n ") \
                                                + "  <---\n"
    
    frag_first_lineno = max(0, frame_lineno - first_lineno - linerange)
    source_lines = source_lines[
                   frag_first_lineno
                   : frame_lineno - first_lineno + linerange
                   ]
    
    if PY2:  # convert bytes to unicode
        _source_lines = []
        for line in source_lines:
            try:
                line = line.decode("utf8")
            except:
                line = repr(line)
            _source_lines.append(line)
        source_lines = _source_lines
    
    frag_first_lineno += first_lineno
    source_lines = "".join(
        (
            "    {:<4}{}".format(i + frag_first_lineno, x)
            if not x.startswith("-")
            else "    {}".format(x)
        )
        for i, x in enumerate(source_lines)
    )
    
    text = """File "{abs_path}", line {frame_lineno}, in {func_name}
{source_lines}
#----global_vars----#
{global_vars}
#----local_vars----#
{local_vars}
#------------------------------------#
""".format(
        abs_path=abs_path, frame_lineno=frame_lineno, func_name=func_name,
        source_lines=source_lines.rstrip("\r\n"), global_vars=global_vars.rstrip(), local_vars=local_vars.rstrip()
    )
    return text
