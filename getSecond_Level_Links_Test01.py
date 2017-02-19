#!/usr/bin/env Python
# coding=utf-8
from urllib.request import urlopen
from bs4 import BeautifulSoup
#拿到第一个一级页面URL
firstUrl ="http://tieba.baidu.com/f?kw=%E8%BE%BD%E5%AE%81%E5%B7%A5%E7%A8%8B%E6%8A%80%E6%9C%AF%E5%A4%A7%E5%AD%A6&ie=utf-8"
i=0
count = 0
while(count<2):
    pageNum = str(count*50)
     #生成一级页面URL
     #http://tieba.baidu.com/f?kw=%E8%BE%BD%E5%AE%81%E5%B7%A5%E7%A8%8B%E6%8A%80%E6%9C%AF%E5%A4%A7%E5%AD%A6&ie=utf-8&pn=50
    First_Level_Url = firstUrl + "&pn="+pageNum
    print(First_Level_Url)
    count+=1
    i+=1
    html = urlopen(First_Level_Url)
    bsObj = BeautifulSoup(html,"html5lib")
    #获取当前页面二级链接,并保存
    for link in bsObj.findAll("a",{"class":"j_th_tit"}):
         if 'href' in link.attrs:
            print(link.attrs['href'])
