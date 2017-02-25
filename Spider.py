#!/usr/bin/python
# -*- coding: UTF-8 -*-
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
def main():
    # firstUrlStr = input("请输入贴吧名，如“辽宁工程技术大学吧”：")
    # firstUrl = getFirstUrl(firstUrlStr)
    firstUrl = "http://tieba.baidu.com/f?kw=%E8%BE%BD%E5%AE%81%E5%B7%A5%E7%A8%8B%E6%8A%80%E6%9C%AF%E5%A4%A7%E5%AD%A6&ie=utf-8"
    outputStr = input("请输入采集结果输出路径：")
    print("输出路径为"+outputStr)
    output_file_name = outputStr+'/result.txt'
    file = open(output_file_name,'a')
    print("创建文件")
    lastPageNum = getLastPageNum(firstUrl)
    secondLinks = getSecond_Level_Links(firstUrl,lastPageNum)
    for secondLink in secondLinks:
        allSecondLInks = getAllSecondLInks(secondLink)
        for secondlink in allSecondLInks:
            content = getSecondLevel_PagesContent(secondlink)
            littleInfos = getTargetInfo(content)
            #写出数据
            for info in littleInfos:
                file.write(str(secondLink)+'/n')
                file.write(info+'/n')
        print("正在扫描："+secondLink)

    file.closed
def getSecond_Level_Links(firstUrl,lastPageNum):
    '获取指定URL贴吧所有帖子URL'
    secondLinks = set()
    count = 0
    while(count<lastPageNum):
        pageNum = str(count*50)
         #生成一级页面URL
         #http://tieba.baidu.com/f?kw=%E8%BE%BD%E5%AE%81%E5%B7%A5%E7%A8%8B%E6%8A%80%E6%9C%AF%E5%A4%A7%E5%AD%A6&ie=utf-8&pn=50
        First_Level_Url = firstUrl + "&pn="+pageNum
        count+=1

        html = urlopen(First_Level_Url)
        bsObj = BeautifulSoup(html,"html5lib")
        #获取当前页面二级链接,并保存
        for link in bsObj.findAll("a",{"class":"j_th_tit"}):
             if 'href' in link.attrs:
                #将ULR拼接后存入
                secondLink = "http://tieba.baidu.com"+link.attrs['href']
                secondLinks.add(secondLink)
    return secondLinks

def getLastPageNum(firstUrl):
    '获取指定URL贴吧尾页URL中结尾数字'
    html = urlopen(firstUrl)
    bsObj = BeautifulSoup(html,"html5lib")
    lastPageNum = 0
    for link in bsObj.findAll("a",{"class":"last pagination-item "}):
        if 'href' in link.attrs:
            #http://tieba.baidu.com/f?kw=%E8%BE%BD%E5%AE%81%E5%B7%A5%E7%A8%8B%E6%8A%80%E6%9C%AF%E5%A4%A7%E5%AD%A6&ie=utf-8&pn=266000
            lastPageUrl = link.attrs['href']
            #需求：lastPageNum = lastPageUrl[113:]
            #正则？截取 &pn= 后面的内容
            targets = re.findall("[0-9]{2,12}",lastPageUrl)
            for target in targets:
               lastPageNum = int(target)
    print("拿到尾页数字"+str(lastPageNum))
    return lastPageNum

def getAllSecondLInks(secondLink):
    secondLinkBrothers = set()
    secondLinkBrothers.add(secondLink)
    firstSecondHtml = urlopen(secondLink)
    fisrtBsObj = BeautifulSoup(firstSecondHtml,"html5lib")
    #拿到子页面最后一页URL结尾数字
    minNum = 2147483647
    for li in fisrtBsObj.findAll("li",{"class":"l_reply_num"}):
        liContent = li.get_text()
        #正则提取最小数字
        targetNums = re.findall("[0-9]{1,10}",liContent)
        for targetNum in targetNums:
            targetNum = int(targetNum)
            if(targetNum<minNum):
                minNum = targetNum

    lastSonPageNum = minNum
    pn = 2
    for num in range(2,lastSonPageNum+1):
        #拼接二级子链接兄弟链接并保存
        brotherLink = str(secondLink)+"?pn="+ str(pn)
        pn = pn + 1
        secondLinkBrothers.add(brotherLink)
        print("拿到"+brotherLink)

    return secondLinkBrothers
def getSecondLevel_PagesContent(secondlink):
    html = urlopen(secondlink)
    bsObj = BeautifulSoup(html,"html5lib")
    #得到子页面div
    sonDivs = bsObj.findAll("div",{"class":{"l_post j_l_post l_post_bright noborder ","l_post j_l_post l_post_bright "}})
    for sonDiv in sonDivs:
        #将sonDiv重新封装成bsObj(将二级页面子页面重装为一个新的html文档方便降低调用成本)
        sonHtml = "<html><head></head><body>"+str(sonDiv)+"</body></html>"
        sonBsObj = BeautifulSoup(sonHtml,"html5lib")

        #得到用户主页尾URL
        targetUrl = sonBsObj.find("a",{"class":{"p_author_face "}})
        if 'href' in targetUrl.attrs:
            userMainPageUrl = targetUrl.attrs['href']

        #得到子页面文本
        targetContents = sonBsObj.findAll("div",{"class":{"d_post_content j_d_post_content clearfix","core_reply j_lzl_wrapper"}})
        for targetContent in targetContents:
            content = targetContent.get_text()

        content = userMainPageUrl+":"+content

        #得到评论用户名及评论内容
    return content

def getTargetInfo(content):
    infos = set()
    results = re.findall(r"\b[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}|1[3|4|5|7|8]\d{9}|\d{5,10}|0\d{2,3}-\d{5,9}\b",content)
    for result in results:
        if re.match(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}",result) != None:
            result = "[email:"+result+"]"
            infos.add(result)
        elif (re.match(r"1[3|4|5|7|8]\d{9}",result) != None)or(re.match(r"0\d{2,3}-\d{5,9}",result) != None):
            result = "[phone:"+result+"]"
            infos.add(result)
        else:
                result = "[qq:"+result+"]"
                infos.add(result)
    return infos
def getFirstUrl(firstUrlStr):
    firstUrl= "http://tieba.baidu.com/f?kw="+firstUrlStr+"&ie=utf-8"
    return firstUrl
if __name__ == "__main__":
    main()