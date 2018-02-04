# -*- coding: utf-8 -*-
"""
Created on Wed Jan 31 15:30:20 2018

@author: longz
"""
import urllib.request
import re

class QSBK:
    
    #初始化
    def __init__(self,url,headers,start=1,count=10):
        self.url = url
        self.headers = headers
        #抓取 作者 性别  年龄 笑点数 评论数 内容
        self.p = r'.*?<h2>(.*?)</h2>.*?articleGender (\w+)">(\d+)</div>.*?(?<=<span>)(.*?)(?=</span>).*?stats-vote.*?(\d+).*?number.*?(\d+)'
        self.pattern = re.compile(self.p,re.S)
        self.filename='qsbk.txt'
        self.count = 0
        
    #获取网页内容
    def getHtml(self):
        try:
            request = urllib.request.Request(url=self.url,headers=self.headers)
            response = urllib.request.urlopen(request)
        except urllib.error.URLError as e:
            print(e.reason)
            
        html = response.read().decode('utf-8')       
        return html
    
    #解析网页内容
    def getText(self,content):
        
        items = re.findall(self.pattern,content)
        
        return items
    
    #保存获取信息
    def saveText(self,items):
        self.count = 0
        fp = open(self.filename,'w')
        
        for item in items:
            name = item[0]
            age = item[2]
            ixl = item[4]
            ipl = item[5]
            text = item[3]
            
            if 'man' in item[1]:    
                sex = '男'
            elif 'women' in item[1]:
                sex = '女'
                
            fp.write('作者:'+name+'\n')
            fp.write('性别:'+sex+'\n')
            fp.write('年龄:'+age+'\n')
            fp.write('笑脸:'+ixl+'\n')
            fp.write('评论:'+ipl+'\n')
            fp.write('笑话内容:'+text+'\n')
            self.count += 1
            
        fp.close()
        
    #启动抓取程序
    def start(self):
        
        i = 1
        
        while i <= 3 :
            self.url = self.url + str(i) +'/'
            print('抓取第 %d 页记录 ' % (i))
            html = self.getHtml()
            
            item = self.getText(html)
    
            self.saveText(item)
            print('第 %d 页记录,抓取完毕!!!\n共计 %d 条记录 ' % (i,self.count))
            i += 1

            
def main():
    url = 'https://www.qiushibaike.com/8hr/page/'
    headers = {'User-Agent': 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'}
    
    qsbk = QSBK(url,headers)
    qsbk.start()
 
if __name__ =='__main__':

    main()