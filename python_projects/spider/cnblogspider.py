# -*- coding: utf-8 -*-
# @Author: longzx
# @Date: 2018-04-07 09:43:23
"""
使用bs4

"""
from time import time, ctime
from functools import wraps
import requests
from requests.exceptions import RequestException
from bs4 import BeautifulSoup
import re
import csv

COUNT = 0


def logger(fun):
    @wraps(fun)
    def wrapper(*args, **kwargs):
        print('-------------{} begin at {}-------'.format(
            fun.__name__, ctime()))
        starttm = time()
        ret = fun(*args, **kwargs)
        endtm = time()
        print('-------------end at {}-------------'.format(ctime()))
        print('-------------{} total time:{}------'.format(
            fun.__name__, endtm - starttm))
        return ret

    return wrapper


def get_one_page(url):
    try:
        r = requests.get(url)
    except RequestException as r:
        print(r)
    else:
        if r.status_code == 200:
            return r.text
        else:
            return None


def parse_one_page(html):
    soup = BeautifulSoup(html, 'html5lib')
    post_list = soup.find(id='post_list')
    post_item = post_list.find_all('div', class_='post_item')
    for item in post_item:
        post_foot = item.find(
            'div', class_='post_item_foot').text.strip().split()
        ydpl = re.compile(r'.*?(\d+){1}').findall(post_foot[-1])

        yield {
            "发布人": post_foot[0],
            "发布标题": item.find('a', class_='titlelnk').text.strip(),
            "发布内容": item.find('p', class_='post_item_summary').text.strip(),
            "发布时间": post_foot[2],
            "阅读数": ydpl[0],
            "评论数": ydpl[1],
            "具体文章地址": item.find('a', class_='titlelnk')['href']
        }

@logger
def main(url, writer):
    global COUNT
    html = get_one_page(url)
    for item in parse_one_page(html):
        writer.writerow(item)
        COUNT += 1
    print('{} bs4 success spirder'.format(url))


@logger
def main1():
    fp = open('bky1.csv', 'w', newline="", encoding='utf-8')
    fieldnames = ['发布人', '发布标题', '发布内容', '发布时间', '阅读数', '评论数', '具体文章地址']
    writer = csv.DictWriter(fp, fieldnames=fieldnames)
    writer.writeheader()
    for i in range(1, 20):
        url = 'https://www.cnblogs.com/sitehome/p/' + str(i)
        main(url, writer)
    fp.close()
    print('共计下载：{} 条'.format(COUNT))


if __name__ == '__main__':
    main1()
