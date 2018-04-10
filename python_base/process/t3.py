#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-03-30 16:45:31
# @Author  : Longzx (longzongxing@163.com)
# @Link    : http://www.cnblogs.com/lonelyhiker/
# @Version : $Id$

from multiprocessing import Process, Queue, Manager, Pool
from time import sleep, time, ctime

"""
多个小贩烤卖烤肠
多个吃货在排队买烤肠

"""


def makeSausage(queue, name):
    print('{} 技师正在制作烤肠！！！'.format(name))
    sleep(3)  # 技术精湛的技师一般3秒弄一个
    if not queue.full():
        queue.put('{}:sausage'.format(name))
    else:
        print('{}：哎呀，没卖出去，我自己吃了吧！！！--{}'.format(name, queue.qsize()))


def buySausage(queue, name):
    print('{}:看有好吃的去买个！！1'.format(name))
    sleep(2)
    if not queue.empty():
        print('{}:{}，好吃的'.format(name, queue.get()))
    else:
        print('{}:哎呀，没了吗？？-{}'.format(name, queue.qsize()))


def main():

    pool = Pool(processes=10)
    manager = Manager()
    q = manager.Queue(3)
    for i in range(4):
        pool.apply_async(makeSausage, (q, '技师{:03}'.format(i)))

    print('优雅的分割线'.center(60, '-'))

    for i in range(6):
        pool.apply_async(buySausage(q, '顾客{:03}'.format(i)))

    pool.close()
    pool.join()
    print('end')

if __name__ == '__main__':
    main()
