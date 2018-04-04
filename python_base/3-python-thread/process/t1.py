#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-03-30 10:22:54
# @Author  : Longzx (longzongxing@163.com)
# @Link    : http://www.cnblogs.com/lonelyhiker/
# @Version : $Id$

"""
1.利用multiprocessing.Process对象可以创建一个进程，该Process对象与Thread对象的用法相同，
也有start(), run(), join()等方法。Process类适合简单的进程创建，
2.如需资源共享可以结合multiprocessing.Queue使用；
3.如果想要控制进程数量，则建议使用进程池Pool类。

Process类主要的进程管理类,主要用于创建一个简单的进程
1.构造方法
Process(target,name,*args,*kwargs)
target:要执行的方法
name：进程名字
args/kwargs:传入的参数
2.常用属性和方法
is_alive() : 返回进程是否存在
run(): 运行进程
join():阻塞当前进程，直到进程结束
start():进程准备就绪，等待CPU调度
pid
daemon 守护进程不允许创建子进程
terminate()：不管任务是否完成，立即终止进程

创建一个多进程方法：
1.定义函数，传入给process
2.继承process类，重写run()
"""

from multiprocessing import Process, current_process
from time import time, sleep, ctime


class MyProcess(Process):
    num = 3

    def __init__(self, sec=None, n=0):
        Process.__init__(self)
        self.sec = sec
        self.n = n

    def run(self):
        MyProcess.num = self.n
        print('begin 当前正在执行的进程是: {}sleep:{}  num={}'.format(
            current_process(), self.sec, MyProcess.num))
        sleep(self.sec)
        print('end 当前正在执行的进程是: {}  sleep:{}  num={}'.format(
            current_process(),  self.sec, MyProcess.num))

num = 4


def fun(name, sec, n):
    global num
    num = n
    print('begin 当前正在执行的进程是: {} name={} sleep:{}  num={}'.format(
        current_process(), name, sec, num))

    sleep(sec)
    print('end 当前正在执行的进程是: {} name={} sleep:{}  num={}'.format(
        current_process(), name, sec, num))


def main1():
    pcs = []
    names = ['tom', 'jack', 'pet']
    secs = [3, 2, 5]
    nums = [8, 7, 5]

    # 创建进程
    for i in range(3):
        p = Process(target=fun, args=(names[i], secs[i], nums[i]))
        pcs.append(p)

    # 启动进程
    for i in range(3):
        pcs[i].start()

    # 设置等所有进程执行完毕退出
    for i in range(3):
        pcs[i].join()


def main2():
    pcs = []
    names = ['tom', 'jack', 'pet']
    secs = [3, 2, 5]
    nums = [8, 7, 5]

    # 创建进程
    for i in range(3):
        p = MyProcess(sec=secs[i], n=nums[i])
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
    print()
    print('main2 begin at {}'.format(ctime()))
    starttm = time()
    main2()
    print('main2 end at {}'.format(ctime()))
    print('总共用时:{}'.format(time() - starttm))
