from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
"""
    标签所在URL：
        http://tieba.baidu.com/f?kw=%E8%BE%BD%E5%AE%81%E5%B7%A5%E7%A8%8B%E6%8A%80%E6%9C%AF%E5%A4%A7%E5%AD%A6&ie=utf-8
    标签定位：
        <a class="last pagination-item " href="http://tieba.baidu.com/f?kw=%E8%BE%BD%E5%AE%81%E5%B7%A5%E7%A8%8B%E6%8A%80%E6%9C%AF%E5%A4%A7%E5%AD%A6&ie=utf-8&pn=266000">尾页</a>
    获取内容：
        266000
"""
firstUrl = "http://tieba.baidu.com/f?kw=%E8%BE%BD%E5%AE%81%E5%B7%A5%E7%A8%8B%E6%8A%80%E6%9C%AF%E5%A4%A7%E5%AD%A6&ie=utf-8"
html = urlopen(firstUrl)
bsObj = BeautifulSoup(html,"html5lib")
for link in bsObj.findAll("a",{"class":"last pagination-item "}):
    if 'href' in link.attrs:
        #http://tieba.baidu.com/f?kw=%E8%BE%BD%E5%AE%81%E5%B7%A5%E7%A8%8B%E6%8A%80%E6%9C%AF%E5%A4%A7%E5%AD%A6&ie=utf-8&pn=266000
        lastPageUrl = link.attrs['href']
        #需求：lastPageNum = lastPageUrl[113:]
        #正则？截取 &pn= 后面的内容
        targets = re.findall("[0-9]{2,12}",lastPageUrl)
        for target in targets:
            lastPageNum = int(target)
        print(lastPageNum) #266000
