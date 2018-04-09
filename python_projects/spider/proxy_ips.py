# -*- coding: utf-8 -*-
# @Author: longzx
# @Date: 2018-02-08 14:53:47
"""
获取代理ip
"""
import csv
from bs4 import BeautifulSoup
from spider_tools import logger, get_one_page


def parse_one_page(html):
    ips = []
    soup = BeautifulSoup(html, 'lxml')
    ip_list = soup.find_all('tr')
    for ip_tr in ip_list:
        try:
            ip = ip_tr.find_all('td')[1].text
        except Exception:
            continue
        try:
            port = ip_tr.find_all('td')[2].text
        except Exception:
            continue
        try:
            ip_type = ip_tr.find_all('td')[5].text
        except Exception:
            continue
        ips.append({'ip': ip, 'port': port, 'ip_type': ip_type})
    return ips


@logger
def main(end):
    cnt = 0
    url = 'http://www.xicidaili.com/nn/'
    with open('ip.csv', 'w', encoding='utf-8', newline="") as f:
        fieldnames = ['ip', 'port', 'ip_type']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for i in range(2, end):
            html = get_one_page(url)
            items = parse_one_page(html)
            writer.writerows(items)
            url = url + str(i)
            cnt += len(items)
            print('正在下载{}条记录'.format(i))
        print('一共下载{}记录'.format(cnt))


if __name__ == '__main__':
    main(5)
