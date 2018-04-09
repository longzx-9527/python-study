# -*- coding: utf-8 -*-
# @Author: longzx
# @Date: 2018-02-08 18:43:10

import csv
from bs4 import BeautifulSoup
from spider_tools import get_one_page

url = 'http://ip.chinaz.com/'

ip_lst = []

p = {'http': 'http://223.167.134.164:8080'}


def ip_check(url, proxies):
    html = get_one_page(url, proxies)
    if html:
        soup = BeautifulSoup(html, 'lxml')
        try:
            parent_node = soup.find(class_="IpMRig-tit")
            for i in parent_node.find_all('dd'):
                print(i.get_text())
        except Exception as _e:
            return False
    else:
        return False


with open('ip.csv', newline="", encoding='utf-8') as f:
    reader = csv.reader(f)
    for row in reader:

        proxy_host = "http://" + row[0] + ":" + row[1]
        proxy_temp = {"http": proxy_host}
        ip_check(url, proxy_temp)
