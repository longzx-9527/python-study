# -*- coding: utf-8 -*-
# @Author: longzx
# @Date: 2018-02-06 11:07:55
"""
requests:
1.获取请求
2.解析页面
3.下载存储页面
具体项目：
爬取博客园首页：
url = 'https://www.cnblogs.com/'
获取以下信息：
1.发布人
2.发布标题
3.发布内容
4.发布时间
5.阅读数
6.评论数
7.文章具体地址

"""
from time import time, ctime
import re
import csv
from spider_tools import logger, get_one_page

COUNT = 0


def parse_one_page(html):
    pattern = re.compile(
        r'titlelnk.*?href="(.*?)".*?"_blank">(.*?)</a>.*?alt=""/>' +
        r'</a>(.*?)</p>.*?class="lightblue">(.*?)</a>.*?发布于(.*?)<span ' +
        r'.*?class="gray">.*?评论\((.*?)\)</a>.*?class="gray">阅读\((.*?)\)</a>',
        re.S)

    items = re.findall(pattern, html)
    for item in items:
        yield {
            "发布人": item[3].strip(),
            "发布标题": item[1].strip(),
            "发布内容": item[2].strip(),
            "发布时间": item[4].strip(),
            "阅读数": item[6],
            "评论数": item[5],
            "具体文章地址": item[0].strip()
        }


def save_down(url, writer):
    global COUNT
    html = get_one_page(url)
    for item in parse_one_page(html):
        writer.writerow(item)
        COUNT += 1
    print('{} success spirder'.format(url))


@logger
def main(start, end, filepath='tmp.csv'):
    fp = open(filepath, 'w', newline="", encoding='utf-8')
    fieldnames = ['发布人', '发布标题', '发布内容', '发布时间', '阅读数', '评论数', '具体文章地址']
    writer = csv.DictWriter(fp, fieldnames=fieldnames)
    writer.writeheader()
    for i in range(start, end):
        url = 'https://www.cnblogs.com/sitehome/p/' + str(i)
        save_down(url, writer)
    fp.close()
    print('共计下载：{} 条'.format(COUNT))


if __name__ == '__main__':
    start = 1
    end = 10
    main(start, end)
