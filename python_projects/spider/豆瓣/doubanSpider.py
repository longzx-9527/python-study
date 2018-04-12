# -*- coding: utf-8 -*-
# @Author: longzx
# @Date: 2018-03-21 22:52:22
import csv
import json
import os
from collections import defaultdict

import pymysql
from bs4 import BeautifulSoup
from config import (BASE_PATH, LOG_FILE, LOG_STAT, MOVIE_LIMIT,
                    MOVIES_TYPE_FILE, baseurl, main_url, top_list_type)
from spider_tools import get_one_page, logger_deco
from mylogger import logger


def get_movies_type(html):
    # 获取电影分类
    soup = BeautifulSoup(html, 'lxml')
    typelst = soup.find('div', 'types').find_all('span')
    typelist = list()

    for x in typelst:
        typename = x.a.text
        typeurl = x.a.get('href').split('&', 1)[1]
        typelist.append((typename, typeurl))
    return typelist


@logger_deco
def save_type_csv(filename, data):
    # 保存电影分类
    with open(filename, 'w', newline="", encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerows(data)


@logger_deco
def get_type_csv(filename):
    # 获取电影分类类表
    lst = []
    with open(filename, 'r', newline="", encoding='utf-8') as f:
        reader = csv.reader(f)
        lst = list(reader)
    return lst


@logger_deco
def save_movie_info(filename, data):
    # 保存电影信息
    if os.path.isfile(filename):
        flag = False
    else:
        flag = True
    with open(filename, 'a+', newline="", encoding='utf-8') as f:
        fieldnames = ['电影排名', '电影名称', '演员列表', '年代', '类型', '评分', '评论人数', '海报图片']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if flag:
            writer.writeheader()
        writer.writerows(data)


def get_movie_count(url):
    # 获取当前种类电影个数
    html = get_one_page(url)
    type_list_count = json.loads(html)
    return type_list_count.get('total', 0)


@logger_deco
def get_movie_list(url, filename):
    # 获取并保存电影详细列表
    html = get_one_page(url)
    movie_data = json.loads(html)
    movie_list = []
    for movie_info in movie_data:
        movie_dict = {}
        movie_dict['电影排名'] = movie_info.get('rank')
        movie_dict['电影名称'] = movie_info.get('title')
        movie_dict['演员列表'] = ','.join(movie_info.get('actors'))
        movie_dict['年代'] = movie_info.get('release_date')
        movie_dict['类型'] = ','.join(movie_info.get('types'))
        movie_dict['评分'] = movie_info.get('rating')[0]
        movie_dict['评论人数'] = movie_info.get('vote_count')
        movie_dict['海报图片'] = movie_info.get('cover_url').replace('\\', '')
        movie_list.append(movie_dict)

    save_movie_info(filename, movie_list)


@logger_deco
def get_movie_type_list():
    # 获取电影分类列表
    if not os.path.exists(MOVIES_TYPE_FILE) or os.path.getsize(
            MOVIES_TYPE_FILE) == 0:
        html = get_one_page(main_url)
        type_list = get_movies_type(html)
        save_type_csv(MOVIES_TYPE_FILE, type_list)
    else:
        type_list = get_type_csv(MOVIES_TYPE_FILE)
    return type_list


@logger_deco
def down_type_movies(path, url):
    # 获取当前电影种类电影个数
    count_url = baseurl + top_list_type[0] + url
    movie_count = get_movie_count(count_url)
    if movie_count == 0:
        logger.debug('当前类型没有电影！！！')
        return
    else:
        start = 0
        while start < movie_count:
            movies_url = baseurl + top_list_type[1] + url + "&start={}&limit={}".format(
                start, MOVIE_LIMIT)
            get_movie_list(movies_url, path)
            start += MOVIE_LIMIT


@logger_deco
def down_movie(movetype="all"):
    type_list = get_movie_type_list()

    if type == "all":
        # 1.获取电影分类类表
        for movie_type, movies_url in type_list:
            filepath = os.path.join(BASE_PATH, movie_type + ".csv")
            down_type_movies(filepath, movies_url)
    else:
        filepath = os.path.join(BASE_PATH, movetype + ".csv")
        movies_url = dict(type_list).get(movetype)
        down_type_movies(filepath, movies_url)


@logger_deco
def main():
    logger.debug('下载喜剧部分电影')
    down_movie("喜剧")


if __name__ == '__main__':
    main()
