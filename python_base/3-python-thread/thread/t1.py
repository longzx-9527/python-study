#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-03-30 10:59:58
# @Author  : Longzx (longzongxing@163.com)
# @Link    : http://www.cnblogs.com/lonelyhiker/
# @Version : $Id$

from time import time, sleep, ctime
from threading import Thread, current_thread

num = 3


def fun(name, sec, n):
    global num
    num = n
    print('begin 当前正在执行的线程是: {} name={} sleep:{}  num={}'.format(
        current_thread(), name, sec, num))

    sleep(sec)
    print('end 当前正在执行的线程是: {} name={} sleep:{}  num={}'.format(
        current_thread(), name, sec, num))


def main1():
    pcs = []
    names = ['tom', 'jack', 'pet']
    secs = [3, 2, 5]
    nums = [8, 7, 5]

    # 创建进程
    for i in range(3):
        p = Thread(target=fun, args=(names[i], secs[i], nums[i]))
        pcs.append(p)

    # 启动进程
    for i in range(3):
        pcs[i].start()

    # 设置等所有进程执行完毕退出
    for i in range(3):
        pcs[i].join()


if __name__ == '__main__':
    print('main1 begin at {}'.format(ctime()))
    starttm = time()
    main1()
    print('main1 end at {}'.format(ctime()))
    print('总共用时:{}'.format(time() - starttm))
