#!/usr/bin/env python3
# coding=utf-8
# by nearg1e (nearg1e.com@gmail[dot]com)
""" process manager """

import time
import signal
import collections
import multiprocessing

from utils.log import LOGGER as logger


def init_signal():
    """multiprocessing.Pool 2nd parma."""
    signal.signal(signal.SIGINT, signal.SIG_IGN)


def init_process_pool():
    """new a multi process poll"""
    max_processes = multiprocessing.cpu_count() * 2
    pool = multiprocessing.Pool(max_processes, init_signal)
    return pool


class ProcessTimeoutError(Exception):
    """multiprocess execute timeout."""
    pass


def call_multi_process(function, args_lst, timeout=float('inf')):
    """
    use multiprocessing to call the function like pool.map.

    :param function: function to call.
    :param function: iterable object contains args.
    """
    process_pool = init_process_pool()
    results = {}
    childs = []
    start_time = time.time()

    for args in args_lst:
        def _callback(result, args_=args):
            results[args_] = result

        if not isinstance(args, (list, tuple, collections.Generator)):
            args = (args, )
        childs.append(process_pool.apply_async(function, args, callback=_callback))

    try:
        while True:
            time.sleep(0.5)
            now = time.time()
            if (now - start_time) > timeout:
                raise ProcessTimeoutError("main process time cost: {}".format(now))
            if all((child.ready() for child in childs)):
                break
    except (KeyboardInterrupt, ProcessTimeoutError) as ex:
        logger.warning("stopping by user interrupt. exception info: %s", ex)
        process_pool.terminate()
        process_pool.join()
    else:
        process_pool.close()
        process_pool.join()
    return results
