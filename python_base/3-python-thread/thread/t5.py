#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-03-31 15:27:55
# @Author  : Longzx (longzongxing@163.com)
# @Link    : http://www.cnblogs.com/lonelyhiker/
# @Version : $Id$

"""主要是生产者和消费者线程实现
   1.生产者生产数据放入队列中
   2.消费者取出数据
"""

from threading import Thread
from queue import Queue
from time import sleep


# 生产者
class Producer(Thread):

    def __init__(self, name, queue, count):
        super().__init__(name=name)
        self.queue = queue
        self.count = count

    def run(self):
        print('生产者 {} 要生产特斯拉！！！'.format(self.getName()))
        for i in range(self.count):
            s = '特斯拉_{:02}号'.format(i)
            print('{} 成品'.format(s))
            sleep(2)
            if self.queue.full():  # 这个判断也是不准的，为啥
                print('sorry,厂库已满，没法在放了，等会再来吧')
            else:
                print('{} 已生成，放入厂库'.format(s))
                self.queue.put(s)

        print('{} 完成生产任务！'.format(self.getName()))


# 消费者
class Customer(Thread):

    def __init__(self, name, queue, count):
        super().__init__(name=name)
        self.queue = queue
        self.count = count

    def run(self):
        print('消费者 {} 前来购物！！'.format(self.getName()))
        for i in range(self.count):
            if self.queue.empty():
                print('sorry,库存已空,等会再来看吧！！！')
            else:
                s = self.queue.get()
                print('我购买到了，{}'.format(s))
            sleep(2)

        print('{} 购物完成，很快乐！！！'.format(self.getName()))


def main():
    queue = Queue(5)

    names = ['富士康', '盖茨']

    threads = []

    t1 = Producer(names[0], queue, 8)

    t2 = Customer(names[1], queue, 8)

    threads.append(t1)
    # threads.append(t2)

    for i in range(1):
        threads[i].start()

    for i in range(1):
        threads[i].join()


if __name__ == '__main__':
    main()
