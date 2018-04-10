#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-03-30 11:37:33
# @Author  : Longzx (longzongxing@163.com)
# @Link    : http://www.cnblogs.com/lonelyhiker/
# @Version : $Id$


from time import time, ctime, sleep
from multiprocessing import Pool, current_process

"""
Multiprocessing.Pool可以提供指定数量的进程供用户调用，当有新的请求提交到pool中时，如果池还没有满，
那么就会创建一个新的进程用来执行该请求；但如果池中的进程数已经达到规定最大值，那么该请求就会等待，
直到池中有进程结束，才会创建新的进程来执行它。在共享资源时，只能使用Multiprocessing.Manager类，
而不能使用Queue或者Array。
用途
Pool类用于需要执行的目标很多，而手动限制进程数量又太繁琐时，如果目标少且不用控制进程数量则可以用Process类。




"""


def fun(n):
    print('fun begin={} {n}*{n}={m}'.format(current_process().name, n=n, m=n))
    sleep(2)
    print('fun end={} {n}*{n}={m}'.format(current_process().name, n=n, m=n * n))
    return n * n


def fun1(n, m=0):
    sleep(0.01)
    print('current_process={} {n}*{n}={mm}'.format(current_process().name, n=n, mm=m))
    return n * n


def func(msg):
    print("{} {}:".format(current_process().name, msg))
    time.sleep(3)
    print("end {}".format(current_process().name))


def callbck():
    print('我执行完了')


def main():
    for i in range(100):
        fun(i)


def main1():
    lst = [x for x in range(4)]
    print(lst)
    pool = Pool(processes=3)
    pool.map(fun, lst)
    pool.close()
    pool.join()


def main11():
    lst = [x for x in range(4)]
    print(lst)
    pool = Pool(processes=3)
    pool.map_async(fun, lst)
    pool.close()
    pool.join()


def main2():
    pool = Pool(processes=3)

    for i in range(4):
        msg = "hello %d" % (i)
        pool.apply_async(fun, (i,))

    print('main22222222222')
    pool.close()
    pool.join()


def main4():
    with Pool(processes=4) as pool:         # start 4 worker processes
        # evaluate "f(10)" asynchronously in a single process
        result = pool.apply_async(fun, (10,))
        # prints "100" unless your computer is *very* slow
        print(result.get(timeout=1))

        print(pool.map(fun, range(10)))       # prints "[0, 1, 4,..., 81]"

        it = pool.imap(fun, range(10))
        print(next(it))                     # prints "0"
        print(next(it))                     # prints "1"
        # prints "4" unless your computer is *very* slow
        print(it.next(timeout=1))

        result = pool.apply_async(time.sleep, (10,))
        # raises multiprocessing.TimeoutError
        print(result.get(timeout=1))


def main3():
    pool = Pool(processes=3)
    for i in range(4):
        r = pool.apply(fun, (i,))
        print('r=', r)
    print('main3333333333333333')
    pool.close()
    pool.join()


def printfun(fun):
    print('{} begin at {}'.format(fun.__name__, ctime()))
    starttm = time()
    fun()
    print('{} end at {}'.format(fun.__name__, ctime()))
    print('{}总共用时:{}'.format(fun.__name__, time() - starttm))


if __name__ == '__main__':
    # printfun(main1)
    # printfun(main11)
    # printfun(main3)
    printfun(main2)
