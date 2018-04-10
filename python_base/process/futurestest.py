#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-04-04 08:41:17
# @Author  : Longzx (longzongxing@163.com)
# @Link    : http://www.cnblogs.com/lonelyhiker/
# @Version : $Id$

from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor, Executor
from time import time, ctime, sleep
from functools import wraps
"""
concurrent.futures模块为异步执行可调用项提供了一个高级接口。

异步操作可以由线程实现（通过ThreadPoolExecutor），
或者由进程实现（通过ProcessPoolExecutor）。两者实现了相同的接口，这些接口是定义在抽象类Executor中的。

"""


def gcd(args):
    a, b = args
    low = min(a, b)
    for i in range(low, 1, -1):
        if a % i == 0 and b % i == 0:
            return i

numbers = [(2, 12),
           (2, 12),
           (23443332, 49024902),
           (21444232, 82883392),
           (776677832, 37983842),
           (8, 2)
           ]


def logger(fun):
    @wraps(fun)
    def wrapper(*args, **kwargs):
        print('{} begin at {}'.format(fun.__name__, ctime()))
        starttm = time()
        fun(*args, **kwargs)
        endtm = time()
        print('{} end at {}'.format(fun.__name__, ctime()))
        print('total time:{}'.format(endtm - starttm))
    return wrapper


@logger
def fun1():
    for x in numbers:
        print(gcd(x))


@logger
def fun2():
    pool = ThreadPoolExecutor(max_workers=4)
    result = list(pool.map(gcd, numbers))


@logger
def fun3():
    pool = ProcessPoolExecutor(max_workers=4)
    result = list(pool.map(gcd, numbers))
    for x in result:
        print(x)


@logger
def fun4():
    executor = ProcessPoolExecutor(max_workers=4)
    results = []
    for i in numbers:
        future = executor.submit(gcd, args=i)
        results.append(future)
    for x in results:
        print(x.result())

if __name__ == '__main__':
    fun3()
    fun4()
