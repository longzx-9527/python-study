#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-03-31 08:11:32
# @Author  : Longzx (longzongxing@163.com)
# @Link    : http://www.cnblogs.com/lonelyhiker/
# @Version : $Id$


from time import time, sleep, ctime
from multiprocessing import Process, Pool
from threading import Thread

"""
thread线程，能使用多线程也能使用多进程
一般只有几个进程的话使用process
如果有很多进程的话pool进程池进行管理

"""


def fun1(name):
    print('hello {},welcome to beijing!!'.format(name))
    i = 0
    while i < 5:
        print('while {},welcome to beijing!!'.format(name))
        sleep(1)
        i += 1

    print('see you later {} , good lock!!'.format(name))


class MyProcess(Process):

    def __init__(self, target=None, name=None):
        super().__init__()
        self.target = target
        self.name = name

    def run(self):
        self.target(self.name)


def printfun(fun, *args):
    print('{} begin at {}'.format(fun.__name__, ctime()))
    starttm = time()
    fun(*args)
    print('{} end at {}'.format(fun.__name__, ctime()))
    print('{}总共用时:{}'.format(fun.__name__, time() - starttm))


def forfun(n):
    for i in range(n):
        printfun(fun1, 'jack_{}'.format(i))


def threadfun(n):
    """多线程测试

        1.创建多线程 1.直接Thread 2.继承Thread类
    """
    threads = []

    for i in range(n):
        t = Thread(target=fun1, args=('thread_{}'.format(i),))
        # t.daemon = True
        threads.append(t)

    print('start thread')
    for i in range(n):
        threads[i].start()

    for i in range(n):
        threads[i].join()
    print('threadfun end')


def processTest1(n):
    """创建多进程
        1.使用Process 2.继承Process
    """
    pcs = []

    for i in range(n):
        p = Process(target=fun1, args=('沉睡的小五郎_{:02}'.format(i),))
        pcs.append(p)

    for i in range(n):
        pcs[i].start()

    for i in range(n):
        pcs[i].join()


def processTest2(n):
    # 使用process继承的类来创建多进程

    pcs = []

    for i in range(n):
        p = MyProcess(target=fun1, name='柯南_{:02}'.format(i))
        pcs.append(p)

    for i in range(n):
        pcs[i].start()

    for i in range(n):
        pcs[i].join()


def poolTest(n):
    """
    进程池：
    1.获取进程池对象实例，初始化池子大小
    2.使用apply apply_async() map map_async()
    """
    pool = Pool(processes=n)
    choice = 'map'
    if 'map' == choice:
        print('begein', choice)
        lst = ['超人_{:02}'.format(i) for i in range(n)]
        pool.map(fun1, lst)
        # pool.map_async(fun1, lst)
    elif 'apply' == choice:
        for i in range(n):
            # 阻塞完成所有操作，就像forfun一样,这种方式设置池子大小没啥意思
            pool.apply(func=fun1, args=('小龙人_{:02}'.format(i),))
            # 非阻塞
            # pool.apply_async(fun1, args=('小黄人_{:02}'.format(i),))

    print('--------close pool-----------')
    # 关闭池子入口，不让更多对象进入
    pool.close()
    # 等待所有进程执行完毕退出
    pool.join()
    print('--------end pool-----------')


if __name__ == '__main__':
    n = 2
    # printfun(forfun, n)
    # printfun(threadfun, n)
    # printfun(processTest2, n)
    printfun(poolTest, n)
    print('main end')
