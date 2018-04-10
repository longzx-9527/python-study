#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-04-02 09:49:51
# @Author  : Longzx (longzongxing@163.com)
# @Link    : http://www.cnblogs.com/lonelyhiker/
# @Version : $Id$

import os
import socket
import tools
from threading import Thread
from concurrent.futures import ThreadPoolExecutor


BUFFSIZE = 1024


class ServerSocket(Thread):
    """socket服务端
        监听客户端请求，默认tcp连接
        flag:是否开启多线程 True:开启
        listen:监听数默认5
    """

    def __init__(self, addr=(), tcp=True, flag=True, listen=5):
        super().__init__(name='server')
        self.tcp = tcp
        if self.tcp:
            self._server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        else:
            self._server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.addr = addr
        self.flag = flag
        self.listen = listen
        if self.flag:
            self._executor = ThreadPoolExecutor(max_workers=5)

    def _tosend(self, conn, addr):
        # 对接客户端并发送文件
        path = conn.recv(BUFFSIZE).decode('utf-8')
        tools.sendfiles(path, conn)
        conn.close()

    def _sendctl(self, conn, addr):
        # 判断是否启动多线程
        if self.flag:
            self._executor.submit(self._tosend, conn, addr)
        else:
            self._tosend(conn, addr)

    def run(self):
        if self.tcp:
            self._server.bind(self.addr)
            self._server.listen(self.listen)
            print('server begin')
            i = 0
            while i < 2:

                conn, addr = self._server.accept()
                self._sendctl(conn, addr)
                i += 1

            self._server.close()
            print('end server')
