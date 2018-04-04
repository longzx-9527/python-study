#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-04-02 09:50:33
# @Author  : Longzx (longzongxing@163.com)
# @Link    : http://www.cnblogs.com/lonelyhiker/
# @Version : $Id$

import os
import server
import client
from threading import Thread
from functools import wraps
from time import ctime, time
PORT = 9999
addr = ('', PORT)


def logger(fun):
    @wraps(fun)
    def wrapers(*args, **kwargs):
        print('{} begin  at {}--------------->'.format(fun.__name__, ctime()))
        sttime = time()
        fun(*args, **kwargs)
        print('{} end  at {}--------------->'.format(fun.__name__, ctime()))
        print('{} total time:{}'.format(fun.__name__, time() - sttime))

    return wrapers


@logger
def main():

    s = server.ServerSocket(addr=addr, flag=False)
    s.start()
    print('begin11 ----------------------')

    c1 = client.ClientSocket('/home/longzx/tmp', addr=addr)
    c2 = client.ClientSocket('/home/longzx/tmp1', addr=addr)

    print('begin ----------------------')
    c1.start()
    c2.start()

    s.join()
    c1.join()
    c2.join()

    print('end -------------------------')

if __name__ == '__main__':
    main()
