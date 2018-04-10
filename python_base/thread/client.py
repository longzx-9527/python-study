#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-04-02 09:50:21
# @Author  : Longzx (longzongxing@163.com)
# @Link    : http://www.cnblogs.com/lonelyhiker/
# @Version : $Id$

import os
import socket
import json
from threading import Thread
BUFFESIZE = 1024
from time import time, ctime, sleep


class ClientSocket(Thread):

    def __init__(self, path, addr=(), tcp=True):
        super().__init__(name='clint')
        self.tcp = tcp
        if self.tcp:
            self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        else:
            self._socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.addr = addr
        self.path = path

    def _connect(self):
        self._socket.connect(self.addr)

    def run(self):
        # 建立连接
        self._connect()
        self._socket.send(self.path.encode('utf-8'))
        print('send success')
        while True:
            transheadJson = self._socket.recv(BUFFESIZE).decode('utf-8')
            if not transheadJson:
                break

            transhead = json.loads(transheadJson)
            print('transhead = {}'.format(transhead))
            filename = transhead['filename']
            filepath = transhead['filepath']
            filetype = transhead['filetype']
            filesize = transhead['filesize']

            self._socket.send(b'recv transhead')

            path = os.path.join(filepath, 'tmp', filename)
            with open(path, 'wb') as fp:
                bytes_recd = 0
                print('client {} begin  at {}--------------->'.format(filepath, ctime()))
                starttm = time()
                while bytes_recd < filesize:
                    data = self._socket.recv(
                        min(filesize - bytes_recd, BUFFESIZE))
                    if data == b'':
                        raise RuntimeError('socket connection broke')
                    fp.write(data)
                    bytes_recd += len(data)
                    sleep(0.1)
                print('client {} end  at {}--------------->'.format(filepath, ctime()))
                print('client {} total time:{}'.format(
                    filepath, time() - starttm))
            self._socket.send(b'recv file success')
        self._socket.close()
