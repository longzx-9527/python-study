#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2018-04-02 09:50:46
# @Author  : Longzx (longzongxing@163.com)
# @Link    : http://www.cnblogs.com/lonelyhiker/
# @Version : $Id$

import os
import json
from time import time, ctime, sleep
from functools import wraps
from concurrent.futures import ThreadPoolExecutor


transhead = {
    'filename': None,
    'filepath': None,
    'filesize': 0,
    'filetype': None,
    'charset': 'utf-8'
}


def logger(fun):
    @wraps(fun)
    def wrapers(*args, **kwargs):
        print('{} begin  at {}--------------->'.format(fun.__name__, ctime()))
        sttime = time()
        fun(*args, **kwargs)
        print('{} end  at {}--------------->'.format(fun.__name__, ctime()))
        print('{} total time:{}'.format(fun.__name__, time() - sttime))

    return wrapers


def getfile(path):
    # 返回给定路径下所有的文件
    if not os.path.exists(path):
        print('{} is not exists'.format(path))
        raise ValueError

    if not os.path.isdir(path):
        print('{} is not a dir'.format(path))
        raise ValueError

    dirs = os.listdir(path)
    dirlist = []
    for x in dirs:
        filepath = os.path.join(path, x)
        if os.path.isfile(filepath):
            dirlist.append(filepath)
        else:
            print('{} is not a file'.format(filepath))
            continue
    return dirlist


def sendfiles(path, conn):
    files = getfile(path)
    for filepath in files:
        sendfilehead(filepath, conn)
        msg = conn.recv(1024)
        print('msg = {}'.format(msg))

        print('{} begin  at {}--------------->'.format(filepath, ctime()))
        starttm = time()
        sendfile(filepath, conn)
        print('{} end  at {}--------------->'.format(filepath, ctime()))
        print('{} total time:{}'.format(filepath, time() - starttm))
        msg = conn.recv(1024)
        print('recv msg = {}'.format(msg))
    print('file all send')


def sendfilepath(filepath, conn):
    sendfilehead(filepath, conn)
    msg = conn.recv(1024)
    print('msg = {}'.format(msg))
    starttm = time()
    sendfile(filepath, conn)
    msg = conn.recv(1024)
    print('recv msg = {}'.format(msg))


def sendfilehead(path, conn):
    th = set_transhead(path)
    thJson = json.dumps(th)
    print('thjson = {}'.format(thJson))
    conn.send(thJson.encode('utf-8'))
    print('sendfilehead success')


def sendfile(path, conn):
    # 发送文件
    with open(path, 'rb') as fin:
        data = fin.read()
        totalsend = 0
        dlen = len(data)
        while totalsend < dlen:
            send = conn.send(data[totalsend:])
            if send == 0:
                raise RuntimeError('client connection broken')
            print('send = {}'.format(send))
            totalsend += send
        print('sendfile success')


def set_transhead(path):
    # 设置传输文件头部信息
    filesize = os.path.getsize(path)
    filename = os.path.basename(path)
    filepath = os.path.dirname(path)
    filetype = filename.split('.')[1]
    transhead['filename'] = filename
    transhead['filepath'] = filepath
    transhead['filesize'] = filesize
    transhead['filetype'] = filetype
    print('文件头信息:{}'.format(transhead))
    return transhead
