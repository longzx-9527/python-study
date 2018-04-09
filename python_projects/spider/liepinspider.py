# -*- coding: utf-8 -*-
# @Author: longzx
# @Date: 2018-03-07 19:43:23
"""
爬取猎聘网关于python职位信息
熟悉requests和bs4基本用法
存储数据方面使用了CVS和json/pickle数据存储
"""
from time import time, ctime, sleep
from bs4 import BeautifulSoup
import re
import csv, json, pickle
from spider_tools import get_one_page, logger

#用于记录下载记录数
COUNT = 0


def parse_one_page(html):
    # 解析具体网页，获取想要的内容
    job_lst = []
    soup = BeautifulSoup(html, 'lxml')
    sojob = soup.find('div', 'sojob-result ')
    # 获取下一页地址
    next_url = sojob.find('span', 'ellipsis').next_sibling['href']
    # 获取招聘列表
    job_li = sojob.find_all('li')
    for item in job_li:
        # 发现有很多标签没有值,就会报异常退出程序，对没有值标签做下处理
        try:
            company_name = item.find('p', 'company-name').a.text
        except Exception as _e:
            company_name = "None"

        try:
            company_type = item.find('a', 'industry-link').text
        except Exception as _e:
            company_type = "None"

        try:
            job_name = item.find('div', 'job-info').h3.text.strip()
        except Exception as _e:
            job_name = "None"

        try:
            job_url = item.find('div', 'job-info').h3.a['href']
        except Exception as _e:
            job_url = "None"

        try:
            job_salary = item.find('span', 'text-warning').text
        except Exception as _e:
            job_salary = "None"

        try:
            job_area = item.find('a', 'area').text
        except Exception as _e:
            job_area = "None"

        try:
            job_edu = item.find('span', 'edu').text
        except Exception as _e:
            job_edu = "None"

        try:
            job_year = item.find('span', 'edu').next_sibling.next_sibling.text
        except Exception as _e:
            job_year = "None"

        job_lst.append({
            "公司名称": company_name,
            "公司类型": company_type,
            "招聘职位": job_name,
            "工作薪水": job_salary,
            "工作地址": job_area,
            "教育情况": job_edu,
            "工作年限": job_year,
            "招聘地址": job_url
        })
    return job_lst, next_url


def save_down(url, writer=None, mode=None):
    """使用不同的方式存储数据
    mode='csv'/'json'/'db'
    """
    global COUNT
    html = get_one_page(url)
    items, next_url = parse_one_page(html)

    if 'csv' == mode:
        writer.writerows(items)
    elif 'json' == mode:
        json_item = json.dumps(items, ensure_ascii=False) + '\n'
        writer.write(json_item)
    elif 'pickle' == mode:
        pickle.dump(items, writer)
    elif 'db' == mode:
        pass
    else:
        raise Exception('wrong mode,you should input cvs or json or db')

    COUNT += len(items)

    new_url = 'https://www.liepin.com' + next_url
    return new_url


@logger
def main(url_in, end=10, filename='test', mode='csv', fieldnames=None):
    if mode == 'db':
        writer = None
    elif mode == 'pickle':
        fp = open(filename + '.' + mode, 'wb')
        writer = fp
    elif 'csv' == mode:
        fp = open(filename + '.' + mode, 'w', newline="", encoding='utf-8')
        if fieldnames is None:
            print('fieldnames must input')
            raise Exception('fieldnames must input')
        writer = csv.DictWriter(fp, fieldnames=fieldnames)
        writer.writeheader()
    elif 'json' == mode:
        fp = open(filename + '.' + mode, 'w')
        writer = fp

    next_url = None
    for i in range(1, end):
        if i == 1:
            url = url_in
        print('第 {} 页地址：{}'.format(i, url))
        next_url = save_down(url, writer=writer, mode=mode)
        url = next_url
    fp.close()
    print('共计下载：{} 条'.format(COUNT))


if __name__ == '__main__':
    url = 'https://www.liepin.com/zhaopin/?pubTime=&ckid=c90ed7b8c9bcfdab&fromSearchBtn=2&compkind=&isAnalysis=&init=-1&searchType=1&dqs=&industryType=&jobKind=&sortFlag=15&degradeFlag=0&industries=&salary=&compscale=&clean_condition=&key=python&headckid=c90ed7b8c9bcfdab&d_pageSize=40&siTag=I-7rQ0e90mv8a37po7dV3Q~fA9rXquZc5IkJpXC-Ycixw&d_headId=0f913b2c0df0cc182eb9e837caeb5fb8&d_ckId=0f913b2c0df0cc182eb9e837caeb5fb8&d_sfrom=search_prime&d_curPage=2&curPage=0'
    fieldnames = [
        '公司名称', '公司类型', '招聘职位', '工作薪水', '工作地址', '教育情况', '工作年限', '招聘地址'
    ]
    main(url, end=3, filename='liepin', mode='pickle', fieldnames=fieldnames)
